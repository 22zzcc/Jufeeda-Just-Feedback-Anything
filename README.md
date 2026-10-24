# Jufeeda · 终端里的成长教练

> **反馈不是挑刺，是陪你变强的教练。**

一个住在终端里的**成长教练**——它记住你、催着你、陪你变强：
能**反馈任何事**、能**记录任何事**、能**督促你完成**，并**集成 SDD 开发能力**。

## 三支柱

| 支柱 | 一句话 | 命令 |
| :--- | :--- | :--- |
| ① 督促力（教练） | 持续跟进：反馈 → 行动 → 复检 → 完成 | `nudge` |
| ② 记忆力（档案） | 记录任何事 + 沉淀 badcase，越用越懂你 | `add` / `list` / `done` |
| ③ 陪伴感（终端伙伴） | 命令行原生，随叫随到 | 全部 |

## 用法

```bash
cd Jufeeda

# ① 反馈任何事
python main.py review examples/sample_prd.md
python main.py review "这个功能大概需要优化一下"

# ② 记录任何事（代码反馈 / 产品迭代 / 目标 / 待办）
python main.py add "修复登录 bug" --kind feedback
python main.py add "完成 v2 产品迭代 spec" --kind goal
python main.py list

# ③ 督促完成
python main.py nudge
python main.py done <id>
```

## 反馈结构（每条 5 要素）

severity（error/warning/info）· category（清晰度/可验证性/完整性/可执行性）· location（行号）
· message · suggestion · **acceptance（怎么算改好了）** ← SDD 精髓

## SDD 集成

1. **每条反馈带验收标准**：不只说「有问题」，还说「怎么算改好」，可直接当回归项。
2. **本项目用 SDD 开发自己**（`specs/` 目录是它自己的 mission/tech-stack/roadmap/requirements/plan/validation）——SDD 自举。
3. **能评审 SDD 产物**：内置 spec/prd/roadmap 文档类型模板，自动识别必要章节缺失。

## 愿景

从「一次性体检工具」升级到「有记忆、会督促、陪伴式的成长教练」——反馈只是起点，成长才是终点。

参考：SDD https://github.com/learnllm-ai/SDD_Starter
