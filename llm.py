# -*- coding: utf-8 -*-
"""
llm.py —— 本地模型接口（可选，仅做增强）
=========================================
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request

OLLAMA_URL = "http://127.0.0.1:11434"
MODEL = "qwen3:4b"


class LLM:
    def __init__(self, model: str = MODEL, url: str = OLLAMA_URL):
        self.model, self.url = model, url

    def json(self, prompt: str) -> list:
        payload = {"model": self.model, "prompt": prompt, "stream": False,
                   "format": "json", "options": {"temperature": 0.1}}
        req = urllib.request.Request(self.url + "/api/generate",
                                     data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                body = json.loads(r.read().decode())
        except urllib.error.URLError as e:
            raise RuntimeError(f"无法连接 Ollama：{e}") from e
        raw = (body.get("response") or "[]").strip()
        s, e = raw.find("["), raw.rfind("]")
        return json.loads(raw[s:e + 1] if s != -1 and e > s else "[]")
