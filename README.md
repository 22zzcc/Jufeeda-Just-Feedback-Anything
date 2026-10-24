# Feedback Harness · 反馈任何事

> 一句话：一个**可复用的反馈 harness**——给它「任何事」（PRD / feature spec / roadmap /
> 简历 / 报告 / 代码 diff……），它输出结构化反馈：问题、严重程度、位置、改进建议、验收标准。

这个项目**用 SDD 开发自己**（specs/ 里是它自己的 mission/tech-stack/roadmap/requirements/plan/validation），
是「SDD 自举」的最小示范。

## 用法

```bash
cd feedback-harness

# 评审一个文件
python main.py review examples/sample_prd.md

# 评审一段文本
python main.py review "这个功能大概需要优化一下"

# JSON 输出 / 追加 LLM 一致性评审（需 Ollama）
python main.py review examples/sample_prd.md --json
python main.py review examples/sample_prd.md --llm
```

## 反馈结构（每条反馈 5 要素）

| 字段 | 说明 |
| :--- | :--- |
| severity | error / warning / info |
| category | 清晰度 / 可验证性 / 完整性 / 可执行性 |
| location | 行号 + 片段 |
| message | 问题描述 |
| suggestion | 改进建议 |
| **acceptance** | **验收标准（怎么算改好了）** ← SDD 精髓 |

## 四条可插拔评审器

| 评审器 | 检查什么 | 示例 |
| :--- | :--- | :--- |
| 清晰度 | 模糊措辞（大概/尽量/等等/TODO） | 「还有一些别的功能等等」 |
| 可验证性 | 空泛成功/质量措辞、缺数字指标 | 「会很好用」「性能要快一点」 |
| 完整性 | 按文档类型查必要章节缺失 | PRD 缺「成功标准」 |
| 可执行性 | 未决问题/待定决策 | 「目标用户是谁还没想好」 |

文档类型自动识别（spec / prd / roadmap / resume / generic），必要章节模板在
`harness/profiles.py`，新增类型只加一行。

## SDD 自举

`specs/` 目录是这个 harness 自己的 SDD 产物：

```
specs/
├── mission.md        # 项目宪法：为什么存在、成功标准
├── tech-stack.md     # 技术边界
├── roadmap.md        # 三阶段推进顺序
└── features/2025-01-01-core/
    ├── requirements.md   # 范围/范围外/行为/决策/背景/未决问题
    ├── plan.md           # task group 实现顺序
    └── validation.md     # 验收清单（独立验证）
```

## 设计要点

- **反馈 ≠ 修改**：只报告、不改内容（harness 是「评论家」不是「执行者」），
  与 SDD「验证者不当裁判」一脉相承。
- **每条反馈带 acceptance**：不只说「有问题」，还说「怎么算改好了」，可直接当回归项。
- **规则层离线可跑**：四类评审器纯标准库；LLM 只做「一致性」增强、可选。
- **可插拔**：reviewer 统一签名 `(text, profile) -> list[Issue]`，新评审器注册即生效。

## 参考

- SDD（Spec-Driven Development）：https://github.com/learnllm-ai/SDD_Starter
