# Tech Stack

- **项目类型与入口**：CLI + 可导入的 Python 库。`python main.py review <文件|文本>`。
- **语言与运行时**：Python 3.10+，标准库为主。
- **核心选择**：
  - 规则评审器：纯 Python 正则/关键词（离线、确定性、可解释）；
  - LLM 评审器（可选）：本地 Ollama，仅做「一致性/整体判断」增强，不阻塞规则层；
  - 输出：Markdown + JSON（结构化）。
- **测试与验证方式**：`python main.py review examples/sample_prd.md` 应命中「缺失必要章节(error) + 模糊措辞(warning)」；跑 `specs/features/2025-01-01-core/validation.md` 清单全绿。
- **约束**：不得新增第三方依赖（除可选 numpy）；反馈不修改输入；规则层必须离线可跑。
- **已知空白**：不做多文件/目录递归评审；不做自动修复。
