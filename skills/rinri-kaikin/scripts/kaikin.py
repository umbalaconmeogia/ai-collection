#!/usr/bin/env python3
"""
Thống kê 皆勤 / もう少し賞 cho モーニングセミナー của 倫理法人会 từ file CSV 参加履歴情報.

Usage:
    python kaikin.py <csv_path> <month>
        month: 202609 hoặc 2026/09 hoặc 2026-09

Quy tắc:
- Buổi (session) = các giá trị distinct của cột ngày (開催日 / 開始日) trong tháng chỉ định,
  tính trên TOÀN BỘ dòng (kể cả 他単会, 非会員) để không bỏ sót buổi.
- Chỉ xét người có 区分 chứa "自単会".
- Nhận diện người theo 姓+名 (đã chuẩn hoá khoảng trắng), KHÔNG dùng 法人会員番号
  vì số đó là mức 法人, nhiều người cùng công ty dùng chung.
- Mỗi người mỗi ngày chỉ đếm 1 lần (dedupe).
- 皆勤 = dự đủ mọi buổi; もう少し賞 = vắng đúng 1 buổi.
"""
import csv
import re
import sys
from collections import defaultdict

DATE_COLS = ("開催日", "開始日")
KUBUN_COL = "区分"
OWN_MARK = "自単会"


def norm(s: str) -> str:
    """Bỏ mọi khoảng trắng (half/full-width) để so khớp tên."""
    return re.sub(r"[\s　]+", "", s or "")


def display(s: str) -> str:
    return re.sub(r"[\s　]+", " ", (s or "")).strip()


def parse_month(m: str) -> str:
    m = m.strip()
    mm = re.fullmatch(r"(\d{4})[/\-]?(\d{1,2})", m)
    if not mm:
        sys.exit(f"Tháng không hợp lệ: {m!r} (dùng 202609 hoặc 2026/09)")
    return f"{mm.group(1)}-{int(mm.group(2)):02d}"


def read_rows(path: str):
    for enc in ("utf-8-sig", "cp932"):
        try:
            with open(path, encoding=enc, newline="") as f:
                return list(csv.DictReader(f))
        except UnicodeDecodeError:
            continue
    sys.exit("Không đọc được CSV (thử utf-8-sig, cp932)")


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    path, month = sys.argv[1], parse_month(sys.argv[2])
    rows = read_rows(path)
    if not rows:
        sys.exit("CSV rỗng")

    date_col = next((c for c in DATE_COLS if c in rows[0]), None)
    if not date_col:
        sys.exit(f"Không tìm thấy cột ngày {DATE_COLS}; các cột có: {list(rows[0])}")
    if KUBUN_COL not in rows[0]:
        sys.exit(f"Không tìm thấy cột {KUBUN_COL}")

    def ym(d: str) -> str:
        d = d.strip().replace("/", "-")
        return d[:7]

    month_rows = [r for r in rows if ym(r[date_col]) == month]
    sessions = sorted({r[date_col].strip() for r in month_rows})
    if not sessions:
        sys.exit(f"Không có buổi nào trong tháng {month}")

    own = [r for r in month_rows if OWN_MARK in (r.get(KUBUN_COL) or "")]
    attended = defaultdict(set)   # key -> set(dates)
    info = {}                     # key -> (姓, 名, 会社名)
    for r in own:
        key = (norm(r.get("姓")), norm(r.get("名")))
        attended[key].add(r[date_col].strip())
        info.setdefault(key, (display(r.get("姓")), display(r.get("名")), display(r.get("会社名"))))

    n = len(sessions)
    kaikin = [k for k, d in attended.items() if len(d) == n]
    mousukoshi = [k for k, d in attended.items() if len(d) == n - 1]

    def sort_key(k):
        return info[k][0], info[k][1]

    def names(keys):
        return " , ".join(f"{info[k][0]} {info[k][1]}" for k in sorted(keys, key=sort_key))

    print(f"皆勤賞（{len(kaikin)}人）：{names(kaikin)}")
    print(f"もう少し賞（{len(mousukoshi)}人）：{names(mousukoshi)}")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
