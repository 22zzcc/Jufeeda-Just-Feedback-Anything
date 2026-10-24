# -*- coding: utf-8 -*-
"""
harness/output.py —— 反馈输出（Markdown + JSON）
================================================
"""
from __future__ import annotations

import json

from .types import FeedbackResult

_SEV_ICON = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}


def to_markdown(r: FeedbackResult) -> str:
    lines = [f"# 反馈报告（类型：{r.target_type}）", ""]
    s = r.summary()
    lines.append(f"共 {s['total']} 条：{s['by_severity']}，分类 {s['by_category']}")
    lines.append("")
    if not r.issues:
        lines.append("✅ 未发现问题。")
    for i, it in enumerate(r.issues, start=1):
        icon = _SEV_ICON.get(it.severity, "·")
        lines.append(f"## {i}. {icon} [{it.severity}] {it.category} — {it.location}")
        lines.append(f"- **问题**：{it.message}")
        lines.append(f"- **建议**：{it.suggestion}")
        lines.append(f"- **验收**：{it.acceptance}")
        lines.append("")
    return "\n".join(lines)


def to_json(r: FeedbackResult) -> str:
    return json.dumps(r.to_dict(), ensure_ascii=False, indent=2)
