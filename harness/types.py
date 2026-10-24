# -*- coding: utf-8 -*-
"""
harness/types.py —— 反馈数据模型
=================================

一条反馈 = 问题 + 严重程度 + 类别 + 位置 + 改进建议 + 验收标准。
「验收标准」是 SDD 的精髓：反馈不只说「有问题」，还说「怎么算改好了」。
"""
from __future__ import annotations

from dataclasses import dataclass, field

SEVERITY = ("error", "warning", "info")


@dataclass
class Issue:
    severity: str          # error / warning / info
    category: str          # 完整性 / 可验证性 / 清晰度 / 可执行性
    location: str          # 「行 N」或「全局」
    message: str           # 问题描述
    suggestion: str        # 改进建议
    acceptance: str        # 验收标准（怎么算改好了）

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class FeedbackResult:
    target_type: str
    issues: list[Issue] = field(default_factory=list)

    def summary(self) -> dict:
        from collections import Counter
        return {
            "target_type": self.target_type,
            "total": len(self.issues),
            "by_severity": dict(Counter(i.severity for i in self.issues)),
            "by_category": dict(Counter(i.category for i in self.issues)),
        }

    def to_dict(self) -> dict:
        return {"target_type": self.target_type,
                "issues": [i.to_dict() for i in self.issues],
                "summary": self.summary()}
