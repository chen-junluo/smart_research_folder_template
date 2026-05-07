# CLAUDE.md

- `panel_factory/` 是 shared data pipeline，不是 project-specific analysis space
- 核心职责：从 raw 中，稳定地重建 reusable intermediate、features、final panels
- 代码来源听从用户指示，可以用 `Archive/` 重建，也可以根据自然语言指令

---
## 1. Working rules

- Prioritize consistency with the current notebook pipeline before improving logic
- Treat existing intermediate artifact names as contracts during the first migration pass
- Preserve write/read CSV boundaries when they affect downstream behavior
- Do not rename columns, merge keys, or staged output files unless all downstream consumers are updated together
- Keep raw data read-only

---
## 2. 核心概念与架构

- 主要逻辑：`raw data` → `feature tables` → `final panels`
  - panel 的构建，不是把所有逻辑都堆在一个大表上反复改
  - 更合适的方式：在某个 `intermediate` base table 上，late merge 多个 compact features，最后形成 panel
- 内部文件架构：
  - `data/raw/`：原始数据，只读
  - `data/features/`：生成的 feature 表，以及部分重要 intermediate
  - `data/panels/`：最终 panel 数据
  - `src/features/`：feature 生成脚本
  - `src/panels/`：panel 聚合脚本
  - `src/utils/`：shared utilities，例如 `paths`、registry、I/O helpers
  - `documents/`：可选参考文档
    - 作用：减少重复阅读、节省 token、方便复查
    - 不是必须层，也不是 rule source
    - 规则与协作方式以 `CLAUDE.md` 为准
    - 如果 `documents/` 与 `CLAUDE.md` 不一致，应优先修正或忽略 `documents/`
    - 当前默认参考：`documents/features_registry.md`、`documents/pipeline_dependency_table.md`、`documents/naming_conventions.md`
    - 如需修改或沉淀，不仅要更新对应 `documents/`，也要在合适层级的 `CLAUDE.md` 中补充 reference
  - `notebooks/`：dashboard-style orchestration，供用户手动运行 pipeline，调用 `src/` 下的各类 Python 脚本
    - 不要默认把 notebooks 当作一次性实验文件
    - 不要在未经说明的情况下把 notebook 工作流改写成别的交互方式

---
## 3. 写新代码时的默认判断

- 如果要加的是 reusable variable，先判断它是否应该成为一个独立 feature table
- 如果某段逻辑只是某个 project 的临时分析需求，不要直接写进 `panel_factory/`
- 如果当前目标只是组装一个 panel，不要顺手把 feature generation 也塞进 panel builder
- 如果已有 intermediate 或 feature 已能支持当前任务，直接复用，不要重复造轮子
- 涉及 artifact 依赖关系时，优先参考 `documents/pipeline_dependency_table.md`
- 涉及 `feature` 是否已存在、是否应复用时，优先参考 `documents/features_registry.md`

---
---
## User-Specific Rules

<!-- 在此添加你的 panel_factory 特定规则 -->

