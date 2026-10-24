# -*- coding: utf-8 -*-
"""
harness/reviewers.py —— 可插拔规则评审器（反馈「任何事」的四类检查）
====================================================================

四条规则评审器，统一签名 `review(text, profile) -> list[Issue]`：
    1. 清晰度    —— 模糊措辞（「大概/尽量/等等/TODO」）；
    2. 可验证性  —— 成功/质量措辞过空泛、缺数字指标；
    3. 完整性    —— 按文档类型的必要章节查缺失；
    4. 可执行性  —— 未决问题/待定决策（「是否/待定/未定」）。

纯规则、离线、可解释；LLM 增强（一致性/整体判断）可选，见 harness.py。
"""
from __future__ import annotations

import re

from .profiles import required_sections
from .types import Issue

# 模糊措辞词表（命中即 warning）
_VAGUE_TERMS = ["大概", "可能", "差不多", "尽量", "适当", "等等", "之类", "若干",
                "基本上", "TODO", "TBD", "FIXME", "待定", "后续", "以后", "暂时"]

# 空泛的成功/质量措辞（命中即 warning，提示补量化指标）
_VAGUE_QUALITY = ["更好", "更快", "好用", "易用", "用户满意", "体验好", "性能好",
                  "高质量", "稳定", "优化", "提升", "改善"]

# 未决问题/待定决策（强信号：命中即 warning）
_OPEN_TERMS = ["待定", "未定", "未决", "还没想", "以后再", "以后再说", "TODO", "TBD"]
# 弱信号「是否」：若同一行已给出「暂定/默认/确定」方案，则不判未决
_RESOLVED_MARK = re.compile(r"暂定|默认|确定|采用|选择|已定")


def _scan_lines(text: str, pattern, category, message_tpl, suggestion, acceptance,
                severity="warning") -> list[Issue]:
    """逐行扫描，命中的行生成一条 Issue（带行号定位）。"""
    issues = []
    for i, line in enumerate(text.splitlines(), start=1):
        if pattern.search(line):
            issues.append(Issue(
                severity=severity, category=category, location=f"行 {i}",
                message=message_tpl.format(term=line.strip()[:40]),
                suggestion=suggestion, acceptance=acceptance))
    return issues


# ---- ① 清晰度 ----
def review_clarity(text: str, profile: str = "") -> list[Issue]:
    pat = re.compile("|".join(re.escape(t) for t in _VAGUE_TERMS), re.I)
    return _scan_lines(text, pat, "清晰度", "模糊措辞：{term}",
                       "把模糊表述替换为具体、可判定的说法（数量/范围/标准）",
                       "该句不再含模糊词，且有明确数值或判定条件")


# ---- ② 可验证性 ----
def review_verifiability(text: str, profile: str = "") -> list[Issue]:
    pat = re.compile("|".join(re.escape(t) for t in _VAGUE_QUALITY))
    issues = _scan_lines(text, pat, "可验证性", "空泛的成功/质量措辞：{term}",
                         "补一个可测指标（数字、百分比、通过/失败条件）",
                         "该目标可被一个可执行检查判断真伪（如 Recall@5≥0.9）")
    # 全局：全文没有任何数字，提示整体缺量化
    if not re.search(r"\d", text):
        issues.append(Issue("info", "可验证性", "全局",
                            "全文未出现任何数字/量化指标，验收将无法客观执行",
                            "在关键目标与验收处补数字（时长/数量/阈值/比例）",
                            "每个关键结论都有至少一个可量化支撑"))
    return issues


# ---- ③ 完整性 ----
def review_completeness(text: str, profile: str = "") -> list[Issue]:
    issues = []
    for section, kws in required_sections(profile).items():
        if not any(kw in text for kw in kws):
            issues.append(Issue(
                "error", "完整性", "全局",
                f"缺少必要章节「{section}」（{profile} 类型要求）",
                f"补一节「{section}」，写清该类型的核心要素",
                f"文档中出现「{section}」相关内容，且无该 error"))
    return issues


# ---- ④ 可执行性 ----
def review_actionability(text: str, profile: str = "") -> list[Issue]:
    issues = _scan_lines(text, re.compile("|".join(re.escape(t) for t in _OPEN_TERMS)),
                         "可执行性", "未决问题/待定决策：{term}",
                         "给未决项一个「暂定处理方式」，或明确标注由谁、何时拍板",
                         "每个未决项都带暂定方案或明确决策人/时间点")
    # 弱信号「是否」：只有同一行没给「暂定/默认」方案才算未决
    for i, line in enumerate(text.splitlines(), start=1):
        if "是否" in line and not _RESOLVED_MARK.search(line):
            issues.append(Issue("warning", "可执行性", f"行 {i}",
                                f"未决问题：{line.strip()[:40]}",
                                "给「是否」一个暂定处理方式，或明确由谁、何时拍板",
                                "该未决项带暂定方案或明确决策人/时间点"))
    return issues


# 可插拔评审器注册表：新增评审器在此登记即可
REVIEWERS = [
    ("clarity", review_clarity),
    ("verifiability", review_verifiability),
    ("completeness", review_completeness),
    ("actionability", review_actionability),
]
