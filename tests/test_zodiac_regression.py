"""별자리(Natal Chart) 계산 회귀 테스트 — skyfield ↔ pyephem cross-check.

CLAUDE.md 절대 룰: "추측 금지, 실측 데이터만". 두 엔진 결과 일치 보장.
- skyfield: NASA JPL DE421 ephemeris
- pyephem: libastro

실행:
    pytest tests/test_zodiac_regression.py -v
또는
    python tests/test_zodiac_regression.py
"""

from __future__ import annotations

import math
import sys
from datetime import datetime, timezone, timedelta

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from skyfield.api import load, wgs84
import ephem


ZODIAC = ["양자리", "황소자리", "쌍둥이자리", "게자리", "사자자리", "처녀자리",
          "천칭자리", "전갈자리", "사수자리", "염소자리", "물병자리", "물고기자리"]

PLANETS = [
    ("태양", "sun", ephem.Sun),
    ("달", "moon", ephem.Moon),
    ("수성", "mercury", ephem.Mercury),
    ("금성", "venus", ephem.Venus),
    ("화성", "mars", ephem.Mars),
    ("목성", "jupiter barycenter", ephem.Jupiter),
    ("토성", "saturn barycenter", ephem.Saturn),
    ("천왕성", "uranus barycenter", ephem.Uranus),
    ("해왕성", "neptune barycenter", ephem.Neptune),
]

# (label, year, month, day, hour, min, tz_offset, lat, lon, expected_sun_sign or None)
REFERENCE_CASES = [
    ("1990-03-15 서울 14:30 KST", 1990, 3, 15, 14, 30, 9, 37.5665, 126.978, "물고기자리"),
    ("2000-01-01 서울 정오 KST", 2000, 1, 1, 12, 0, 9, 37.5665, 126.978, "염소자리"),
    # 2024-06-21 정오 KST = UTC 03:00 < 하지 시점 04:50 UTC → 아직 쌍둥이자리
    ("2024-06-21 서울 정오 KST (하지 직전)", 2024, 6, 21, 12, 0, 9, 37.5665, 126.978, "쌍둥이자리"),
    # 별자리 경계 케이스 (양자리/물고기자리 경계 = 약 3월 20일)
    ("2024-03-20 서울 정오 (양자리 경계)", 2024, 3, 20, 12, 0, 9, 37.5665, 126.978, None),
    # 다른 시간대
    ("1985-07-15 뉴욕 10:00 EDT", 1985, 7, 15, 10, 0, -4, 40.7128, -74.0060, "게자리"),
    ("1999-12-31 런던 23:55 GMT", 1999, 12, 31, 23, 55, 0, 51.5074, -0.1278, "염소자리"),
]

_eph = None
_ts = None


def _load_skyfield():
    global _eph, _ts
    if _eph is None:
        _ts = load.timescale()
        _eph = load("de421.bsp")
    return _eph, _ts


def calc_skyfield_planets(birth_utc: datetime, lat: float, lon: float) -> dict:
    eph, ts = _load_skyfield()
    t = ts.from_datetime(birth_utc)
    earth = eph["earth"]
    observer = earth + wgs84.latlon(lat, lon)
    out = {}
    for name_ko, eph_key, _ in PLANETS:
        body = eph[eph_key]
        astro = observer.at(t).observe(body).apparent()
        _, ecl_lon, _ = astro.ecliptic_latlon()
        out[name_ko] = ecl_lon.degrees % 360
    return out


def calc_pyephem_planets(birth_utc: datetime, lat: float, lon: float) -> dict:
    obs = ephem.Observer()
    obs.lon = str(lon)
    obs.lat = str(lat)
    obs.date = ephem.Date(birth_utc.strftime("%Y/%m/%d %H:%M:%S"))
    out = {}
    for name_ko, _, body_cls in PLANETS:
        body = body_cls()
        body.compute(obs)
        ecl = ephem.Ecliptic(body)
        out[name_ko] = math.degrees(ecl.lon) % 360
    return out


def lon_to_sign(lon: float) -> str:
    return ZODIAC[int(lon // 30) % 12]


def main():
    print("=" * 100)
    print(f"별자리 회귀 테스트 — {len(REFERENCE_CASES)}개 케이스")
    print("출처: skyfield (NASA JPL DE421) ↔ pyephem (libastro)")
    print("=" * 100)

    total_planets = 0
    sign_mismatches = 0
    deg_max_diff = 0.0
    failures = []

    for case_idx, (label, y, m, d, h, mi, tz_off, lat, lon, expected_sun) in enumerate(REFERENCE_CASES, 1):
        birth_local = datetime(y, m, d, h, mi)
        birth_utc = birth_local.replace(tzinfo=timezone(timedelta(hours=tz_off))).astimezone(timezone.utc)

        sky = calc_skyfield_planets(birth_utc, lat, lon)
        pe = calc_pyephem_planets(birth_utc, lat, lon)

        case_mismatches = []
        case_max_diff = 0.0
        for name_ko, _, _ in PLANETS:
            sky_lon = sky[name_ko]
            pe_lon = pe[name_ko]
            sky_sign = lon_to_sign(sky_lon)
            pe_sign = lon_to_sign(pe_lon)
            diff = abs(sky_lon - pe_lon)
            if diff > 180:
                diff = 360 - diff
            case_max_diff = max(case_max_diff, diff)
            deg_max_diff = max(deg_max_diff, diff)
            total_planets += 1
            if sky_sign != pe_sign:
                sign_mismatches += 1
                case_mismatches.append(f"{name_ko}: sky={sky_sign} pe={pe_sign}")

        sun_sign = lon_to_sign(sky["태양"])
        sun_check = "" if not expected_sun else ("✅" if sun_sign == expected_sun else f"❌ expected={expected_sun}")
        status = "✅" if not case_mismatches else "❌"
        print(f"\n#{case_idx} {label}")
        print(f"  태양궁: {sun_sign} {sun_check}")
        print(f"  9개 행성 별자리 일치: {status}  (최대 도수 차: {case_max_diff:.2f}°)")
        if case_mismatches:
            for cm in case_mismatches:
                print(f"    ⚠️ {cm}")
            failures.append((label, case_mismatches))

    print("\n" + "=" * 100)
    if sign_mismatches == 0:
        print(f"✅ PASS: {total_planets}/{total_planets} 행성 별자리 일치")
        print(f"   최대 도수 차이: {deg_max_diff:.2f}° (보통 달의 parallax 영향, 별자리 동일이면 OK)")
    else:
        print(f"❌ FAIL: {sign_mismatches}/{total_planets} 행성 별자리 불일치")
        sys.exit(1)


def test_zodiac_engines_agree():
    """pytest용 — 두 엔진 별자리 일치 검증."""
    failures = []
    for label, y, m, d, h, mi, tz_off, lat, lon, _ in REFERENCE_CASES:
        birth_local = datetime(y, m, d, h, mi)
        birth_utc = birth_local.replace(tzinfo=timezone(timedelta(hours=tz_off))).astimezone(timezone.utc)
        sky = calc_skyfield_planets(birth_utc, lat, lon)
        pe = calc_pyephem_planets(birth_utc, lat, lon)
        for name_ko, _, _ in PLANETS:
            if lon_to_sign(sky[name_ko]) != lon_to_sign(pe[name_ko]):
                failures.append(f"{label} - {name_ko}")
    if failures:
        raise AssertionError(f"별자리 불일치 {len(failures)}건: {failures}")


if __name__ == "__main__":
    main()
