# 🎙️ Voice-Controlled Local AI Agent

A highly polished, robust, and lightning-fast voice-controlled AI agent built with **Streamlit** and powered conceptually by **Groq** APIs.

This agent listens to your microphone (or accepts uploaded audio files), transcribes your speech, extracts actionable tool intents using a 70-billion parameter LLM, natively prompts you for confirmation, and executes code or text generation directly to your local file system.

This project was built iteratively, integrating robust edge-case handling, dynamic naming algorithms, and a seamless native memory-state architecture.

---

## Demo Video : https://youtu.be/7DlyI9wOGCk

## Medium Article : https://medium.com/@harsh-jsx/building-a-voice-controlled-local-ai-agent-from-audio-to-action-9973b17e7138

---

## ⚡ Architecture

* **Framework:** Streamlit (Python 3.14+)
* **Audio Inputs:** Streamlit Native `st.audio_input` & `st.file_uploader`
* **Speech-to-Text (STT):** Groq `whisper-large-v3-turbo`
* **Intent Classification:** Groq `llama-3.3-70b-versatile`
* **Data Persistence:** Custom lightweight `memory_layer.py` JSON storage

> **Hardware Note:**
> Ollama and local models like Wav2Vec were intentionally skipped due to computational bottlenecks. Groq API handles dense 70B LLMs and Whisper transcription in ~1 second total pipeline execution, making the voice agent feel truly conversational and instantaneous.

---

## 🧪 Model Benchmarking

During development, multiple model options were evaluated to balance **speed, accuracy, and ease of deployment**.

### 🔍 Speech-to-Text Comparison

| Model            | Speed     | Accuracy | Setup Complexity     |
| ---------------- | --------- | -------- | -------------------- |
| Local Whisper    | Medium    | High     | High (GPU/CPU heavy) |
| Groq Whisper API | Very Fast | High     | Very Low             |

**Observation:**
While local Whisper provides offline capability, it introduces latency and hardware constraints. The Groq Whisper API delivers near-instant transcription with comparable accuracy.

**Decision:**
Groq Whisper was selected for its **real-time performance and seamless integration**.

---

### 🔍 Intent Classification Comparison

| Model              | Speed     | Accuracy | Reliability              |
| ------------------ | --------- | -------- | ------------------------ |
| Local LLM (Ollama) | Slow      | Medium   | Inconsistent JSON output |
| Groq LLaMA 70B     | Very Fast | High     | Highly structured        |

**Observation:**
Local models struggled with structured intent extraction and produced inconsistent outputs. The 70B Groq model consistently returned clean, structured JSON suitable for deterministic tool execution.

**Decision:**
Groq `llama-3.3-70b-versatile` was chosen for **high accuracy, structured outputs, and low latency**.

---

### 🧠 Final Takeaway

The final architecture prioritizes:

* ⚡ Real-time responsiveness
* 🎯 High intent accuracy
* 🧩 Clean structured outputs

This ensures the agent feels **fast, reliable, and production-ready**, rather than experimental.

---

## 🎯 Supported Core Intents

1. `create_file`: Generates empty files safely inside the `output/` sandbox
2. `write_code`: Generates code or structured text and writes directly to a file
3. `summarize_text`: Produces concise summaries of long text inputs
4. `general_chat`: Handles conversational queries

---

## 🌟 The "Gold-Standard" Feature List

We extensively added over **6 unique Bonus Features** to make this agent production-ready:

* ✅ **Compound Commands:** Handles multi-step instructions in a single input
* ✅ **Dynamic File Naming:** Extracts or intelligently generates contextual filenames
* ✅ **Intent Confidence Scoring:** Displays quantified confidence levels for predictions
* ✅ **Pipeline Execution UI:** Clearly visualizes each stage of execution
* ✅ **Human-in-the-Loop:** Requires confirmation before executing file operations
* ✅ **Command History (Sidebar):** Interactive history with state restoration
* ✅ **Graceful Degradation:** Handles edge cases like silence or unknown intents
* ✅ **Persistent Local Memory:** Maintains context using lightweight JSON storage
* ✅ **Soft Interface Clears:** Resets audio input state dynamically

---

## 🚀 How To Run Locally

1. **Clone the repository**
2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
3. **Set up API keys:**
   Copy `.env.example` → `.env`

   ```env
   GROQ_API_KEY=gsk_your_key_here
   ```
4. **Run the app:**

   ```bash
   streamlit run app.py
   ```
5. Check the `output/` folder for generated files

---

## 🧠 Final Note

This project focuses on building a **real-world AI agent pipeline**, not just a chatbot.
By combining voice input, structured reasoning, and local execution, it demonstrates how AI systems can move from passive responses to **action-oriented assistants**.


