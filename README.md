# smart_research_folder_template
[中文说明](README-zh.md)

A lightweight research workspace template for rebuilding legacy analysis into a cleaner, reusable structure.

## What this template is for
This repository is a mini research workspace for projects that start from messy legacy materials such as long `.Rmd` files, old scripts, old panels, and scattered writeup files.

The template separates that work into three top-level areas:

- `Archive/`: legacy materials and old artifacts kept as reconstruction source
- `panel_factory/`: shared data pipeline for rebuilding reusable data artifacts
- `Projects/`: downstream research spaces for project-specific analysis and writeup

## Core idea
The template is built around one structural rule:

- treat a panel as `intermediate + features -> panel`

Instead of repeatedly mutating one large table, the workflow keeps three layers separate:

- `intermediate`: reusable base tables
- `features`: compact keyed feature tables
- `panel`: final assembled panel created by late merges

This makes it easier to:

- reuse the same intermediate across multiple features
- reuse feature tables across multiple panels or projects
- keep project-specific logic out of the shared pipeline
- migrate legacy workflows incrementally instead of rewriting everything at once

## Repository structure
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

## How to use
1. Put legacy materials, old scripts, and old outputs into `Archive/`.
2. Inventory what should become reusable pipeline logic.
3. Rebuild shared data construction inside `panel_factory/`.
4. Keep regressions, tables, figures, and manuscript work inside `Projects/`.
5. Expand gradually from a minimal runnable structure.

## Included placeholders
This template includes lightweight placeholders for:

- `panel_factory/src/panels/build_example_intermediate.py`
- `panel_factory/src/features/build_example_feature.py`
- `panel_factory/src/panels/build_example_panel.py`
- `panel_factory/src/utils/paths.py`
- `Projects/project_template/dashboard/todo.md`
- `Projects/project_template/dashboard/decisions.md`

These files are intentionally minimal. They are starting points for adapting the structure to a real research project.

## Design principles
- Do not overwrite legacy files directly.
- Respect existing artifact names, merge keys, and output boundaries first.
- Move reusable logic upward into `panel_factory/`.
- Keep project-specific analysis inside `Projects/`.
- Recover a minimal runnable workflow before optimizing abstractions.

## Who this is for
This template is useful if you:

- inherit old empirical workflows that are hard to reuse
- want a clearer separation between shared data construction and project analysis
- need an AI-friendly folder structure for iterative reconstruction
- want a compact starting point rather than a large framework

## License
MIT
