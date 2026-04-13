import streamlit as st
import os
from config import OUTPUT_DIR
from stt import transcribe_audio
from intent import classify_intent, ToolCall
from tools import execute_tool, ToolResult
from memory_layer import record_user_message, get_relevant_memories

st.set_page_config(page_title="Mem0 Voice Agent", page_icon="🎙️", layout="wide")

if "command_history" not in st.session_state:
    st.session_state.command_history = []

if "pending_tools" not in st.session_state:
    st.session_state.pending_tools = []
    
if "pipeline_results" not in st.session_state:
    st.session_state.pipeline_results = {}
    
if "last_audio" not in st.session_state:
    st.session_state.last_audio = None

if "widget_key" not in st.session_state:
    st.session_state.widget_key = 0

st.title("🎙️ Mem0 Voice Agent")

with st.sidebar:
    st.header("🧠 Command History")
    if not st.session_state.command_history:
        st.write("No commands yet.")
    else:
        for i, cmd in enumerate(st.session_state.command_history):
            label = cmd.get("transcript", "Empty Recording...")
            label = label[:25] + "..." if len(label) > 25 else label
            if st.button(f"💬 {label}", key=f"hist_{i}"):
                st.session_state.pipeline_results = cmd
                st.session_state.pending_tools = []
                # Rerun to switch view
                st.rerun()
        
    st.header("📁 Output Directory")
    if os.path.exists(OUTPUT_DIR):
        files = os.listdir(OUTPUT_DIR)
        for f in files:
            st.write(f"📄 {f}")
    else:
        st.write("No files generated yet.")

col1, col2 = st.columns(2)

new_audio_value = None

with col1:
    st.subheader("🎤 Microphone")
    audio_value_mic = st.audio_input("Record your voice", key=f"mic_{st.session_state.widget_key}")
    if audio_value_mic:
        new_audio_value = audio_value_mic

with col2:
    st.subheader("📁 Upload File")
    audio_value_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "ogg", "m4a", "flac"], key=f"file_{st.session_state.widget_key}")
    if audio_value_file:
         new_audio_value = audio_value_file

# Check if new audio was uploaded/recorded
if new_audio_value and new_audio_value != st.session_state.last_audio:
    st.session_state.last_audio = new_audio_value
    st.session_state.pending_tools = []
    
    # Start a new pipeline result and attach it to history immediately
    st.session_state.pipeline_results = {}
    st.session_state.command_history.append(st.session_state.pipeline_results)
    
    with st.spinner("Transcribing..."):
        bytes_data = new_audio_value.getvalue()
        file_name = getattr(new_audio_value, "name", "audio.wav")
        transcript = transcribe_audio(bytes_data, file_name)
        
        # --- Error Handling: No Audio / Unclear Speech ---
        cleaned_t = transcript.strip()
        hallucinations = ["Thank you.", "Thank you", "Thanks for watching.", "Thanks for watching", "[BLANK_AUDIO]", ""]
        if not cleaned_t or cleaned_t in hallucinations or len(cleaned_t) < 2:
            transcript = "Error: No clear audio detected or speech was unclear. Please try again."
            
        st.session_state.pipeline_results["transcript"] = transcript
        
    if transcript.startswith("Error"):
        st.error(transcript)
    else:
        memories = get_relevant_memories(transcript)
        with st.spinner("Classifying Intent..."):
            intent_result = classify_intent(transcript, memory_context=memories)
            st.session_state.pipeline_results["intent"] = intent_result
            
            if intent_result:
                st.session_state.pending_tools = intent_result.tool_calls
                record_user_message(f"User said: {transcript}")

# Display Pipeline Results
if "transcript" in st.session_state.pipeline_results:
    st.markdown("### 🌟 Pipeline Execution")
    
    t_text = st.session_state.pipeline_results["transcript"]
    if t_text.startswith("Error"):
        st.error(t_text)
    else:
        st.write("**🎤 Transcript:**", t_text)
        
        if "intent" in st.session_state.pipeline_results:
            intent_result = st.session_state.pipeline_results["intent"]
            if intent_result:
                intents_list = [f"{tc.intent} ({getattr(tc, 'confidence', 1.0) * 100:.0f}%)" for tc in intent_result.tool_calls]
                st.write("**🧠 Intent:**", ", ".join(intents_list))
                
        if "tools_done" in st.session_state.pipeline_results:
            for tool_name, res in st.session_state.pipeline_results["tools_done"]:
                st.write("**⚙️ Action:**", f"Executed `{tool_name}`" + (" ❌ Failed" if not res.success else ""))
                
                out_txt = res.message
                if res.file_path:
                    out_txt += f" | Saved: {res.file_path}"
                st.write("**📁 Output:**", out_txt)
                if res.content:
                    with st.expander("Preview Content Cache"):
                        st.write(res.content)
        elif st.session_state.pending_tools:
            st.write("**⚙️ Action:**", "⏳ *Pending human confirmation...*")
            st.write("**📁 Output:**", "⏳ *Waiting...*")

# Human In the Loop Confirmation
if st.session_state.pending_tools:
    # --- Error Handling: Unknown Intent ---
    if any(t.intent == "unknown_intent" for t in st.session_state.pending_tools):
        st.markdown("### ⚠️ Action Failed")
        st.error("Unknown Intent: Your request was not understood or mapped to a valid tool effectively. Please clarify.")
        if st.button("Dismiss"):
            st.session_state.pending_tools = []
            st.rerun()
    else:
        st.markdown("### ⚡ Pending Actions")
        st.warning("The following actions are pending human confirmation:")
        
        for tool in st.session_state.pending_tools:
            st.write(f"**{tool.intent}**: {tool.description}")
        
    col_ok, col_no = st.columns([1, 4])
    with col_ok:
        if st.button("✅ Confirm"):
            results = []
            for tool in st.session_state.pending_tools:
                res = execute_tool(tool)
                results.append((tool.intent, res))
                record_user_message(f"System executed {tool.intent}. Result: {res.message}")
                
            st.session_state.pipeline_results["tools_done"] = results
            st.session_state.pending_tools = []
            st.rerun()
    with col_no:
        if st.button("❌ Cancel"):
            st.session_state.pending_tools = []
            st.warning("Action cancelled by human.")
            st.rerun()



st.markdown("---")
if st.button("🗑️ Clear All & New Task"):
    # Save the widget_key to increment it before clearing
    current_key = st.session_state.get("widget_key", 0)
    st.session_state.clear()
    # Increment key forces Streamlit to render fresh, blank audio widgets
    st.session_state.widget_key = current_key + 1
    st.rerun()
