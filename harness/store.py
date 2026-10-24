# -*- coding: utf-8 -*-
"""
harness/store.py —— 记录任何事 + 督促完成（Jufeeda 的记忆层）
============================================================================

不只是「反馈」，还能「记录你需要完成的任何事」——代码反馈、产品迭代、目标、待办。
持久化到本地 JSON，支持 add / list / done / nudge。

「督促完成」是成长教练的核心：nudge() 不只列出待办，还用教练语气催一句，
让「记录 → 督促 → 完成」形成闭环。
"""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path


class TaskStore:
    """记录任何事：待办/目标/反馈项 的持久化存储。"""

    def __init__(self, path: str = "data/tasks.json"):
        self.path = Path(path)
        self.tasks: list[dict] = self._load()

    def _load(self) -> list[dict]:
        if self.path.exists():
            return json.loads(self.path.read_text(encoding="utf-8"))
        return []

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.tasks, ensure_ascii=False, indent=2),
                             encoding="utf-8")

    # ---- 记录 ----
    def add(self, text: str, kind: str = "todo") -> dict:
        task = {"id": uuid.uuid4().hex[:8], "text": text, "kind": kind,
                "status": "pending", "created_at": time.time(), "done_at": None}
        self.tasks.append(task)
        self.save()
        return task

    # ---- 查看 ----
    def list(self, status: str | None = None) -> list[dict]:
        return [t for t in self.tasks if status is None or t["status"] == status]

    def pending(self) -> list[dict]:
        return self.list("pending")

    # ---- 完成 ----
    def done(self, task_id: str) -> dict | None:
        for t in self.tasks:
            if t["id"] == task_id and t["status"] == "pending":
                t["status"] = "done"
                t["done_at"] = time.time()
                self.save()
                return t
        return None

    # ---- 督促（成长教练的语气）----
    def nudge(self) -> str:
        pending = self.pending()
        if not pending:
            return "🎉 全部完成！没有待办。去给自己加个新目标吧：`python main.py add \"...\"`"
        lines = [f"还有 {len(pending)} 件事没完成，别攒着：", ""]
        for i, t in enumerate(sorted(pending, key=lambda x: x["created_at"]), start=1):
            days = (time.time() - t["created_at"]) / 86400
            lines.append(f"  {i}. [{t['kind']}] {t['text']}（已 {days:.0f} 天）")
        lines.append("")
        lines.append("挑最小的一件先做，做完就 `python main.py done <id>`。"
                     "反馈会记住你的每一次完成。")
        return "\n".join(lines)

    def stats(self) -> dict:
        from collections import Counter
        return {"total": len(self.tasks),
                "pending": len(self.pending()),
                "done": sum(1 for t in self.tasks if t["status"] == "done"),
                "by_kind": dict(Counter(t["kind"] for t in self.tasks))}
