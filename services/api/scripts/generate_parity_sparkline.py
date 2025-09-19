import sys
import json
from pathlib import Path
from typing import List

BLOCKS = [" ", "▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]


def load_history(path: Path) -> List[dict]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    data = []
    for line in lines[-60:]:  # cap window for performance
        try:
            data.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return data


def scale(values: List[int]) -> str:
    if not values:
        return "(no data)"
    mn, mx = min(values), max(values)
    if mn == mx:
        # Flat line; choose mid block if non-zero else blank
        idx = 0 if mx == 0 else len(BLOCKS)//2
        return BLOCKS[idx] * len(values)
    span = mx - mn
    chars = []
    for v in values:
        norm = (v - mn) / span
        idx = int(round(norm * (len(BLOCKS) - 1)))
        chars.append(BLOCKS[idx])
    return ''.join(chars)


def build_sparkline(records: List[dict]) -> str:
    # Pick mismatch_total or (total_specialists - matched) if parity key present
    if not records:
        return "(no data)"
    mismatch_values = []
    for r in records:
        if 'mismatch_total' in r:
            mismatch_values.append(int(r.get('mismatch_total', 0)))
        elif 'total_specialists' in r and r.get('parity') is False:
            # Fallback heuristic
            mismatch_values.append(1)
        else:
            mismatch_values.append(0)
    spark = scale(mismatch_values)
    last = mismatch_values[-1] if mismatch_values else 0
    return f"{spark} (last={last})"


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.generate_parity_sparkline <history_jsonl_path>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    records = load_history(path)
    spark = build_sparkline(records)
    print(spark)
    return 0

if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
