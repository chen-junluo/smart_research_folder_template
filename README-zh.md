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
    └── project_template/
        ├── analysis/
        ├── dashboard/
        └── writeup/
```

## 使用方式
1. 先把 legacy materials、旧 scripts、旧 outputs 放进 `Archive/`。
2. inventory 哪些内容应该沉淀成 reusable pipeline logic。
3. 在 `panel_factory/` 里重建 shared data construction。
4. 把 regressions、tables、figures、manuscript work 留在 `Projects/`。
5. 从 minimal runnable structure 开始，逐步扩展。

## 当前自带的 placeholder
这个 template 目前带了几类最小占位文件：

- `panel_factory/src/panels/build_example_intermediate.py`
- `panel_factory/src/features/build_example_feature.py`
- `panel_factory/src/panels/build_example_panel.py`
- `panel_factory/src/utils/paths.py`
- `Projects/project_template/dashboard/todo.md`
- `Projects/project_template/dashboard/decisions.md`

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
