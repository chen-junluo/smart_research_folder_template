# CLAUDE.md

- 这是一个科研项目 workspace，不是单一项目仓库。当前 workspace 主要包含三类内容：
  - `Archive/`：legacy materials。这里放旧 analysis scripts、旧 panel、旧 tables / figures、旧 writeup。主要用于参考，不应默认视为当前主流程。
  - `panel_factory/`：shared data pipeline。用于从 raw data 生成 features，再将 features 合并为 panels。
  - `Projects/`：downstream research spaces。项目分析、回归、写作等工作原则上应建立在 `panel_factory/` 产出的数据之上。


---
## 1. 项目文件夹和架构详细介绍

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

- `projects/`
  - 这里存放具体研究项目。每个项目文件夹通常包括：项目说明、决策记录与待办、分阶段的 analysis、分阶段的 writeup
  - 这些项目文件夹是 `panel_factory/` 下游的研究工作区，不是共享数据处理框架本身。因此：
    - 项目分析代码不要与通用 pipeline 代码混淆
    - 项目特定逻辑不要随意上移到 `panel_factory/`
    - 写作材料、回归脚本、图表输出，应优先放在各自项目内部管理

- `archive/`
  - 这里是迁移前的旧架构内容和历史项目材料。
  - 用途：回溯旧逻辑、查找历史脚本或中间结果、对照迁移前后的处理方式
  - 默认规则：
    - `archive/` 不是当前主流程
    - 不要默认把 `archive/` 中的代码当作最新版本
    - 如需复用旧逻辑，应先与 `panel_factory/` 当前实现核对

---
## 2. 如果要进行reconstruction（数字化转型），workflow如下：

- reconstruction workflow
  - 第一步：归档关键文件。
    - 将关键项目文件放入 `Archive/`。
    - 重点包括：生成代码的文件、分析类文件、相关文档、旧 panel、旧输出。
    - 常见来源包括：又长又杂的 Python notebooks、旧 `.py`、旧 `.R` / `.do`、零散说明文档。
  - 第二步：AI 预处理 + 用户确认。
    - 先由 AI 读取 `Archive/` 中的关键文件，对项目尤其是 data logic 形成初步理解。
    - AI 应先按 block 切分旧文件中的逻辑，而不是要求用户手动从头拆解。
    - 然后进入用户确认环节：由用户标记或确认哪些 block 属于 `raw -> intermediate`，哪些属于 reusable `feature`，哪些属于 final `panel`。
    - 这一步的核心难点是：旧项目常常通过“在旧表后增加 columns 形成新表”的方式演化，导致 intermediate files 冗余严重。
    - 因此需要在交互中形成共识：
      - 哪些部分应保留为 base `intermediate`。
      - 哪些变量应拆成独立 `feature`。
      - 最终 panel 应如何由 `intermediate + features` 组装而成。
  - 第三步：产出执行文件与任务分派。
    - 在完成 block-level 判断后，产出一个可供后续 AI 执行的文件。
    - 根据工作量与复杂度，将任务适当拆成多个 blocks。
    - 再把这些 blocks 拆成 `N` 个执行文件，便于分派给下游 AI 并行处理。
  - 第四步：结果验收与一致性保证。
    - 需要设置专门的验收 block。
    - 如果验收发现问题，应继续修正，而不是直接交付。
    - 最终目标是确保 consistency：最终生成的 panel 与 `Archive/` 中原始项目逻辑一致，尤其要核对 merge、filter、样本边界、关键变量定义。
  - 第五步：代码重构与自动化。
    - 在数据 construction 稳定后，再整理 analysis 部分的代码。
    - 目标是参照 templates 重构现有 analysis code，使其更适合后续通过自然语言生成、修改、运行与读取结果。
  - 默认原则
    - 不要一上来就把 `Archive/` 全量重写。
    - 先恢复 minimal runnable structure，再逐步解耦。
    - 第一优先级是与原始项目保持一致，而不是先做抽象上的优雅重构。



---
## 3. 默认工作边界

除非用户明确要求，否则不要自动进行以下操作：
- 不要为了“更整洁”而重命名文件夹
- 不要自动重组 workspace 结构
- 不要随意改动 raw data
- 不要轻易修改 feature 名称、列名、merge keys、输出文件名
- 不要把 `archive/` 误当作当前生产代码
- 不要把项目内部分析逻辑直接混入 `panel_factory/`
- 不要未经说明就重写 notebook 驱动的工作方式

---
## 4. 任务定位规则

当用户提出任务时，先按下面的方式定位：
- 如果任务涉及 raw data、feature 生成、panel 构建、pipeline 工具函数，优先查看 `panel_factory/`
- 如果任务涉及回归、实证分析、表图输出、论文写作，优先查看 `projects/`
- 如果任务涉及历史版本、旧架构、迁移前逻辑，查看 `archive/`

---

## 5. 局部说明优先

如果某个子文件夹下还有自己的 `CLAUDE.md`，则该局部文件夹内的说明优先级更高。
例如在 `panel_factory/` 内工作时，应同时遵守 `panel_factory/CLAUDE.md` 的要求。
- 协作风格
  - 中文简洁描述内容，technical terms 用 English。
  - 当结构不清晰时，先列 inventory，再提 reconstruction plan。
  - 优先尊重已有 artifact names、merge keys、output boundaries，再逐步优化。