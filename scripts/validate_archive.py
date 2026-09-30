#!/usr/bin/env python3
"""
validate_archive.py — 校验单份人物档案是否符合模板规范。

用法:
  python validate_archive.py path/to/archive.md
  python validate_archive.py path/to/archive.md --strict

输出:
  通过: exit 0, 打印 "OK"
  失败: exit 1, 打印所有偏差

检查项:
  1. 11 节结构齐（不缺不多）
  2. 章节顺序与模板一致
  3. 标题级别全为 ##
  4. frontmatter 无 author: ChatGPT 残留
  5. 无非模板章节
  6. 无破折号
  7. 无商业黑话
  8. 无模型路标词
  9. 无借喻清单词
  10. frontmatter 含必填字段
"""
import re
import sys
import argparse
from pathlib import Path

REQUIRED_SECTIONS = [
    "执行摘要",
    "关系网络",
    "时间线与主要作品/言论",
    "核心价值观",
    "思维模式",
    "方法论",
    "创作如何变成影响",
    "争议与风险点",
    "可信度与信息差异",
    "可操作建议",
    "主要参考来源",
]

PROHIBITED_DASHES = ["——", "—", "–"]

BUSINESS_JARGON = [
    "闭环", "能力沉淀", "赋能", "抓手", "底层逻辑",
    "内容矩阵", "拉通", "复利", "范本", "范式",
]

MODEL_BOILERPLATE = [
    "值得注意的是", "本质上", "由此可见",
    "从某种意义上说", "总之", "总体而言",
]

METAPHOR_WORDS = ["仓库", "抽屉", "温度", "坍塌", "浪潮", "钥匙", "底座"]

REQUIRED_FRONTMATTER = ["title", "type", "description", "tags", "created", "updated"]


def parse_frontmatter(content: str) -> dict:
    """Simple YAML frontmatter parser (no external deps)."""
    if not content.startswith("---"):
        return {}
    end = content.find("\n---", 3)
    if end == -1:
        return {}
    block = content[3:end].strip()
    result = {}
    for line in block.split("\n"):
        if ":" in line and not line.strip().startswith("-"):
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip()
    return result


def extract_body(content: str) -> str:
    """Strip frontmatter."""
    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end != -1:
            return content[end + 4:]
    return content


def find_sections(body: str) -> list:
    """Return list of (heading_level, section_name) for ## and # headings."""
    sections = []
    for m in re.finditer(r"^(#{1,3})\s+(.+)$", body, re.MULTILINE):
        level = m.group(1)
        name = m.group(2).strip()
        sections.append((level, name))
    return sections


def validate(path: str, strict: bool = False) -> list:
    """Run all checks, return list of issues."""
    issues = []
    p = Path(path)
    if not p.exists():
        return [f"文件不存在: {path}"]
    
    content = p.read_text(encoding="utf-8")
    
    # 1. Frontmatter check
    fm = parse_frontmatter(content)
    if not fm:
        issues.append("缺少 frontmatter")
    else:
        missing = [f for f in REQUIRED_FRONTMATTER if f not in fm]
        if missing:
            issues.append(f"frontmatter 缺少必填字段: {missing}")
        if fm.get("author", "").lower() == "chatgpt":
            issues.append("frontmatter 有 author: ChatGPT 残留（模板红线禁止）")
    
    # 2. Section structure
    body = extract_body(content)
    sections = find_sections(body)
    required_names = []
    for level, name in sections:
        if name in REQUIRED_SECTIONS:
            required_names.append((name, level))
    
    # 2a. Missing sections
    present = {n for n, _ in required_names}
    missing = [s for s in REQUIRED_SECTIONS if s not in present]
    if missing:
        issues.append(f"缺少章节: {missing}")
    
    # 2b. Section order
    if len(required_names) == len(REQUIRED_SECTIONS):
        order_ok = required_names == sorted(
            required_names, key=lambda x: REQUIRED_SECTIONS.index(x[0])
        )
        if not order_ok:
            issues.append("章节顺序与模板不一致")
    
    # 2c. Heading level
    bad_level = [(n, l) for n, l in required_names if l != "##"]
    if bad_level:
        issues.append(f"标题级别错误（应为 ##）: {bad_level}")
    
    # 2d. Non-template sections
    non_req = [
        n for l, n in sections
        if l == "##" and n not in REQUIRED_SECTIONS
    ]
    if non_req:
        issues.append(f"存在非模板章节: {non_req}")
    
    # 3. Prohibited dashes (excluding frontmatter)
    for dash in PROHIBITED_DASHES:
        if dash in body:
            # Skip dashes inside quotes (verbatim quotes are allowed)
            issues.append(f"发现禁用破折号: {dash}")
            break
    
    # 4. Business jargon
    for w in BUSINESS_JARGON:
        if w in body:
            issues.append(f"发现商业黑话: {w}")
    
    # 5. Model boilerplate
    for w in MODEL_BOILERPLATE:
        if w in body:
            issues.append(f"发现模型路标词: {w}")
    
    # 6. Metaphor words (careful: 仓库 in Obsidian context is allowed)
    # Only flag as warning, not error
    metaphor_hits = [w for w in METAPHOR_WORDS if w in body]
    if strict and metaphor_hits:
        issues.append(f"[strict] 发现借喻词（需人工确认是否为字面用法）: {metaphor_hits}")
    
    return issues


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="档案 markdown 路径")
    parser.add_argument("--strict", action="store_true", help="严格模式：借喻词也报错")
    args = parser.parse_args()
    
    issues = validate(args.path, strict=args.strict)
    if not issues:
        print(f"OK: {args.path}")
        sys.exit(0)
    else:
        print(f"FAIL: {args.path}")
        for i in issues:
            print(f"  - {i}")
        sys.exit(1)


if __name__ == "__main__":
    main()
