# Changelog

本文件记录 person-profile 的所有显著变更。

格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [语义化版本 2.0.0](https://semver.org/lang/zh-CN/)。

> `0.x` 阶段：SKILL.md 的章节结构与输出格式仍可能调整，升级前请阅读对应版本的**一句话概括**。

## [0.1.1](https://github.com/cgartlab/person-profile/compare/v0.1.0...v0.1.1) - 2026-09-30
> **一句话概括**：0.1.1 是一次可移植性修复——移除与 Hermes 平台的绑定、硬编码工具名和已失效的技能引用，使 skill 能在任意 harness 上运行。**你不需要做任何事，直接升级即可。**本次变更对应 [#2](https://github.com/cgartlab/person-profile/pull/2)。

### Fixed

### Fixed
- 对使用者：skill 不再绑定单一 Agent 平台，可在任意 harness 中使用。技术细节：移除 frontmatter（技能文件开头的元数据区）里的 `metadata.hermes` 平台耦合块（Hermes 是本 skill 原先绑定的一个 Agent 平台），只保留标准 name/description/version/author/license。
- 对使用者：在不同 harness（承载 agent 运行的宿主环境）之间切换时，不再因工具名不匹配而失败。技术细节：`delegate_task`（将任务委派给子 agent 的调用）不再硬编码工具名，改为用当前 harness 的 subagent / 委派工具的能力级描述，解决跨 harness 可移植性。
- 对使用者：档案里不再出现已不存在的技能，避免打开时看到失效的相关技能链接。技术细节：移除对 3 个不存在 skill（`person-profile-research` / `grounded-citations` / `concept-synthesis`）的引用，并同步更新「相关技能」与「不用于」章节。

## [0.1.0] - 2026-09-30

> **一句话概括**：首次发布 person-profile skill，一次性提供完整骨架：11 节档案模板、7 步工作流 + 17 项验收清单、证据分级、双向链与四份校验脚本。**你不需要做任何事——这是初始版本，后续升级前请阅读每版的“一句话概括”。**

### Added
- 项目骨架：README、DESIGN、CHANGELOG
- SKILL.md：完整工作流（7 步 + 17 项验收清单）
- templates/person-archive.md：11 节完整模板
- references/：证据分级、章节设计、双向链、反例审查、引用纪律、写作规范
- scripts/validate_archive.py：单份档案校验脚本
- scripts/validate_library.py：批量校验脚本
- scripts/check_bidirectional.py：双向链完整性检查
- scripts/check_prohibitions.py：禁词与格式违规扫描
- benchmarks/：标杆档案评分标准
- references/external-references.md：吸收的 GitHub 外部参考清单

### Design Decisions
- 11 节结构基于 27 份高质量档案实践提炼（[references/chapter-rationale.md](references/chapter-rationale.md)）
- 5 级证据分级独立于常见 3 级方案（[references/evidence-grading.md](references/evidence-grading.md)）
- 反例必须取自档案已有材料（禁止网上现找）（[references/counter-example-rules.md](references/counter-example-rules.md)）
- 抓不到就写「未取得」，绝不构造 URL（[references/citation-discipline.md](references/citation-discipline.md)）
- 章节标题必须 `##` 级别（[references/chapter-rationale.md](references/chapter-rationale.md)）
- 禁商业黑话 + 禁模型路标词 + 禁借喻清单 + 禁破折号（[references/writing-style.md](references/writing-style.md)）
