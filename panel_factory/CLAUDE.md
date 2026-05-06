# panel_factory rules

Working rules:
1. Prioritize consistency with the current notebook pipeline before improving logic.
2. Treat existing intermediate artifact names as contracts during the first migration pass.
3. Preserve write/read CSV boundaries when they affect downstream behavior.
4. Do not rename columns, merge keys, or staged output files unless all downstream consumers are updated together.
5. Keep raw data read-only.

- 这个文件夹是 shared data pipeline，不是 project-specific analysis space。
- 它的核心职责是：从 raw 中，稳定地重建 reusable intermediate、features、final panels。代码的来源请听从用户指示，可以用Archive里面重建，也可以根据自然语言指令。

- `panel_factory/` 的核心概念
  - 主要的逻辑是读取 raw data -> 生成 feature tables -> 将 feature tables 合并为最终 panels。注意 panel 的构建，不是把所有逻辑都堆在一个大表上反复改。更合适的方式是：在某个 `intermediate` base table 上，late merge 多个 compact features，最后形成 panel。
  - 内部文件架构如下：
    - `data/raw/`：原始数据，只读
    - `data/features/`：生成的 feature 表，以及部分重要 intermediate
    - `data/panels/`：最终 panel 数据
    - `src/features/`：feature 生成脚本
    - `src/panels/`：panel 聚合脚本
    - `src/utils/`：shared utilities，例如 `paths`、registry、I/O helpers。
    - `documents/`：可选参考文档。作用是减少重复阅读、节省 token、方便复查。这里的内容不是必须层，也不是 rule source。规则与协作方式以 `CLAUDE.md` 为准；如果 `documents/` 与 `CLAUDE.md` 不一致，应优先修正或忽略 `documents/`。
    - `notebooks/`：用于 dashboard-style orchestration、供用户手动运行 pipeline，调用 `src/` 下的各类 Python 脚本。不要默认把 notebooks 当作一次性实验文件，也不要在未经说明的情况下把 notebook 工作流改写成别的交互方式。

- 写新代码时的默认判断
  - 如果要加的是 reusable variable，先判断它是否应该成为一个独立 feature table。
  - 如果某段逻辑只是某个 project 的临时分析需求，不要直接写进 `panel_factory/`。
  - 如果当前目标只是组装一个 panel，不要顺手把 feature generation 也塞进 panel builder。
  - 如果已有 intermediate 或 feature 已能支持当前任务，直接复用，不要重复造轮子。

- `src/` 下的命名习惯
  - 如果是 base/intermediate 大表，命名应接近 `build_xxx_intermediate.py`。
  - 如果是特征族，命名应接近 `build_xxx.py`。
  - 如果是 panel，命名应接近 `build_xxx_panel.py`。
  - 不要在 panel script 里重复生成已经可以独立生成的 feature。
  - 不要为了加一个变量，就在 full panel 上一路 mutate 出更多中间表。
  - 新变量如果能作为 compact feature 独立存在，就优先写成 feature builder。
  - panel builder 的职责应尽量收敛到：读取某个 intermediate，merge 所需 features，输出 final panel。