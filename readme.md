````markdown
# Paper PPT Skills

一组用于 Claude Code 的论文汇报 PPT skills

---

## Installation

### 1. 安装到 Claude Code user-level skills 目录

推荐安装到：

```text
C:\Users\<your-username>\.claude\skills
````

如果你使用的是打包好的 zip：

```powershell
Expand-Archive -Path .\paper-pptx-skills-optimized-combined.zip -DestinationPath $env:USERPROFILE -Force
```

安装后目录应类似：

```text
C:\Users\<your-username>\.claude\skills\
├── paper-to-ppt\
└── pptx\
```

检查安装结果：

```powershell
Get-ChildItem "$env:USERPROFILE\.claude\skills"
```

在 Claude Code 中运行：

```text
/skills
```

应能看到：

```text
paper-to-ppt · user
pptx · user
```

---

### 2. 安装字体

本项目默认 PPT 风格使用：

* English headings: `Kalam`
* English body: `Patrick Hand`
* Chinese fallback: `FangSong / 仿宋`
* Equations and symbols: `Cambria Math` or other math fonts

其中 `Kalam` 和 `Patrick Hand` 需要手动安装。

Windows PowerShell：

```powershell
$fontDir = "$env:LOCALAPPDATA\Microsoft\Windows\Fonts"
$downloadDir = "$env:USERPROFILE\Downloads\google-handdrawn-fonts"

New-Item -ItemType Directory -Force -Path $fontDir | Out-Null
New-Item -ItemType Directory -Force -Path $downloadDir | Out-Null

$fonts = @(
  @{
    Name = "Kalam Light (TrueType)"
    File = "Kalam-Light.ttf"
    Url  = "https://raw.githubusercontent.com/google/fonts/main/ofl/kalam/Kalam-Light.ttf"
  },
  @{
    Name = "Kalam Regular (TrueType)"
    File = "Kalam-Regular.ttf"
    Url  = "https://raw.githubusercontent.com/google/fonts/main/ofl/kalam/Kalam-Regular.ttf"
  },
  @{
    Name = "Kalam Bold (TrueType)"
    File = "Kalam-Bold.ttf"
    Url  = "https://raw.githubusercontent.com/google/fonts/main/ofl/kalam/Kalam-Bold.ttf"
  },
  @{
    Name = "Patrick Hand Regular (TrueType)"
    File = "PatrickHand-Regular.ttf"
    Url  = "https://raw.githubusercontent.com/google/fonts/main/ofl/patrickhand/PatrickHand-Regular.ttf"
  }
)

foreach ($font in $fonts) {
  $downloadPath = Join-Path $downloadDir $font.File
  $installPath = Join-Path $fontDir $font.File

  Invoke-WebRequest -Uri $font.Url -OutFile $downloadPath
  Copy-Item $downloadPath $installPath -Force

  New-ItemProperty `
    -Path "HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Fonts" `
    -Name $font.Name `
    -Value $installPath `
    -PropertyType String `
    -Force | Out-Null
}

Write-Host "Fonts installed to: $fontDir"
Write-Host "Please restart PowerPoint, Claude Code, and terminal windows."
```

检查字体：

```powershell
Get-ChildItem "$env:LOCALAPPDATA\Microsoft\Windows\Fonts" |
  Where-Object { $_.Name -match "Kalam|Patrick" } |
  Select-Object Name, FullName
```

安装字体后，请重启：

* Claude Code
* PowerPoint
* 当前终端窗口

---

### 3. Recommended Workflow

先用 `paper-to-ppt` 生成中间文档：

```text
使用 paper-to-ppt skill 处理 papers/example.pdf。
只生成中间产物，不要生成 PPT。
```

然后检查并修改：

```text
paper_summary.md
slides_plan.md
images_needed.md
speaker_notes.md
review_checklist.md
```

确认无误后，再用 `pptx` 生成 PPT：

```text
使用 pptx skill，根据当前目录已有的 paper-to-ppt 中间产物生成 report.pptx。

严格以 slides_plan.md 为页面结构来源，使用 images_needed.md 和 assets/ 处理图片，使用 speaker_notes.md 处理备注。不要重新读论文，不要重写大纲。缺图用占位，不要编造。
```

建议先生成 1-2 页样张：

```text
使用 pptx skill，先只生成 2 页样张，不要生成整套 PPT。
优先选择 1 页方法页和 1 页实验结果页。
```

确认风格后再生成完整 `report.pptx`。

---

## Acknowledgements

本项目受到以下开源项目和社区资源启发，特此感谢：

* [Max-astro/paper-reading-skills](https://github.com/Max-astro/paper-reading-skills)
  提供了面向论文阅读的 Claude Code skill 思路，尤其是分阶段阅读、结构化理解和中文论文精读流程。

* [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)
  提供了丰富的 Claude skills 参考，尤其是 document-skills 中的 `pptx` skill，对 PPTX 生成、HTML-to-PPTX、OOXML 编辑和缩略图检查流程有重要启发。

* [Google Fonts](https://fonts.google.com/)
  提供 `Kalam` 和 `Patrick Hand` 等开源字体，使 hand-drawn 风格可以更自然地用于学术汇报。

* [PyMuPDF](https://github.com/pymupdf/PyMuPDF)
  可用于 PDF 页面渲染和图像提取，是论文图表提取脚本的重要可选依赖。

感谢开源社区让这些工具、字体、思路和工作流可以被自由学习、组合和改进。


