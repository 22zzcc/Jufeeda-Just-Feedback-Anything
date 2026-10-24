#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py —— 反馈 harness 入口
=============================

用法（在项目根目录）：

    python main.py review examples/sample_prd.md          # 反馈任何事（评审文件/文本）
    python main.py add "修复登录 bug"                      # 记录一件需要完成的事
    python main.py list                                   # 列出待办
    python main.py done <id>                              # 标记完成
    python main.py nudge                                  # 督促：看看还有什么没完成
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def main() -> None:
    parser = argparse.ArgumentParser(description="JUST FEEDBACK ANYTHING · 反馈任何事")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_review = sub.add_parser("review", help="评审文件或文本（反馈任何事）")
    p_review.add_argument("target", help="文件路径或文本")
    p_review.add_argument("--json", action="store_true", help="JSON 输出")
    p_review.add_argument("--llm", action="store_true", help="追加 LLM 一致性评审（需 Ollama）")

    p_add = sub.add_parser("add", help="记录一件需要完成的事")
    p_add.add_argument("text", help="要记录的事")
    p_add.add_argument("--kind", default="todo", choices=["todo", "feedback", "goal"],
                       help="类型：todo/feedback/goal")

    p_list = sub.add_parser("list", help="列出记录（默认待办）")
    p_list.add_argument("--all", action="store_true", help="显示全部（含已完成）")

    p_done = sub.add_parser("done", help="标记一件事为完成")
    p_done.add_argument("task_id", help="任务 id")

    p_nudge = sub.add_parser("nudge", help="督促：看看还有什么没完成")

    args = parser.parse_args()

    from harness.store import TaskStore

    # 记录/督促类命令
    if args.cmd == "add":
        store = TaskStore()
        t = store.add(args.text, kind=args.kind)
        print(f"已记录 [{t['kind']}] {t['id']}：{t['text']}")
        print(store.nudge())
        return
    if args.cmd == "list":
        store = TaskStore()
        tasks = store.list(None if args.all else "pending")
        for t in tasks:
            mark = "✅" if t["status"] == "done" else "⏳"
            print(f"  {mark} {t['id']} [{t['kind']}] {t['text']}")
        print(f"（{len(tasks)} 条 / 共 {len(store.tasks)} 条）")
        return
    if args.cmd == "done":
        store = TaskStore()
        t = store.done(args.task_id)
        print(f"✅ 完成：{t['text']}" if t else f"未找到待办 {args.task_id}")
        print(store.nudge())
        return
    if args.cmd == "nudge":
        store = TaskStore()
        print(store.nudge())
        return

    # 反馈命令
    from harness.harness import FeedbackHarness
    from harness.output import to_markdown, to_json

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
