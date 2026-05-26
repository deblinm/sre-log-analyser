import httpx
from app.core.models import  LogEntry
import os


class LLMAnalyser:

    def __init__(self):
        self.base_url= os.environ.get("OLLAMA_URL", "http://localhost:11434")
        self.model="phi3"

    def _build_prompt  (self,level, service,message):
        return (f"you are an SRE assistant, given this log entry with "
                f"Level: {level}\n"
                f"Service: {service}\n"
                f"Message: {message} , \n"
                f"explain what the error means and suggest a fix. "
                f"Be concise. Structure your response with two sections: \"Explanation:\" and \"Suggested Fix:\"")

    def analyse (self,log : LogEntry):
        data= {"model": self.model, "prompt": self._build_prompt(log.level.value, log.service, log.message), "stream": False}
        httpx_call = httpx.post(self.base_url+"/api/generate",json=data,timeout=120.0)
        return httpx_call.json()["response"]