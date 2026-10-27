#!/usr/bin/env python3
"""Dependency-free static contract checks for doubao-talkstyle. Not an LLM-behavior test."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = []

def check(condition, message):
    if not condition:
        errors.append(message)

def read(path):
    target = ROOT / path
    check(target.is_file(), f"missing file: {path}")
    return target.read_text(encoding="utf-8") if target.is_file() else ""

skill = read("SKILL.md")
lib = read("references/phrase-library.md")
read("references/style-guide.md")
read("references/humor-patterns.md")
read("references/examples.md")
read("docs/specs/doubao-talkstyle-enhancement-spec.md")
suite_raw = read("tests/test-cases.json")
check(skill.startswith("---\n"), "missing YAML front matter")
fm = skill.split("---", 2)
check(len(fm) > 2 and "name: doubao-talkstyle" in fm[1] and "description:" in fm[1], "front matter incomplete")
for p in set(re.findall(r"references/[\w-]+\.md", skill)):
    read(p)
check(len(set(re.findall(r"references/[\w-]+\.md", skill))) >= 4, "references links incomplete")
for word in ("默认 3", "默认 2", "智能", "上下文", "定向", "任务忠实度", "不自动触发", "原句"):
    check(word in skill, f"missing skill rule marker: {word}")
patterns = re.findall(r"(?m)^\d+\. \*\*[^\n]+", lib)
check(len(patterns) == 21, f"legacy sentence templates not fully preserved: {len(patterns)}")
for phrase in ("我没有身份证，所以我敢说话", "惹到我你算是踢到棉花了", "千对万对，都是我没错", "再问就不是这个价格了"):
    check(phrase in lib, f"missing legacy phrase: {phrase}")
try:
    suite = json.loads(suite_raw)
except json.JSONDecodeError as exc:
    errors.append(f"invalid tests JSON: {exc}")
    suite = {}
cases = suite.get("cases", [])
check(len(cases) == 20, f"expected 20 cases, got {len(cases)}")
ids = [x.get("case_id") for x in cases if isinstance(x, dict)]
check(ids == [f"T{i:02}" for i in range(1, 21)], "expected unique sequential T01-T20 IDs")
for case in cases:
    if not isinstance(case, dict):
        errors.append("case is not object")
        continue
    for required in ("case_id", "task_type", "input", "target", "humor", "roast", "context", "expected_properties", "forbidden_properties"):
        check(required in case, f"{case.get('case_id')} missing {required}")
    check(isinstance(case.get("humor"), int) and 1 <= case["humor"] <= 5, f"{case.get('case_id')} invalid humor")
    check(isinstance(case.get("roast"), int) and 1 <= case["roast"] <= 5, f"{case.get('case_id')} invalid roast")
    check(isinstance(case.get("context"), list), f"{case.get('case_id')} invalid context")
    check(isinstance(case.get("expected_properties"), list) and len(case["expected_properties"]) > 0, f"{case.get('case_id')} missing expectations")
    check(isinstance(case.get("forbidden_properties"), list), f"{case.get('case_id')} missing forbidden properties")

if errors:
    print(f"FAIL: {len(errors)} static check(s)")
    for error in errors:
        print(" -", error)
    sys.exit(1)
print(f"PASS: Skill front matter, refs, default settings, 21 legacy templates, core phrases and {len(cases)} regression cases")
print("NOTE: This script does NOT run or grade an LLM. Behavioral evaluation remains required.")
