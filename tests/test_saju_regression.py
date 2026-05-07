"""사주 계산 회귀 테스트 — sajupy ↔ lunar-python cross-check.

CLAUDE.md 절대 룰: "추측 금지, 실측 데이터만". 두 라이브러리 결과 일치 보장.

실행:
    pytest tests/test_saju_regression.py -v
또는
    python tests/test_saju_regression.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Windows 콘솔 UTF-8
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from sajupy import calculate_saju as sajupy_calc
from lunar_python import Solar


# 알려진 reference 케이스 — 두 라이브러리 모두 동일 결과 산출해야 함
# 진태양시 보정 OFF (KST 표준자오선 기준 비교)
REFERENCE_CASES = [
    # (label, year, month, day, hour, minute, expected_8자_또는_None)
    # expected가 None이면 두 라이브러리 일치만 확인
    ("일반 오후 출생", 1990, 3, 15, 14, 30, None),
    ("야자시 23:30", 1990, 3, 15, 23, 30, None),
    ("조자시 00:30 (다음날)", 1990, 3, 16, 0, 30, None),
    ("새벽 일반", 1990, 3, 16, 1, 30, None),
    # 절기 경계 — 입동 전후
    ("입동 직전 1990-11-06", 1990, 11, 6, 12, 0, None),
    # 입춘 경계 — 매년 2/4 전후로 년주 변동
    ("입춘 직전 2000-02-03", 2000, 2, 3, 12, 0, None),  # 己卯년
    ("입춘 직후 2000-02-05", 2000, 2, 5, 12, 0, None),  # 庚辰년
    # 윤달·절기 경계 케이스
    ("2024-01-01 자정 직후", 2024, 1, 1, 0, 30, None),
    # 멀리 떨어진 케이스
    ("1900년 초", 1900, 1, 15, 12, 0, None),
    ("2099년 말", 2099, 12, 25, 18, 0, None),
]


def calc_lunar_python(y, m, d, h, mi):
    """lunar-python 8자 계산."""
    s = Solar.fromYmdHms(y, m, d, h, mi, 0)
    ec = s.getLunar().getEightChar()
    return f"{ec.getYear()}/{ec.getMonth()}/{ec.getDay()}/{ec.getTime()}"


def calc_sajupy(y, m, d, h, mi):
    """sajupy 8자 계산 (한국 만세력)."""
    r = sajupy_calc(year=y, month=m, day=d, hour=h, minute=mi, use_solar_time=False)
    return f"{r['year_pillar']}/{r['month_pillar']}/{r['day_pillar']}/{r['hour_pillar']}"


def test_all_cases():
    """모든 케이스에서 sajupy ↔ lunar-python 일치 확인."""
    failures = []
    for label, y, m, d, h, mi, expected in REFERENCE_CASES:
        lp = calc_lunar_python(y, m, d, h, mi)
        sj = calc_sajupy(y, m, d, h, mi)
        match = lp == sj
        exp_match = (expected is None) or (lp == expected)
        if not match or not exp_match:
            failures.append({
                "case": label, "date": f"{y}-{m:02d}-{d:02d} {h:02d}:{mi:02d}",
                "lunar_python": lp, "sajupy": sj, "expected": expected,
                "lib_match": match, "expected_match": exp_match,
            })
    return failures


def main():
    print("=" * 90)
    print(f"사주 회귀 테스트 — {len(REFERENCE_CASES)}개 케이스")
    print("출처: sajupy (한국 만세력 1900-2100) ↔ lunar-python")
    print("=" * 90)
    print(f"{'#':<3} {'케이스':<28} {'lunar-python':<22} {'sajupy':<22} {'일치':<6}")
    print("-" * 90)

    failures = []
    for i, (label, y, m, d, h, mi, expected) in enumerate(REFERENCE_CASES, 1):
        lp = calc_lunar_python(y, m, d, h, mi)
        sj = calc_sajupy(y, m, d, h, mi)
        match = lp == sj
        marker = "✅" if match else "❌"
        exp_note = ""
        if expected and lp != expected:
            exp_note = f"  ⚠️ expected: {expected}"
            marker = "❌"
        print(f"{i:<3} {label:<28} {lp:<22} {sj:<22} {marker}{exp_note}")
        if not match or (expected and lp != expected):
            failures.append((label, lp, sj, expected))

    print("-" * 90)
    if failures:
        print(f"❌ FAIL: {len(failures)}/{len(REFERENCE_CASES)} 케이스 불일치")
        for label, lp, sj, expected in failures:
            print(f"  - {label}: lunar={lp}, sajupy={sj}, expected={expected}")
        sys.exit(1)
    else:
        print(f"✅ PASS: 전체 {len(REFERENCE_CASES)}/{len(REFERENCE_CASES)} 케이스 일치")
        print("→ lunar-python = sajupy = 한국 만세력 표준 확인")
    return 0


# pytest entry
def test_saju_libraries_agree():
    """pytest용 — 라이브러리 간 일치만 검증 (expected는 정보 제공)."""
    failures = test_all_cases()
    failed_match = [f for f in failures if not f["lib_match"]]
    if failed_match:
        msg = "\n".join(
            f"  {f['case']} ({f['date']}): lunar={f['lunar_python']}, sajupy={f['sajupy']}"
            for f in failed_match
        )
        raise AssertionError(f"sajupy ↔ lunar-python 불일치 {len(failed_match)}건:\n{msg}")


if __name__ == "__main__":
    main()
