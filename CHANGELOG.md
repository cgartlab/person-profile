# CHANGELOG.md

## [0.1.1] - 2026-09-30

### Fixed
- 移除 frontmatter 的 `metadata.hermes` 平台耦合块，只保留标准 name/description/version/author/license
- `delegate_task` 硬编码工具名改为能力级描述（用当前 harness 的 subagent / 委派工具），解决跨 harness 可移植性
- 移除对 3 个不存在 skill 的引用（`person-profile-research` / `grounded-citations` / `concept-synthesis`），「相关技能」与「不用于」章节同步更新

## [0.1.0] - 2026-09-30

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
- 11 节结构基于 27 份高质量档案实践提炼
- 5 级证据分级独立于常见 3 级方案
- 反例必须取自档案已有材料（禁止网上现找）
- 抓不到就写「未取得」，绝不构造 URL
- 章节标题必须 `##` 级别
- 禁商业黑话 + 禁模型路标词 + 禁借喻清单 + 禁破折号
