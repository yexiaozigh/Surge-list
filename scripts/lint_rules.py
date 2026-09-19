#!/usr/bin/env python3
"""Read-only structural lint for the repository's Surge rule-set files."""

from __future__ import annotations

import ipaddress
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
DOMAIN_TYPES = {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD"}
CIDR_TYPES = {"IP-CIDR", "IP-CIDR6"}
ALLOWED_TYPES = DOMAIN_TYPES | CIDR_TYPES
GLUED_TYPE = re.compile(r"(?:DOMAIN(?:-SUFFIX|-KEYWORD)?|IP-CIDR6?)\s*,", re.I)


def lint_file(path: Path) -> list[str]:
    errors: list[str] = []
    raw = path.read_bytes()
    if raw and not raw.endswith(b"\n"):
        errors.append(f"{path.name}: 文件末尾缺少换行")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return errors + [f"{path.name}: 不是有效UTF-8"]

    seen: dict[str, int] = {}
    for number, original in enumerate(text.splitlines(), 1):
        line = original.strip()
        if not line or line.startswith(("#", ";")):
            continue
        if line in seen:
            errors.append(f"{path.name}:{number}: 与第{seen[line]}行完全重复")
        else:
            seen[line] = number

        fields = [field.strip() for field in line.split(",")]
        kind = fields[0] if fields else ""
        if kind not in ALLOWED_TYPES:
            errors.append(f"{path.name}:{number}: 非法规则类型 {kind or '<空>'}")
            continue
        remainder = line.split(",", 1)[1] if "," in line else ""
        if GLUED_TYPE.search(remainder):
            errors.append(f"{path.name}:{number}: 疑似两条规则意外粘连")
        if len(fields) != 2 or not fields[1]:
            errors.append(f"{path.name}:{number}: 规则必须包含类型和一个非空匹配项")
            continue
        value = fields[1]
        if any(character.isspace() for character in value):
            errors.append(f"{path.name}:{number}: 匹配项包含空白字符")
        if kind in CIDR_TYPES:
            try:
                network = ipaddress.ip_network(value, strict=False)
                expected = 6 if kind == "IP-CIDR6" else 4
                if network.version != expected:
                    raise ValueError
            except ValueError:
                errors.append(f"{path.name}:{number}: {kind}地址无效")
    return errors


def main() -> int:
    paths = sorted(ROOT.glob("*.list"))
    if not paths:
        print("未找到.list文件", file=sys.stderr)
        return 1
    errors = [error for path in paths for error in lint_file(path)]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"规则检查通过：{len(paths)}个文件。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
