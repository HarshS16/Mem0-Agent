from typing import Literal, Optional, List
from pydantic import BaseModel, Field
import json
from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

class ToolCall(BaseModel):
    intent: Literal["create_file", "write_code", "summarize_text", "general_chat", "unknown_intent"] = Field(description="The matching intent for the tool")
    filename: Optional[str] = Field(None, description="For create_file / write_code. Extract the exact filename from user input if mentioned (e.g., 'notes.txt'). If the user does not specify a name, dynamically invent a descriptive filename relevant to the context (e.g., 'india_summary.txt' or 'fibonacci.py').")
    language: Optional[str] = Field(None, description="For write_code. Programming language (e.g., python, javascript).")
    content: Optional[str] = Field(None, description="Text to summarize, or the user's specific code requirement, or general chat message.")
    description: str = Field(description="Human-readable description of what action needs to be taken.")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0 indicating how certain you are of this intent.")

class IntentResult(BaseModel):
    tool_calls: List[ToolCall] = Field(description="A list of tool calls to execute based on user intent. Can encompass multiple actions for compound commands.")
    reasoning: str = Field(description="LLM's reasoning abstracting its decision process.")

def get_client():
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set.")
    return Groq(api_key=GROQ_API_KEY)

def classify_intent(transcription: str, memory_context: str = "") -> Optional[IntentResult]:
    """Classify the transcription into an IntentResult containing tool calls."""
    schema = IntentResult.model_json_schema()
    client = get_client()
    
    system_prompt = f"""You are an intelligent intent classification model representing a Voice AI Agent.
Analyze the user's transcription and determine what actions they want to take. Extract multiple intents if the user asks for compound commands!

Supported Intents:
- 'create_file': The user wants to create an explicitly EMPTY file. Needs a 'filename'. ONLY use this if no specific content is requested.
- 'write_code': The user wants to generate code OR text content and save it to a file. Needs 'filename' and the user's prompt what code/text to write in 'content'. Use this for code, paragraphs, readmes, text files, etc.
- 'summarize_text': The user wants to summarize a text or topic. 'content' should contain the user's topic to summarize or extract.
- 'general_chat': For everything else (small talk, questions, greetings). 'content' is the user's message.
- 'unknown_intent': Use this ONLY if the transcription is gibberish, strictly unintelligible, or completely outside the bounds of any reasonable response.

Context from past memory (Use this if the user refers to past context implicitly!):
{memory_context}

You MUST return a valid JSON object matching this schema exactly:
{json.dumps(schema, indent=2)}
"""

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcription}
            ],
            response_format={"type": "json_object"},
            temperature=0
        )
        content = response.choices[0].message.content
        data = IntentResult.model_validate_json(content)
        return data
    except Exception as e:
        print(f"Error classifying intent: {e}")
        return None
