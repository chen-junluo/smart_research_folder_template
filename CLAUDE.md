# CLAUDE.md

- 这是一个科研项目 workspace，不是单一项目仓库。当前 workspace 主要包含三类内容：
  - `Archive/`：legacy materials。这里放旧 analysis scripts、旧 panel、旧 tables / figures、旧 writeup。主要用于参考，不应默认视为当前主流程。
  - `panel_factory/`：shared data pipeline。用于从 raw data 生成 features，再将 features 合并为 panels。
  - `Projects/`：downstream research spaces。项目分析、回归、写作等工作原则上应建立在 `panel_factory/` 产出的数据之上。


---
## 1. 项目文件夹和架构详细介绍

- `panel_factory/` 的核心概念
  - 主要的逻辑是读取raw data -> 生成feature tables -> 将featur tables 合并为最终panels。注意panel 的构建，不是把所有逻辑都堆在一个大表上反复改。具体来说，是在某个 `intermediate` base table 上（intermediate也是存放在features文件夹里im的），late merge 多个 compact features，最后形成 panel。
  - 内部文件架构如下：
    - `data/raw/`：原始数据，只读
    - `data/features/`：生成的 feature 表，以及部分重要 intermediate
    - `data/panels/`：最终 panel 数据
    - `src/features/`：feature 生成脚本
    - `src/panels/`：panel 聚合脚本
    - `src/utils/`：shared utilities，例如 paths、registry、I/O helpers。
    - `documents/`：维护了项目的重要文档。主要的目的是为了减少重复工作、方便复查。包括`features_registry.md`、`raw_data_dictionary.md`。如果在工作过程中发现值得沉淀来减少token消耗/提高效率的文档，与用户讨论分析是否要沉淀。沉淀的时候要1、确定好模板；2、修改好CLAUDE.md不要有项目内不一致的地方+确保正确prompting使得能AI正确refer达到复用效果。
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
  - 原始项目的核心代码存放在 `Archive/`。代码可能会比较长，在这种情况下要步子迈小一点，确保代码identically相同先拆成符合panel_factory pipeline的样子。确保consistency。尤其注意各种merge和filter的操作，确保和原始项目一致。
  - 判断哪些内容应沉淀为 `panel_factory/` 里的 reusable pipeline。
  - 判断哪些内容属于具体 project，放进 `Projects/`。
  - 不要一上来就把 archive 全量重写。先恢复 minimal runnable structure，再逐步解耦。



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