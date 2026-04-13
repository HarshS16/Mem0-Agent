import os
from intent import ToolCall
from pydantic import BaseModel
from config import OUTPUT_DIR, GROQ_API_KEY, LLM_MODEL
from groq import Groq

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

class ToolResult(BaseModel):
    success: bool
    message: str
    file_path: str | None = None
    content: str | None = None

def sanitize_filename(filename: str) -> str:
    return os.path.basename(filename)

def execute_tool(tool_call: ToolCall) -> ToolResult:
    if tool_call.intent == "create_file":
        if not tool_call.filename:
            return ToolResult(success=False, message="Filename missing for create_file.")
        safe_name = sanitize_filename(tool_call.filename)
        path = os.path.join(OUTPUT_DIR, safe_name)
        try:
            with open(path, "w", encoding="utf-8") as f:
                pass
            return ToolResult(success=True, message=f"Created empty file at {safe_name}", file_path=path)
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to create file: {e}")
            
    elif tool_call.intent == "write_code":
        if not tool_call.filename:
            return ToolResult(success=False, message="Filename missing for write_code.")
        if not tool_call.content:
             return ToolResult(success=False, message="Requirements missing for write_code.")
        
        system_prompt = f"You are an AI generating content for a file. If the user asks for code, write ONLY the raw code. If they ask for text/paragraphs, write the text. Do not wrap in markdown codeblocks, just provide the exact raw file content. Language Context: {tool_call.language or 'auto'}"
        try:
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": tool_call.content}
                ]
            )
            code_content = response.choices[0].message.content
            if code_content.startswith("```"):
                lines = code_content.split('\n')
                if len(lines) > 2 and lines[-1].strip() == "```":
                    code_content = '\n'.join(lines[1:-1])
            
            safe_name = sanitize_filename(tool_call.filename)
            path = os.path.join(OUTPUT_DIR, safe_name)
            with open(path, "w", encoding="utf-8") as f:
                f.write(code_content)
                
            return ToolResult(success=True, message=f"Wrote generated code to {safe_name}", file_path=path, content=code_content)
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to generate code: {e}")
            
    elif tool_call.intent == "summarize_text":
        if not tool_call.content:
            return ToolResult(success=False, message="Content missing for summarize_text.")
        try:
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Summarize the user's text concisely."},
                    {"role": "user", "content": tool_call.content}
                ]
            )
            summary = response.choices[0].message.content
            return ToolResult(success=True, message="Summarized text successfully.", content=summary)
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to summarize: {e}")
            
    elif tool_call.intent == "general_chat":
        try:
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": "You are a friendly Voice AI Agent. Respond nicely but concisely."},
                    {"role": "user", "content": tool_call.content or "Hello"}
                ]
            )
            chat_reply = response.choices[0].message.content
            return ToolResult(success=True, message="Sent chat reply.", content=chat_reply)
        except Exception as e:
            return ToolResult(success=False, message=f"Failed general chat: {e}")
            
    return ToolResult(success=False, message=f"Unknown intent: {tool_call.intent}")
