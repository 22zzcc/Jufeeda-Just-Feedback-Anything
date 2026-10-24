# Validation: 核心反馈闭环

> 执行者应为独立验证者（或你自己），不为实现者。

- [ ] 自动化：`python main.py review examples/sample_prd.md` 输出包含「完整性」类 error（缺失必要章节）
- [ ] 自动化：同一命令输出包含「清晰度」类 warning（模糊措辞）
- [ ] 自动化：每条 Feedback 都带非空的 suggestion 与 acceptance
- [ ] 场景：对 `specs/features/2025-01-01-core/requirements.md`（一份较完整的 spec）评审，完整性 error 应显著少于 sample_prd
- [ ] 输出：`python main.py review <text> --json` 输出合法 JSON
