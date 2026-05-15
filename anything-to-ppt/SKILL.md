---
name: anything-to-ppt
description: 将指定内容、文件或资料文件夹整理成可检查、可修改、可交接的演示文稿中间产物。适用于论文汇报、项目展示、产品介绍、培训、复盘、方案汇报等场景；只负责阅读资料、总结事实、规划叙事、整理图表需求和讲稿，不直接生成最终 PPT 文件。
---

# anything-to-ppt

把用户指定的内容、单个文件或资料文件夹，转换为可检查、可修改、可交接的 PPT 制作中间产物。

本 skill 的完成条件是生成标准 handoff 文件，而不是生成最终 `.pptx` 文件。最终 PPT 应交给 `pptx` skill 根据 `slides_plan.md`、`images_needed.md`、`speaker_notes.md` 和素材目录生成。

默认目标：

- 10-15 分钟汇报
- 8-12 页演示结构，除非用户指定页数
- 简体中文为主，关键术语、产品名、模型名、项目名保留原文
- 每页只表达一个核心观点
- 少文字，多图示
- 不编造来源材料中没有的信息、数字、结果、图表或结论
- 所有中间文件可检查、可修改

## 能力边界

本 skill 负责：

1. 读取用户指定的内容、文件或资料文件夹。
2. 判断资料可读性、完整性和可信度。
3. 生成事实层总结文件 `summary.md`。
4. 将资料逻辑转换成适合演示的故事线。
5. 生成清晰的页面规划 `slides_plan.md`。
6. 整理需要使用、补充、截图、重绘或生成的视觉素材需求 `images_needed.md`。
7. 生成逐页讲稿 `speaker_notes.md`。
8. 生成中间产物质量检查清单 `review_checklist.md`。
9. 创建素材目录 `assets/extracted/`、`assets/manual/`、`assets/generated/`。

本 skill 不负责：

- 直接创建最终演示文稿文件。
- 直接套用 PPT 模板文件。
- 直接编辑 Office 文件。
- 在资料不可读、缺少来源或数值不清时猜测内容。

如果用户要求最终制作 PPT，应先完成本 skill 的中间文件，再交给 `pptx` skill 生成或编辑最终 `.pptx`。

## 输入

用户可以提供：

```text
/anything-to-ppt path/to/source-file-or-folder
```

可接受的资料类型取决于当前环境可读能力，包括但不限于：

```text
PDF / Markdown / TXT / HTML / DOCX / PPTX / XLSX / CSV / images / source folder / pasted text / mixed materials
```

可选参数：

```text
--slides 8|10|12|15
--minutes 5|10|15|20
--focus balanced|background|method|results|product|project|training|decision|sales|review
--audience "研一组会" | "项目评审" | "客户路演" | "内部培训"
--style "学术简洁" | "产品展示" | "项目复盘" | "手绘风"
--language zh|en|auto
```

默认：

```yaml
slides: 8-12
minutes: 10-15
focus: balanced
audience: 由资料和用户指令推断；不确定则标注待确认
language: 简体中文
aspect_ratio: 16:9
```

## 输出目录

从输入路径推导：

- `source_domain`：输入文件所在上一级目录名，或输入文件夹名
- `source_name`：输入文件名去掉扩展名后转为 lowercase kebab-case；输入为文件夹时使用文件夹名

输出目录：

```text
docs/<source_domain>/<source_name>/anything-to-ppt/
```

必须生成：

```text
summary.md
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

> 兼容性：如果处理的是旧版 `paper-to-ppt` 工作流，可以额外生成或保留 `paper_summary.md`，但新的标准事实总结文件名是 `summary.md`。

## 强制规则

1. 先读资料，再总结事实，再规划演示。
2. 不允许编造来源材料中没有的内容、实验结果、图表、公式、时间线、客户反馈或业务数字。
3. 不确定内容必须标注 `待核实`。
4. 资料无法完整读取时，必须在 `summary.md` 和 `review_checklist.md` 中说明。
5. 所有关键结论、数字、方法细节、图表、截图、引用都必须有 `source_reference`。
6. 每页规划必须有一个 `key_message`。
7. 页面标题必须是观点式标题，不要机械使用 `Background`、`Method`、`Result`、`Conclusion` 这类小节名，除非用户明确要求。
8. 视觉页必须规划合适的图示、流程、架构、截图、表格、对比图或占位符。
9. 大表格、大截图、大图不要硬塞一页；应裁剪、拆页或移入附录。
10. 如果无法自动提取素材，必须在 `images_needed.md` 中告诉用户需要手动补哪些素材。
11. 所有中间文件必须可检查、可修改。
12. `slides_plan.md` 不得包含未经资料支持的新结论。

## 工作流

### Step 0：初始化

1. 确认输入路径或用户提供内容存在。
2. 创建输出目录和子目录。
3. 记录输入资料清单。
4. 如果缺少读取某类文件的能力，继续处理可读部分，并在 `summary.md` 和 `review_checklist.md` 标注限制。

推荐目录创建命令：

```bash
mkdir -p docs/<source_domain>/<source_name>/anything-to-ppt/{assets/extracted,assets/manual,assets/generated,scripts}
```

### Step 1：读取资料

完整读取可访问资料，至少检查：

```yaml
source_read_status:
  input_path:
  source_type:
  files_found:
  readable_files:
  unreadable_files:
  has_images:
  has_tables:
  has_charts:
  has_code_or_formulas:
  warnings:
```

如果资料读取不完整，继续生成可用部分，但必须显式标注风险。

### Step 2：生成 `summary.md`

`summary.md` 是事实层文件，不是页面大纲。

必须包含：

```yaml
basic_info:
  topic:
  source_type:
  audience:
  goal:
  requested_constraints:
source_inventory:
  - file/path/content summary/read status
confirmed_facts:
  - claim + source_reference
key_entities:
  - person/project/product/model/dataset/customer/metric/etc.
main_story_material:
  problem_or_context:
  current_state:
  proposed_solution_or_core_idea:
  evidence_or_support:
  implications_or_next_steps:
visual_inventory:
  figures:
  tables:
  screenshots:
  diagrams:
  charts:
limitations_and_risks:
open_questions:
```

要求：

- 只记录能从资料中确认的内容。
- 每个重要内容都带 `source_reference`。
- 不能把自己的推测写成资料结论。
- 对于论文资料，可保留论文式字段，如研究问题、贡献、方法、公式、实验、结果、局限。
- 对于项目/产品/业务资料，应改用项目目标、用户痛点、方案、进展、证据、风险、下一步等字段。

### Step 3：生成演示故事线

根据资料类型选择叙事结构，不要默认假设是论文。

通用结构：

```text
听众为什么要关心
→ 当前背景 / 问题 / 机会是什么
→ 资料中的核心观点或方案是什么
→ 有哪些证据、进展、数据或案例支持
→ 还存在什么风险、限制或待确认项
→ 希望听众记住什么 / 决策什么 / 下一步做什么
```

论文汇报可使用：

```text
为什么这个问题重要
→ 现有方法卡在哪里
→ 作者的核心洞察是什么
→ 方法如何实现这个洞察
→ 实验证据是否支持主张
→ 贡献、局限与启发是什么
```

项目展示可使用：

```text
项目目标
→ 现状与挑战
→ 方案与架构
→ 当前进展
→ 关键结果 / demo / 证据
→ 风险与计划
→ 需要的支持或决策
```

产品/方案汇报可使用：

```text
用户痛点
→ 市场或业务背景
→ 方案价值主张
→ 核心功能 / 流程
→ 证据 / 案例 / 对比
→ 落地计划
→ Call to action
```

### Step 4：生成 `slides_plan.md`

`slides_plan.md` 是后续制作演示文稿的核心交接文件。生成完成后应允许用户检查和修改。

文件开头必须包含全局字段：

```yaml
deck_title:
deck_theme:        # 例如 paper presentation / project update / product pitch / training / review
audience:
language:
tone:
slide_count:
source_summary: summary.md
```

每页必须包含：

```yaml
slide_number:
title:
key_message:
bullet_points:
visual_suggestion:
visual_assets:
speaker_note:
source_reference:
status: ready|needs_manual_asset|needs_verification
```

规划原则：

- 标题写成观点句。
- bullet 少而短。
- 每页只有一个核心观点。
- `visual_suggestion` 要说明使用原始图、截图、表格、流程图、架构图、对比图、概念图、占位符或生成图。
- 对多图多表页面，应明确：放大单图、两图对比、多面板、拆页或附录。
- 不要把资料原文大段复制进页面内容。

### Step 5：处理视觉素材

优先记录用户资料中的原图、截图、主表、关键流程、架构图、结果图、关键公式或产品界面。

如果环境允许，可以尝试自动提取素材并保存到：

```text
assets/extracted/
```

若需要重新绘制概念图、流程图、示意图、图标或背景素材，保存到：

```text
assets/generated/
```

若需要用户手动截图、裁剪、导出或补充素材，在 `images_needed.md` 中列出，并要求保存到：

```text
assets/manual/
```

素材处理原则：

- 不猜测图中看不清的数值。
- 不重新绘制没有可靠数据来源的结果图。
- 公式、数据、客户信息无法识别时标注 `待核实`。
- 大表格应说明建议裁剪的关键行列。
- 多图、多表应说明优先级，不要默认全部放入同一页。

### Step 6：生成 `images_needed.md`

每个视觉素材都要说明：

```yaml
item_id:
used_on_slide:
source_reference:
asset_type: figure|table|screenshot|diagram|chart|formula|icon|background|placeholder
reason:
priority: high|medium|low
extraction_status: ready|need_manual_crop|need_generated|failed|not_available
current_file:
manual_instruction:
```

手动补图提示格式：

```text
Missing visual: <source_reference>
Save as assets/manual/<item_id>.png
Suggested crop: <what to crop>
Used on slide: <slide_number>
```

中文项目可写成：

```text
待补图：<source_reference>
请保存为 assets/manual/<item_id>.png
建议裁剪：<what to crop>
用于第 <slide_number> 页
```

### Step 7：生成 `speaker_notes.md`

要求：

- 每页 80-180 字左右。
- 复杂方法页、项目方案页或培训页可更长，但尽量不超过 250 字。
- 口语化中文，除非用户要求英文。
- 包含转场句。
- 不确定内容说明“这里需要进一步核实”。
- 不要把来源资料原文大段翻译成讲稿。

### Step 8：生成 `review_checklist.md`

必须检查：

- 资料是否完整读取。
- 是否有编造内容。
- 每个关键结论是否有 `source_reference`。
- `slides_plan.md` 每页是否只有一个核心观点。
- 页数是否适合目标时长。
- 图表、截图、流程图或生成图需求是否列入 `images_needed.md`。
- 缺图是否有清晰的手动补充说明。
- 讲稿是否覆盖每页并包含转场句。
- 待核实内容是否集中列出。
- 是否适合交给 `pptx` skill 继续生成最终 PPT。

## 完成时回复用户

完成后只简要列出：

```text
已生成：
- summary.md
- slides_plan.md
- images_needed.md
- speaker_notes.md
- review_checklist.md
- assets/extracted/
- assets/manual/
- assets/generated/

需要你手动补充：
- [如有缺图，列出 item_id]

主要风险：
- [如有资料读取不完整或待核实内容，列出]
```
