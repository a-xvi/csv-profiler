def basic_profile(rows: list[dict[str, str]]) -> dict:
    cols = get_columns(rows)
    report = {
        "summary": {
            "rows": len(rows),
            "columns": len(cols),
            "column_names": cols
        },
        "columns": {}
    }

    for col in cols:
        values = column_values(rows, col)
        typ = infer_type(values)
        if typ in ("int", "float"):
            report["columns"][col] = {"type": "number", "stats": numeric_stats(values)}
        else:
            report["columns"][col] = {"type": "text", "stats": text_stats(values)}

    return report

def get_columns(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return []
    return list(rows[0].keys())


MISSING = {"","na","n/a","null","none","nan"}

def is_missing(value:str | None) -> bool:
    if value is None:
        return True
    return value.strip().casefold() in MISSING

def try_float(value:str ) -> float |None:
    try:
        return float(value)
    except ValueError:
        return None
    
def infer_type(values: list[str]) -> str:
    for v in values:
        v = v.strip()
        if v and not v.isdigit() and not try_float(v):
            return "str"
    return "int" if all(v.strip() == "" or v.isdigit() for v in values) else "float"

def column_values(rows: list[dict[str, str]], col: str) -> list[str]:
    return [row.get(col,"") for row in rows]

def numeric_stats(values: list[str]) -> dict:
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)
    nums = []
    for v in usable:
        x = try_float(v)
        if x is None:
            raise ValueError(f"Non-numeric value found: {v!r}")
        nums.append(x)

    return {
        "count": len(nums),
        "missing": missing,
        "unique": len(set(nums))
    }


def text_stats(values: list[str], top_k: int = 5) -> dict:
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)

    counts = {}
    for v in usable:
        counts[v] = counts.get(v, 0) + 1

    top_items = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:top_k]
    top = [{"value": v, "count": c} for v, c in top_items]

    return {
        "count": len(usable),
        "missing": missing,
        "top": top
    }
