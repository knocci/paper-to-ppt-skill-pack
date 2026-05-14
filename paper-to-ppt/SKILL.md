---
name: paper-to-ppt
description: 基于论文 PDF 生成中文学术汇报中间产物的多阶段工作流。适用于 10-15 分钟课堂、组会、论文精读汇报；只负责阅读论文、总结事实、规划汇报故事线、整理图表需求和讲稿，不直接生成最终 PPT 文件。
---

# paper-to-ppt

把论文 PDF 转换为可检查、可修改、可交接的学术汇报中间产物。这个 skill 强调“汇报逻辑”，不是机械复述论文目录。

本 skill 的完成条件是生成标准中间文件，而不是生成最终演示文稿文件。

默认目标：

- 10-15 分钟课堂 / 组会 / 学术汇报
- 10-12 页汇报结构
- 中文为主，关键术语保留英文
- 每页只表达一个核心观点
- 少文字，多图示
- 不编造论文内容、实验结果、图表或公式
- 所有中间文件可检查、可修改

## 能力边界

本 skill 负责：

1. 读取论文 PDF。
2. 判断 PDF 可读性。
3. 生成事实层论文总结。
4. 将论文逻辑转成汇报故事线。
5. 生成清晰的页面规划。
6. 整理需要使用、补充或手动截图的图表。
7. 生成逐页讲稿。
8. 生成中间产物质量检查清单。

本 skill 不负责：

- 直接创建最终演示文稿文件。
- 直接套用模板文件。
- 直接编辑 Office 文件。
- 在图表不可读时猜测数据。

如果用户要求最终制作演示文稿，应先完成本 skill 的中间文件，再由用户决定后续制作方式。

## 输入

用户通常提供：

```text
/paper-to-ppt path/to/paper.pdf
```

可选参数：

```text
--slides 10|11|12
--minutes 10|15
--focus balanced|method|experiment|application|review
--audience "研一组会"
--style "学术简洁"
```

默认：

```yaml
slides: 10-12
minutes: 10-15
focus: balanced
audience: 课堂 / 组会 / 学术汇报
language: 简体中文
aspect_ratio: 16:9
```

## 输出目录

从 PDF 路径推导：

- `domain_name`：PDF 所在上一级目录名
- `paper_name`：PDF 文件名去掉 `.pdf` 后转为 lowercase kebab-case

输出目录：

```text
docs/<domain_name>/<paper_name>/paper-to-ppt/
```

必须生成：

```text
paper_summary.md
slides_plan.md
images_needed.md
speaker_notes.md
review_checklist.md
```

辅助目录：

```text
assets/extracted/
assets/manual/
assets/generated/
scripts/
```

## 强制规则

1. 先读论文，再总结事实，再规划汇报。
2. 不允许编造论文内容、实验结果、图表、公式、作者或年份。
3. 不确定内容必须标注 `待核实`。
4. PDF 无法完整读取时，必须在 `paper_summary.md` 和 `review_checklist.md` 中说明。
5. 所有关键结论、数字、方法细节和图表都必须有 `source_reference`。
6. 每页规划必须有一个 `key_message`。
7. 页面标题必须是观点式标题，不要使用 `Method`、`Experiments`、`Conclusion` 这类机械小节标题。
8. 方法页必须规划流程图、模块图或论文原方法图。
9. 实验页必须突出关键对比，不要把大表格原样堆满。
10. 如果无法自动提取图表，必须生成 `images_needed.md`，告诉用户需要手动截图哪些图。
11. 所有中间文件必须可检查、可修改。
12. `slides_plan.md` 不得包含未经论文支持的新结论。

## 工作流

### Step 0：初始化

1. 确认输入 PDF 存在。
2. 创建输出目录和子目录。
3. 复制或引用本 skill 的模板文件。
4. 若缺少 PDF 读取能力，停止并说明：无法可靠读取论文，不能继续生成中间产物。

推荐目录创建命令：

```bash
mkdir -p docs/<domain_name>/<paper_name>/paper-to-ppt/{assets/extracted,assets/manual,assets/generated,scripts}
```

### Step 1：读取论文 PDF

完整读取 PDF，至少检查：

```yaml
pdf_read_status:
  total_pages:
  readable_pages:
  unreadable_pages:
  has_text_layer:
  has_figures:
  has_tables:
  has_equations:
  warnings:
```

如果 PDF 读取不完整，继续生成可用部分，但必须显式标注风险。

### Step 2：生成 `paper_summary.md`

使用 `templates/paper_summary_template.md`。

要求：

- 这是事实层文件，不是页面大纲。
- 只记录论文中能确认的内容。
- 包含基本信息、研究问题、核心贡献、方法、公式、实验、结果、图表清单、局限和待核实项。
- 每个重要内容都带 `source_reference`。
- 不能把自己的推测写成论文结论。

### Step 3：生成汇报故事线

把论文逻辑转换成汇报逻辑：

```text
为什么这个问题重要
→ 现有方法卡在哪里
→ 作者的核心洞察是什么
→ 方法如何实现这个洞察
→ 实验证据是否支持主张
→ 贡献、局限与启发是什么
```

默认 10-12 页：

1. 封面
2. 背景问题
3. 现有瓶颈
4. 核心洞察
5. 方法总览
6. 关键模块 / 公式
7. 实验设计
8. 主结果
9. 消融 / 分析
10. 案例 / 可视化 / 讨论
11. 总结与局限
12. 启发与 Q&A

如果只做 10 页，合并第 9-10 页和第 11-12 页。

### Step 4：生成 `slides_plan.md`

使用 `templates/slides_plan_template.md`。

每页必须包含：

```yaml
slide_number:
title:
key_message:
bullet_points:
visual_suggestion:
speaker_note:
source_reference:
```

`slides_plan.md` 是后续制作演示文稿的核心交接文件。生成完成后应允许用户检查和修改。

### Step 5：处理图表

优先记录论文原图、主结果表、消融图、关键公式。可以尝试自动提取，但不能强行使用低质量图片。

如果环境允许，生成并运行：

```bash
python scripts/extract_pdf_assets.py path/to/paper.pdf docs/<domain_name>/<paper_name>/paper-to-ppt/assets/extracted
```

推荐依赖：

```bash
pip install pymupdf pillow
```

如果自动提取失败或裁剪不准确，必须在 `images_needed.md` 中列出需要手动截图的图表。

图表处理原则：

- 不猜测图中看不清的数值。
- 不重新绘制没有可靠数据来源的结果图。
- 公式无法识别时标注 `待核实`。
- 大表格应在 `images_needed.md` 中说明建议裁剪的关键行列。
- 多图、多表应说明优先级，不要默认全部放入同一页。

### Step 6：生成 `images_needed.md`

使用 `templates/images_needed_template.md`。

每个图表都要说明：

- 用在哪一页。
- 来自 PDF 哪一页 / 哪个 Figure / Table / Equation。
- 为什么需要。
- 是否已提取成功。
- 如果失败，用户应该如何手动截图并保存。

### Step 7：生成 `speaker_notes.md`

使用 `templates/speaker_notes_template.md`。

要求：

- 每页 80-180 字左右。
- 方法页可更长，但尽量不超过 250 字。
- 口语化中文。
- 包含转场句。
- 不确定内容说明“这里需要进一步核实”。
- 不要把论文原文大段翻译成讲稿。

### Step 8：生成 `review_checklist.md`

使用 `templates/review_checklist_template.md`。

必须检查：

- PDF 是否完整读取。
- 是否有编造内容。
- 每个关键结论是否有 source_reference。
- `slides_plan.md` 每页是否只有一个核心观点。
- 页数是否适合 10-15 分钟汇报。
- 图表需求是否列入 `images_needed.md`。
- 缺图是否有清晰的手动截图说明。
- 讲稿是否覆盖每页并包含转场句。
- 待核实内容是否集中列出。

## 页面规划风格要求

- 学术、简洁、清晰。
- 标题使用观点句。
- bullet 少而短。
- 方法页规划流程图或模块图。
- 实验页突出关键对比。
- 结论页包含贡献、局限和启发。
- 不要把论文原文大段翻译进页面内容。
- 对多图多表页面，应在 `visual_suggestion` 中明确：放大单图、两图对比、多面板、拆页或放入附录。

## 完成时回复用户

完成后只简要列出：

```text
已生成：
- paper_summary.md
- slides_plan.md
- images_needed.md
- speaker_notes.md
- review_checklist.md

需要你手动补充：
- [如有缺图，列出 item_id]

主要风险：
- [如有 PDF 读取不完整或待核实内容，列出]
```
