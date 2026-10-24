#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py —— 反馈 harness 入口
=============================

用法（在项目根目录）：

    python main.py review examples/sample_prd.md          # 评审一个文件
    python main.py review "这段文字大概需要优化一下"        # 评审一段文本
    python main.py review examples/sample_prd.md --json    # JSON 输出
    python main.py review examples/sample_prd.md --llm     # 追加 LLM 一致性评审
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def main() -> None:
    parser = argparse.ArgumentParser(description="反馈 harness：反馈任何事")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_review = sub.add_parser("review", help="评审文件或文本")
    p_review.add_argument("target", help="文件路径或文本")
    p_review.add_argument("--json", action="store_true", help="JSON 输出")
    p_review.add_argument("--llm", action="store_true", help="追加 LLM 一致性评审（需 Ollama）")
    args = parser.parse_args()

    from harness.harness import FeedbackHarness
    from harness.output import to_markdown, to_json

    # 输入：文件路径 or 直接文本
    p = Path(args.target)
    text = p.read_text(encoding="utf-8") if p.is_file() else args.target

    llm = None
    if args.llm:
        from llm import LLM
        llm = LLM()

    result = FeedbackHarness(llm=llm).review(text)
    print(to_json(result) if args.json else to_markdown(result))


if __name__ == "__main__":
    main()
