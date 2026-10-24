# -*- coding: utf-8 -*-
"""
harness/profiles.py —— 文档类型识别与必要章节模板
==================================================

「反馈任何事」的关键：不同文档类型有不同「必要章节」，缺失即 error。
这里用「关键词检测 + 必要章节模板」，新增文档类型只需加一行，无需改评审器。
"""
from __future__ import annotations

import re

# 文档类型 → 必要章节（标题关键词，命中一个算有）
PROFILES = {
    "spec": {"name": "feature spec",
             "required": {"范围": ["范围"], "范围外": ["范围外", "不做"], "行为": ["行为", "流程"],
                          "决策": ["决策", "选择"], "背景": ["背景", "约束"]}},
    "prd": {"name": "PRD",
            "required": {"目标": ["目标", "问题"], "用户": ["用户", "谁"], "功能": ["功能", "需求"],
                         "成功标准": ["成功标准", "成功", "指标"]}},
    "roadmap": {"name": "roadmap",
                "required": {"阶段": ["Phase", "阶段"], "目标": ["目标"]}},
    "resume": {"name": "简历",
               "required": {"教育": ["教育"], "项目": ["项目", "经历"], "技能": ["技能"]}},
    "generic": {"name": "通用文本", "required": {}},
}

# 识别顺序：先命中的类型优先
_DETECT = [
    ("spec", re.compile(r"范围外|feature.?spec|Requirements|技术栈|Tech.?Stack")),
    ("prd", re.compile(r"PRD|目标用户|用户痛点|产品需求")),
    ("roadmap", re.compile(r"Roadmap|Backlog|Phase\s*\d")),
    ("resume", re.compile(r"教育经历|工作经历|项目经历|求职意向")),
]


def detect_profile(text: str) -> str:
    for name, pat in _DETECT:
        if pat.search(text):
            return name
    return "generic"


def required_sections(profile: str) -> dict[str, list[str]]:
    return PROFILES.get(profile, PROFILES["generic"])["required"]
