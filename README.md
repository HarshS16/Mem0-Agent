# 🎙️ Voice-Controlled Local AI Agent
A highly polished, robust, and lightning-fast voice-controlled AI agent built with **Streamlit** and powered conceptually by **Groq** APIs. 

This agent listens to your microphone (or accepts uploaded audio files), transcribes your speech, extracts actionable tool intents using a 70-billion parameter LLM, natively prompts you for confirmation, and executes code or text generation directly to your local file system.

This project was built iteratively, integrating robust edge-case handling, dynamic naming algorithms, and a seamless native memory-state architecture.

---

## Demo Video : https://youtu.be/7DlyI9wOGCk



## ⚡ Architecture
- **Framework:** Streamlit (Python 3.14+)
- **Audio Inputs:** Streamlit Native `st.audio_input` & `st.file_uploader`.
- **Speech-to-Text (STT):** Groq `whisper-large-v3-turbo` (Chosen for near-instant execution speed).
- **Intent Classification:** Groq `llama-3.3-70b-versatile` mapped explicitly into JSON structured decoding logic.
- **Data Persistence:** Custom lightweight `memory_layer.py` JSON storage. Bypasses bulky vector requirements.

> **Hardware Note:** 
> Ollama and local models like Wav2Vec were intentionally skipped due to computational bottlenecks. Groq API handles dense 70B LLMs and Whisper transcription in ~1 second total pipeline execution, making the voice agent feel truly conversational and instantaneous. 

---

## 🎯 Supported Core Intents
1. `create_file`: Generates empty files safely directly into the `output/` sandbox.
2. `write_code`: Uses the LLM to write code *or* dense textual paragraphs (e.g. readmes, articles) and save them to a file.
3. `summarize_text`: Parses long texts and returns cohesive summaries.
4. `general_chat`: Handles standard conversational queries smoothly.

---

## 🌟 The "Gold-Standard" Feature List

We extensively added over **6 unique Bonus Features** to make this agent production-ready:

* ✅ **Compound Commands:** The intent extractor maps `pydantic` arrays, comfortably slicing a single voice command like *"Create a python script for math, and also summarize this paragraph in summary.txt"* into parallel sequential executions!
* ✅ **Dynamic File Naming:** Instead of defaulting identically to `output.txt`, the LLM extracts an implicitly requested name (e.g., *"Make notes.txt"*). If you skip naming the file entirely, it parses the context and self-hallucinates incredibly descriptive file abstractions like `india_summary.txt` or `weather_fetcher.py`.
* ✅ **Intent Confidence Scoring:** The LLM internally scales and mathematically evaluates its intent deductions, outputting a quantifiable percentage rating (e.g., `Confidence: 98.4%`) to the dashboard.
* ✅ **Pipeline Execution UI:** An aggregated, beautifully unified dashboard blocks rendering the trace precisely: `🎤 Transcript -> 🧠 Intent -> ⚙️ Action -> 📁 Output`.
* ✅ **Human-in-the-Loop:** Safety first. Before any file mutations or operations execute, a strict confirmation block drops into the UI to await your command. Operations are locked to the `output/` folder directory to prevent accidental system overwrites!
* ✅ **Command History (Sidebar):** An interactive click-to-load history panel. Previous processes don't disappear; click their buttons on the left pane and the entire main Streamlit UI shifts backward in time conceptually to display their state mappings exactly.
* ✅ **Graceful Degradation:** Failsafes catch native Whisper zero-silence hallucinations (`[BLANK_AUDIO]`, `Thank you.`), handles unmapped requests using a strict `unknown_intent` safety catch, and cleanly intercepts empty widget components.
* ✅ **Persistent Local Memory:** Instead of complex LLM vector databases, the agent transparently keeps context memory spanning your history natively stored in JSON, keeping conversations logically connected!
* ✅ **Soft Interface Clears:** Audio inputs cache stubbornly. Clicking "Clear All & New Task" dynamically intercepts Streamlit component keys, forcing browsers to drop the microphone caches and present a shiny blank recording space!

---

## 🚀 How To Run Locally

1. **Clone the repository.**
2. **Install project dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up API Keys:**
   Copy `.env.example` to `.env` and insert your API key:
   ```env
   GROQ_API_KEY=gsk_your_key_here
   ```
4. **Boot the Streamlit Server:**
   ```bash
   streamlit run app.py
   ```
5. Check your `output/` folder for dynamically generated voice-code!
