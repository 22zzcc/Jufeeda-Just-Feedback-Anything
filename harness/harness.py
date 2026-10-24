# -*- coding: utf-8 -*-
"""
harness/harness.py —— 反馈 harness 编排
========================================

把「文档类型识别 → 规则评审器 → 可选 LLM 评审」串成一个可复用的 review()。
「反馈任何事」= 输入任意文本，自动识别类型、套用对应必要章节、输出结构化反馈。
"""
from __future__ import annotations

from .profiles import detect_profile
from .reviewers import REVIEWERS
from .types import FeedbackResult, Issue


class FeedbackHarness:
    def __init__(self, llm=None):
        self.llm = llm

    def review(self, text: str) -> FeedbackResult:
        profile = detect_profile(text)
        issues: list[Issue] = []
        for name, fn in REVIEWERS:
            issues.extend(fn(text, profile))

        # 可选：LLM 做一致性/整体判断（不阻塞规则层）
        if self.llm is not None:
            try:
                issues.extend(self._llm_review(text, profile))
            except Exception:
                pass
        return FeedbackResult(target_type=profile, issues=issues)

    def _llm_review(self, text: str, profile: str) -> list[Issue]:
        """LLM 评审：整体一致性/自相矛盾（规则层难覆盖的部分）。"""
        prompt = ("你是文档评审者。判断下面文档是否有自相矛盾/逻辑不一致的地方，"
                  "输出 JSON 数组，每项含 severity/category/message/suggestion，"
                  "没有就输出空数组 []。\n文档：\n" + text[:3000] + "\nJSON：")
        obj = self.llm.json(prompt)
        out = []
        for it in obj:
            if isinstance(it, dict) and it.get("message"):
                out.append(Issue(
                    severity=it.get("severity", "warning"),
                    category=it.get("category", "一致性"),
                    location="全局(LLM)", message=it["message"],
                    suggestion=it.get("suggestion", "修正矛盾点并重新对照"),
                    acceptance="无自相矛盾表述"))
        return out
