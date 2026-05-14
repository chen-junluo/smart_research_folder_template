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

- 不要重复实现前序步骤已经完成的处理逻辑
  - 如果当前变量的生成需要依赖 raw-like source、某些 intermediate 或 feature，而这些 intermediate 或 feature 已经可以由 `src/` 下现有脚本生成，则默认优先复用已有产物
  - 当前脚本应直接使用这些已有的 intermediate 或 feature 作为输入，不要在本文件中重复生成相同产物
- 每次交付时：
  - 默认要求每个代码文件内部是完整的、`self-consistent` 的
  - 不要出现注释描述、实际逻辑、命名含义彼此不一致的情况
- 对代码注释的处理：
  - 不要删除中英夹杂的现有注释
  - 这类注释通常包含 `context`、研究过程信息或 `domain knowledge`
  - 如果代码改动改变了这些注释的含义，应更新内容，而不是直接删掉
- 我看重 canonical source clarity
  - 优先复用上游有的变量，避免重复 alias，避免 downstream 误读和缺失值污染

---
## 2. 核心概念与架构

- 主要逻辑：`raw data` → `feature tables` → `final panels`
  - panel 的构建，不要在一个 full panel 上一路追加很多变量，再输出更大的 intermediate
  - 优先保持 `intermediate`、`features`、`panel` 三层解耦
  - panel builder 的职责应尽量收敛到：读取 intermediate、merge features、写出 panel

- **Grain vs Intermediate 的区别**
  - **Grain**：从分析层面看的，即它属于哪个 level 的 panel
    - 四个核心 grain：`question`、`human_answer`、`full_answer`、`user_activity`
    - Grain 决定了 merge keys 和数据粒度
    - 例如：`human_answer` grain 的 merge keys 是 `questionURL × resp_id`
  - **Intermediate**：从数据生成角度看的，如果后续会被不断复用，那么它就是一个 Intermediate
    - Intermediate 是 base table，minimal processing
    - Feature 是 compact table，specific metrics
    - Panel 是 final table，late merge features onto intermediate
  - **命名规范**
    - Feature 文件名必须以 grain 开头：`{grain}_{feature_name}.csv`
    - Intermediate 文件名必须包含 `_intermediate` 后缀：`{grain}_intermediate.csv`
- 内部文件架构：
  - `data/raw/`：原始数据，只读
  - `data/features/`：生成的 feature 表，以及部分重要 intermediate
  - `data/panels/`：最终 panel 数据
  - `src/features/`：生成 compact feature tables
  - `src/panels/`：把 features late merge 到某个 intermediate 上，生成 final panel
  - `src/utils/`：shared utilities，例如 `paths`、registry、I/O helpers
  - `documents/`：可选参考文档
    - 作用：减少重复阅读、节省 token、方便复查
    - 不是必须层，也不是 rule source
    - 规则与协作方式以 `CLAUDE.md` 为准
    - 如果 `documents/` 与 `CLAUDE.md` 不一致，应优先修正或忽略 `documents/`
    - 当前默认参考：`documents/features_registry.md`、`documents/pipeline_dependency_table.md`
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
- 对于非生成feature的，简单的查询检索的任务，直接后台撰写代码然后告诉我结果。**如无要求，不要在本地写入py文件和报告！**


---
## 4. 每个 `build_*.py` 文件顶部默认应有简短 bullets，且保持pipeline consistency

- 强制同步规则：当新建/修任何`build_*.py` 文件的时候，必须同步更新三处：
  1. **修改 `build_*.py` 文件的 structured header，确保与实际代码逻辑一致**
  2. **使用 `scripts/update_dependency_docs.py` 更新 `documents/pipeline_dependency_table.md` 的 graph 和 table**
- Structured Header 强制要求
  - 所有 `build_*.py` 文件必须包含 structured header
  - Header 格式必须严格遵守 `documents/build_file_header_template.md` 规范
  - 修改代码逻辑时，必须同步更新 header
  - Header 中的信息必须与实际代码逻辑一致

---
## 5. 每次生成新 feature 后，默认反馈该 feature 的 descriptive statistics

- 至少包括 `min`、`max`、`mean`
- 大概告诉我这个变量的 distribution 的数值范围，让我了解这个变量分布是咋样的
- 默认补充若干 sample rows，优先看命中值为 `1` 的 case
- 注意如果 sample 爆长你不要直接输出，你简略告诉我就行保留关键要点，我只是想看是不是识别的准
- 不需要把描述性统计和 sample 什么的存成 csv，直接在对话中告诉我

---
## 6. 运行 python 脚本

- 不要直接从脚本文件路径裸调用 Python，否则可能报 `ModuleNotFoundError`
- 默认用 notebook 对应的解释器，并在 workspace 根目录下设置 `PYTHONPATH=/Users/dylanchen/Desktop/current_folder_name/panel_factory/src` 后再运行
- 例如：`PYTHONPATH=/Users/dylanchen/Desktop/current_folder_name/panel_factory/src /Users/dylanchen/miniconda3/envs/cityu/bin/python panel_factory/src/panels/build_question_panel.py`


---
---
## User-Specific Rules

<!-- 在此添加你的 panel_factory 特定规则 -->

