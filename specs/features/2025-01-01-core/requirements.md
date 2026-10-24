# Requirements: 核心反馈闭环

- **范围**：一个可导入的 Python harness，对任意文本输出结构化反馈；四条规则评审器；Markdown/JSON 输出。
- **范围外**：不自动修复、不多文件目录递归（见 Phase 3 之后）、不做 LLM 一致性评审（见 Backlog）。
- **行为**：输入文本 → 逐行/逐段扫描 → 每条命中的问题生成一条 Feedback（severity/category/location/message/suggestion/acceptance）→ 汇总输出。
- **决策**：
  - Feedback 用 dataclass，severity 三档 error/warning/info；
  - 位置用「行号 + 片段」定位；
  - reviewer 用统一签名 `(text, profile) -> list[Issue]`，可插拔。
- **背景**：遵循 `specs/mission.md` 与 `specs/tech-stack.md`；输出口径对齐 SDD 的 validation（每条反馈带验收标准）。
- **未决问题**：一致性检测（自相矛盾）规则较难精确，暂用「模糊措辞 + 未决问题」近似，LLM 增强放 Backlog。
