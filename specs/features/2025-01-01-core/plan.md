# Plan: 核心反馈闭环

## Group 1 — 类型定义与输入
1.1 定义 `Issue`（severity/category/location/message/suggestion/acceptance）与 `FeedbackResult`
1.2 输入层：读文件或直接文本，自动识别文档类型 profile

## Group 2 — 四条规则评审器
2.1 清晰度：模糊措辞词表命中
2.2 可验证性：成功/质量措辞过空泛、缺数字指标
2.3 完整性：按 profile 检查必要章节是否缺失
2.4 可执行性：未决问题/待定决策

## Group 3 — 编排与输出
3.1 harness 编排：依次跑 reviewer，汇总 Feedback
3.2 输出：Markdown 与 JSON

## Group 4 — 测试
4.1 示例文档命中预期 issue 类型
