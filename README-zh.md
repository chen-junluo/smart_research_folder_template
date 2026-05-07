# smart_research_folder_template
[English README](README.md)

一个轻量的 research workspace template，用来把 legacy analysis 重建成更清晰、可复用的结构。

## 这个 template 用来做什么
这个仓库是一个 mini research workspace，适合从杂乱的 legacy materials 开始的项目，比如长 `.Rmd`、旧 scripts、旧 panel、零散 writeup 文件。

它把工作默认拆成三块：

- `Archive/`：存放 legacy materials 和旧 artifacts，作为 reconstruction source
- `panel_factory/`：shared data pipeline，用来重建 reusable data artifacts
- `Projects/`：downstream research spaces，放 project-specific analysis 和 writeup

## 核心思路
这个 template 围绕一条结构规则组织：

- 把 panel 理解成 `intermediate + features -> panel`

不要反复在一个大表上持续 mutate，而是把三层分开：

- `intermediate`：可复用的 base tables
- `features`：compact keyed feature tables
- `panel`：通过 late merge 组装出的 final panel

这样做有几个直接好处：

- 同一个 intermediate 可以服务多个 features
- 同一个 feature table 可以服务多个 panels 或 projects
- project-specific logic 不会混进 shared pipeline
- 可以逐步迁移 legacy workflow，不需要一开始就全量重写

## 仓库结构
```text
smart_research_folder_template/
├── Archive/
├── panel_factory/
│   ├── data/
│   ├── documents/
│   ├── notebooks/
│   └── src/
│       ├── features/
│       ├── panels/
│       └── utils/
└── Projects/
    └── project_template_IT_investment/
        ├── 202405 ICIS/
        │   ├── analysis/
        │   │   ├── R/
        │   │   ├── Stata/
        │   │   ├── finalize/
        │   │   └── outputs/
        │   └── writeup/
        │       ├── IT Investment - 202405 ICIS - WriteUp.md
        │       └── submitted version/
        ├── 202501 MISQ/
        ├── 202506 ISR/
        ├── 202601 AMJ/
        └── dashboard/
```

## 使用方式
1. 先把 legacy materials、旧 scripts、旧 outputs 放进 `Archive/`。
2. inventory 哪些内容应该沉淀成 reusable pipeline logic。
3. 在 `panel_factory/` 里重建 shared data construction。
4. 把 regressions、tables、figures、manuscript work 留在 `Projects/`。
5. 从 minimal runnable structure 开始,逐步扩展。

## 保持 fork 同步

如果你 fork 了这个 template，可以同步上游的 `CLAUDE.md` 更新，同时保留你自己的规则。

### 首次设置

```bash
# 添加 upstream remote
git remote add upstream https://github.com/your-username/smart_research_folder_template.git
```

### 同步 CLAUDE.md 文件

```bash
# 拉取最新的 upstream 规则
./scripts/sync-claude-md.sh

# 检查变更
git diff

# 如果满意就提交
git add .
git commit -m "Sync CLAUDE.md from upstream"
```

### 工作原理

每个 `CLAUDE.md` 分为两部分：
- `## User-Specific Rules` **之前**：upstream 规则（会被更新）
- `## User-Specific Rules` **之后**：你的自定义规则（会被保留）

在 marker 下方添加你的项目特定规则：

```markdown
## User-Specific Rules

- 用 `polars` 而不是 `pandas`
- 所有回归用 `fixest` 包
- 图表输出到 `output/figures/`
```

详见 [`scripts/README.md`](scripts/README.md)。

## 简短 prompt use case
当你希望 Claude 把一个 legacy research workflow 重构成当前这个 Smart Research Folder 结构时，可以直接用下面这个模板。

模板：

```text
请先阅读这些文件：
- `CLAUDE.md`：workspace-level 的任务路由和边界
- `Archive/CLAUDE.md`：数字化转型 / reconstruction workflow
- `panel_factory/CLAUDE.md`：shared pipeline 规则
- `panel_factory/documents/naming_conventions.md`：builders、artifacts、variables 的命名规则
- `Projects/CLAUDE.md`：downstream project 规则

最后，帮我进行数字化转型，转型成符合当前这个 Smart Research Folder 的运作模式。
```

这些文件分别是什么：

- `CLAUDE.md`：告诉 Claude 整个 workspace 里 `Archive/`、`panel_factory/`、`Projects/` 分别负责什么
- `Archive/CLAUDE.md`：告诉 Claude 遇到数字化转型、reconstruction、legacy workflow 拆解时该怎么做
- `panel_factory/CLAUDE.md`：告诉 Claude 怎样重建 reusable `intermediate`、`feature`、`panel`
- `panel_factory/documents/naming_conventions.md`：承接已经沉淀到 `documents/` 里的命名规则
- `Projects/CLAUDE.md`：告诉 Claude downstream analysis 和 writeup 应该如何与 shared pipeline 分离

## 当前自带的 placeholder
这个 template 目前带了几类最小占位文件：

- `panel_factory/src/panels/build_example_intermediate.py`
- `panel_factory/src/features/build_example_feature.py`
- `panel_factory/src/panels/build_example_panel.py`
- `panel_factory/src/utils/paths.py`
- `Projects/project_template_IT_investment/dashboard/todo.md`
- `Projects/project_template_IT_investment/dashboard/decisions.md`

这些文件故意保持极简。它们的作用是给真实研究项目提供一个可改造的起点。

## 设计原则
- 不要直接覆盖 legacy files。
- 先尊重已有 artifact names、merge keys、output boundaries。
- reusable logic 尽量上移到 `panel_factory/`。
- project-specific analysis 留在 `Projects/`。
- 先恢复 minimal runnable workflow，再做抽象和优化。

## 适合谁用
如果你符合下面的场景，这个 template 会比较合适：

- 接手了很难复用的旧 empirical workflow
- 想把 shared data construction 和 project analysis 分开
- 需要一个 AI-friendly folder structure 来做 iterative reconstruction
- 想从一个紧凑的 starting point 开始，而不是上来就用很重的 framework

## License
MIT
