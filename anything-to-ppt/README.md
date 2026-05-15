# paper-to-ppt skill

这是一个组合型 Claude Code skill，用于把论文 PDF 转成可检查、可修改的学术汇报中间产物。

安装：

```bash
mkdir -p .claude/skills
cp -r paper-to-ppt .claude/skills/
```

使用：

```text
/paper-to-ppt path/to/paper.pdf
```

核心思想：

- `SKILL.md` 只负责调度和强约束。
- `templates/` 负责标准中间产物格式。
- `scripts/` 放可选辅助脚本。
- 本 skill 的完成条件是生成中间文档：`paper_summary.md`、`slides_plan.md`、`images_needed.md`、`speaker_notes.md`、`review_checklist.md`。
- 后续制作演示文稿时，以这些中间文件作为交接材料。
