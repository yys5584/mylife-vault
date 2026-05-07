#!/usr/bin/env python3
"""출생 차트 (Natal Chart) 계산 — 양력 생년월일시 + 출생지 → 태양궁·달궁·상승궁·행성 배치.

**검증 정책 (CLAUDE.md 절대 룰):**
- skyfield (NASA JPL DE421 ephemeris) = primary
- pyephem (libastro) = cross-check 백업
- 매 실행마다 두 엔진 행성 위치 자동 비교, 별자리 불일치 시 ⚠️ 경고 + 진행 중단

사용:
    python calc_zodiac.py --date 1990-03-15 --time 14:30 --place "Seoul"
    python calc_zodiac.py --date 1990-03-15 --time 14:30 --lat 37.5665 --lon 126.978
    python calc_zodiac.py --date 1990-03-15 --time unknown --place "Seoul"

의존성:
    pip install skyfield ephem
"""

from __future__ import annotations

import argparse
import io
import math
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    from skyfield.api import load, wgs84
except ImportError:
    sys.stderr.write("skyfield 미설치. pip install -r scripts/requirements.txt\n")
    sys.exit(1)

try:
    import ephem as pyephem
except ImportError:
    sys.stderr.write("pyephem 미설치 (cross-check 검증용). pip install -r scripts/requirements.txt\n")
    sys.exit(1)

# 별자리 12궁 (pokebot horoscope_service.py 기반)
ZODIAC_SIGNS = [
    {"name": "양자리",     "symbol": "♈", "en": "Aries",       "element": "불",  "mode": "활동궁",
     "ruler": "화성", "trait": "충동·리더십·에너지·경쟁심"},
    {"name": "황소자리",   "symbol": "♉", "en": "Taurus",      "element": "땅",  "mode": "고정궁",
     "ruler": "금성", "trait": "안정·소유욕·감각·완고함"},
    {"name": "쌍둥이자리", "symbol": "♊", "en": "Gemini",      "element": "바람", "mode": "변통궁",
     "ruler": "수성", "trait": "호기심·소통·변덕·멀티태스킹"},
    {"name": "게자리",     "symbol": "♋", "en": "Cancer",      "element": "물",  "mode": "활동궁",
     "ruler": "달",   "trait": "모성·감정 기복·방어적·가정 중심"},
    {"name": "사자자리",   "symbol": "♌", "en": "Leo",         "element": "불",  "mode": "고정궁",
     "ruler": "태양", "trait": "자존심·관대함·주목·창의력"},
    {"name": "처녀자리",   "symbol": "♍", "en": "Virgo",       "element": "땅",  "mode": "변통궁",
     "ruler": "수성", "trait": "분석·완벽주의·건강 민감·비판적"},
    {"name": "천칭자리",   "symbol": "♎", "en": "Libra",       "element": "바람", "mode": "활동궁",
     "ruler": "금성", "trait": "조화·우유부단·미적 감각·관계 지향"},
    {"name": "전갈자리",   "symbol": "♏", "en": "Scorpio",     "element": "물",  "mode": "고정궁",
     "ruler": "명왕성/화성", "trait": "집요함·비밀주의·통찰·질투"},
    {"name": "사수자리",   "symbol": "♐", "en": "Sagittarius", "element": "불",  "mode": "변통궁",
     "ruler": "목성", "trait": "자유·낙관·솔직함·무책임"},
    {"name": "염소자리",   "symbol": "♑", "en": "Capricorn",   "element": "땅",  "mode": "활동궁",
     "ruler": "토성", "trait": "야망·인내·현실주의·감정 억제"},
    {"name": "물병자리",   "symbol": "♒", "en": "Aquarius",    "element": "바람", "mode": "고정궁",
     "ruler": "천왕성/토성", "trait": "독립·혁신·반항·박애주의"},
    {"name": "물고기자리", "symbol": "♓", "en": "Pisces",      "element": "물",  "mode": "변통궁",
     "ruler": "해왕성/목성", "trait": "직감·공감·현실도피·예술적"},
]

# 도시 → (lat, lon, tz_offset_hours)
CITY_DATA = {
    "seoul":   (37.5665, 126.9780,  9), "서울":   (37.5665, 126.9780,  9),
    "busan":   (35.1796, 129.0756,  9), "부산":   (35.1796, 129.0756,  9),
    "incheon": (37.4563, 126.7052,  9), "인천":   (37.4563, 126.7052,  9),
    "daegu":   (35.8714, 128.6014,  9), "대구":   (35.8714, 128.6014,  9),
    "daejeon": (36.3504, 127.3845,  9), "대전":   (36.3504, 127.3845,  9),
    "gwangju": (35.1595, 126.8526,  9), "광주":   (35.1595, 126.8526,  9),
    "suwon":   (37.2636, 127.0286,  9), "수원":   (37.2636, 127.0286,  9),
    "jeju":    (33.4996, 126.5312,  9), "제주":   (33.4996, 126.5312,  9),
    "tokyo":   (35.6762, 139.6503,  9), "도쿄":   (35.6762, 139.6503,  9),
    "osaka":   (34.6937, 135.5023,  9), "오사카": (34.6937, 135.5023,  9),
    "beijing": (39.9042, 116.4074,  8), "베이징": (39.9042, 116.4074,  8),
    "shanghai":(31.2304, 121.4737,  8), "상하이": (31.2304, 121.4737,  8),
    "newyork": (40.7128, -74.0060, -5), "뉴욕":   (40.7128, -74.0060, -5),
    "losangeles": (34.0522, -118.2437, -8), "la": (34.0522, -118.2437, -8),
    "london":  (51.5074,  -0.1278,  0), "런던":   (51.5074,  -0.1278,  0),
    "paris":   (48.8566,   2.3522,  1), "파리":   (48.8566,   2.3522,  1),
    "sydney":  (-33.8688, 151.2093, 10), "시드니":(-33.8688, 151.2093, 10),
}

PLANETS = [
    ("태양", "☉", "sun"),
    ("달",   "☽", "moon"),
    ("수성", "☿", "mercury"),
    ("금성", "♀", "venus"),
    ("화성", "♂", "mars"),
    ("목성", "♃", "jupiter barycenter"),
    ("토성", "♄", "saturn barycenter"),
    ("천왕성", "♅", "uranus barycenter"),
    ("해왕성", "♆", "neptune barycenter"),
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="출생 차트 (Natal Chart) 계산")
    p.add_argument("--date", required=True, help="양력 생년월일 (YYYY-MM-DD)")
    p.add_argument("--time", default="12:00", help="출생 시간 (HH:MM, 24h, 현지시) 또는 'unknown'")
    p.add_argument("--place", default="", help='출생 도시 (예: "Seoul")')
    p.add_argument("--lat", type=float, help="위도 (--place 대신)")
    p.add_argument("--lon", type=float, help="경도 (--place 대신)")
    p.add_argument("--tz", type=float, help="시간대 UTC offset (예: 9 = KST)")
    p.add_argument("--output", default=None, help="결과 .md 경로 (기본: templates/zodiac.md)")
    p.add_argument("--print-only", action="store_true", help="파일 갱신 안 함")
    return p.parse_args()


def resolve_location(place: str, lat: float | None, lon: float | None,
                     tz: float | None) -> tuple[float, float, float]:
    if lat is not None and lon is not None:
        return (lat, lon, tz if tz is not None else 0)
    if not place:
        raise ValueError("--place 또는 --lat/--lon 둘 중 하나 필수")
    key = place.split(",")[0].strip().lower().replace(" ", "")
    if key not in CITY_DATA:
        raise ValueError(
            f"도시 인식 불가: {place}\n  --lat/--lon 직접 지정하거나, "
            f"인식 가능 도시: {', '.join(sorted(set(CITY_DATA.keys())))}"
        )
    return CITY_DATA[key]


def ecliptic_lon_to_sign(lon_deg: float) -> tuple[dict, float]:
    """황도 경도(0-360°) → (별자리, 도수 0-30°)."""
    lon_deg = lon_deg % 360
    sign_idx = int(lon_deg // 30)
    deg_in_sign = lon_deg % 30
    return (ZODIAC_SIGNS[sign_idx], deg_in_sign)


def calc_ascendant(jd_ut: float, lat_deg: float, lon_deg: float) -> float:
    """상승궁(Ascendant) 황도 경도 계산.

    공식: ASC = arctan2(-cos(LST), sin(LST)·cos(ε) + tan(φ)·sin(ε))
    LST = local sidereal time, ε = 황도경사각, φ = 위도
    """
    # GMST in degrees (Meeus, Astronomical Algorithms, ch.12)
    T = (jd_ut - 2451545.0) / 36525.0
    gmst_deg = (280.46061837 + 360.98564736629 * (jd_ut - 2451545.0)
                + 0.000387933 * T * T - T * T * T / 38710000.0) % 360
    lst_deg = (gmst_deg + lon_deg) % 360
    lst_rad = math.radians(lst_deg)

    # 황도경사각 (mean obliquity)
    eps_deg = 23.4392911 - 0.0130042 * T
    eps_rad = math.radians(eps_deg)
    phi_rad = math.radians(lat_deg)

    asc_rad = math.atan2(
        -math.cos(lst_rad),
        math.sin(lst_rad) * math.cos(eps_rad) + math.tan(phi_rad) * math.sin(eps_rad)
    )
    asc_deg = math.degrees(asc_rad) % 360
    # ASC는 동쪽 지평선 → 보정
    if asc_deg < 180:
        asc_deg += 180
    else:
        asc_deg -= 180
    return asc_deg


def calc_pyephem_planets(birth_utc: datetime, lat: float, lon: float) -> dict:
    """pyephem(libastro)으로 행성 황도 경도 계산. cross-check용."""
    import math
    obs = pyephem.Observer()
    obs.lon = str(lon)
    obs.lat = str(lat)
    obs.date = pyephem.Date(birth_utc.strftime("%Y/%m/%d %H:%M:%S"))

    bodies = {
        "태양": pyephem.Sun(), "달": pyephem.Moon(),
        "수성": pyephem.Mercury(), "금성": pyephem.Venus(), "화성": pyephem.Mars(),
        "목성": pyephem.Jupiter(), "토성": pyephem.Saturn(),
        "천왕성": pyephem.Uranus(), "해왕성": pyephem.Neptune(),
    }
    result = {}
    for name, body in bodies.items():
        body.compute(obs)
        ecl = pyephem.Ecliptic(body)
        result[name] = math.degrees(ecl.lon) % 360
    return result


def calc_natal_chart(birth_dt_local: datetime, tz_offset_hours: float,
                     lat: float, lon: float, time_known: bool):
    tz = timezone(timedelta(hours=tz_offset_hours))
    birth_dt_aware = birth_dt_local.replace(tzinfo=tz)
    birth_utc = birth_dt_aware.astimezone(timezone.utc)

    ts = load.timescale()
    t = ts.from_datetime(birth_utc)

    eph = load("de421.bsp")
    earth = eph["earth"]
    observer = earth + wgs84.latlon(lat, lon)

    # skyfield 행성 황도 경도
    planet_results = []
    for name_ko, symbol, eph_key in PLANETS:
        try:
            body = eph[eph_key]
        except KeyError:
            continue
        astrometric = observer.at(t).observe(body).apparent()
        ecl_lat, ecl_lon, _ = astrometric.ecliptic_latlon()
        sign, deg_in_sign = ecliptic_lon_to_sign(ecl_lon.degrees)
        planet_results.append({
            "name": name_ko, "symbol": symbol,
            "longitude": ecl_lon.degrees,
            "sign": sign, "degree": deg_in_sign,
        })

    # pyephem cross-check
    pyephem_lons = calc_pyephem_planets(birth_utc, lat, lon)
    mismatches = []
    for p in planet_results:
        pe_lon = pyephem_lons.get(p["name"])
        if pe_lon is None:
            continue
        sky_sign_idx = int(p["longitude"] // 30) % 12
        pe_sign_idx = int(pe_lon // 30) % 12
        if sky_sign_idx != pe_sign_idx:
            mismatches.append({
                "planet": p["name"],
                "skyfield_sign": ZODIAC_SIGNS[sky_sign_idx]["name"],
                "pyephem_sign": ZODIAC_SIGNS[pe_sign_idx]["name"],
                "skyfield_lon": p["longitude"],
                "pyephem_lon": pe_lon,
            })
    if mismatches:
        sys.stderr.write("\n" + "=" * 70 + "\n")
        sys.stderr.write("🚨 skyfield ↔ pyephem 별자리 불일치 감지!\n")
        sys.stderr.write("=" * 70 + "\n")
        for mm in mismatches:
            sys.stderr.write(
                f"  {mm['planet']}: skyfield={mm['skyfield_sign']} ({mm['skyfield_lon']:.2f}°), "
                f"pyephem={mm['pyephem_sign']} ({mm['pyephem_lon']:.2f}°)\n"
            )
        sys.stderr.write("\n진행 중단.\n")
        sys.stderr.write("=" * 70 + "\n")
        sys.exit(2)

    # 상승궁 (Ascendant) — 출생 시간 정확해야 의미 있음
    ascendant = None
    if time_known:
        jd_ut = t.ut1  # Skyfield Time 객체의 UT1 (approx UT)
        asc_deg = calc_ascendant(jd_ut, lat, lon)
        asc_sign, asc_deg_in_sign = ecliptic_lon_to_sign(asc_deg)
        ascendant = {"longitude": asc_deg, "sign": asc_sign, "degree": asc_deg_in_sign}

    # 원소·모드 분포
    element_count = {"불": 0, "땅": 0, "바람": 0, "물": 0}
    mode_count = {"활동궁": 0, "고정궁": 0, "변통궁": 0}
    for p in planet_results:
        element_count[p["sign"]["element"]] += 1
        mode_count[p["sign"]["mode"]] += 1

    return {
        "planets": planet_results,
        "ascendant": ascendant,
        "elements": element_count,
        "modes": mode_count,
        "birth_utc": birth_utc,
    }


def fmt_planet(p: dict) -> str:
    sign = p["sign"]
    return f"{p['symbol']} {p['name']:<4} → {sign['symbol']} {sign['name']:<6} {p['degree']:5.1f}°"


def render_zodiac_md(args, result, location, time_known) -> str:
    lat, lon, tz = location
    sun = next(p for p in result["planets"] if p["name"] == "태양")
    moon = next(p for p in result["planets"] if p["name"] == "달")
    asc = result["ascendant"]

    sun_line = f"{sun['sign']['symbol']} **{sun['sign']['name']}** ({sun['sign']['en']}) {sun['degree']:.1f}°"
    moon_line = f"{moon['sign']['symbol']} **{moon['sign']['name']}** ({moon['sign']['en']}) {moon['degree']:.1f}°"
    if asc:
        asc_line = f"{asc['sign']['symbol']} **{asc['sign']['name']}** ({asc['sign']['en']}) {asc['degree']:.1f}°"
    else:
        asc_line = "(출생 시간 미상으로 계산 불가 — 정확한 시간 확보 시 갱신)"

    elem = result["elements"]
    modes = result["modes"]

    def strength(n: int, total: int = 9) -> str:
        ratio = n / total if total else 0
        if ratio >= 0.4: return "과다"
        if ratio >= 0.25: return "강함"
        if ratio >= 0.15: return "보통"
        if ratio > 0: return "약함"
        return "없음"

    planet_table_rows = "\n".join(
        f"| {p['symbol']} {p['name']} | {p['sign']['symbol']} {p['sign']['name']} | {p['degree']:.1f}° | {p['sign']['element']} | {p['sign']['ruler']} |"
        for p in result["planets"]
    )

    place_str = args.place if args.place else f"({lat:.4f}, {lon:.4f})"

    md = f"""# 별자리 — 출생 차트 (Natal Chart)

> 양력 생년월일시 + 출생지 → 행성 12궁 배치 자동 계산.
> `scripts/calc_zodiac.py`로 갱신됨 (skyfield + NASA JPL ephemeris 기반).
> **계산은 박제, 해석은 on-demand.**

---

## 입력 정보

| 항목 | 값 |
|---|---|
| 양력 생년월일 | {args.date} |
| 출생 시간 | {args.time if time_known else "미상"} |
| 출생지 | {place_str} |
| 위도 / 경도 | {lat:.4f} / {lon:.4f} |
| 시간대 (UTC) | {tz:+g} |
| UTC 환산 | {result['birth_utc'].strftime('%Y-%m-%d %H:%M')} UTC |

---

## 빅 3 (가장 중요)

| 위치 | 별자리 | 의미 |
|---|---|---|
| ☉ 태양궁 (Sun Sign) | {sun_line} | 본질·자아·인생의 큰 방향 |
| ☽ 달궁 (Moon Sign) | {moon_line} | 감정·무의식·필요·익숙함 |
| ⬆️ 상승궁 (Ascendant) | {asc_line} | 외부에 비치는 첫인상·인생 접근 방식 |

> 셋 다 다른 별자리면 → 다층적 성격. 같으면 → 일관된 강한 캐릭터.
> 상승궁은 출생 시간 4분 차이로 1도 변함. 시간 모르면 의미 없음.

---

## 전체 행성 배치

| 행성 | 별자리 | 도수 | 원소 | 지배행성 |
|---|---|---|---|---|
{planet_table_rows}

---

## 원소 분포 (Fire / Earth / Air / Water)

| 원소 | 개수 | 강약 |
|---|---|---|
| 🔥 불 (Fire) | {elem['불']} | {strength(elem['불'])} |
| 🌍 땅 (Earth) | {elem['땅']} | {strength(elem['땅'])} |
| 💨 바람 (Air) | {elem['바람']} | {strength(elem['바람'])} |
| 💧 물 (Water) | {elem['물']} | {strength(elem['물'])} |

**과다 원소:** {", ".join(k for k, v in elem.items() if v >= 4) or "없음"}
**부족 원소:** {", ".join(k for k, v in elem.items() if v == 0) or "없음"}

> 부족 원소 = 본인이 자연스럽게 못하는 영역. 시스템(life_os)으로 보완.

---

## 모드 분포 (Cardinal / Fixed / Mutable)

| 모드 | 개수 | 키워드 |
|---|---|---|
| 활동궁 (Cardinal) | {modes['활동궁']} | 시작·주도·리더십 |
| 고정궁 (Fixed) | {modes['고정궁']} | 지속·안정·완고 |
| 변통궁 (Mutable) | {modes['변통궁']} | 적응·변화·유연 |

---

## 해석 — 본인 별자리 한 줄 요약

<!-- 이 섹션은 LLM이 위 데이터를 기반으로 작성. 매년 갱신 가능. -->
<!-- AI에게: "내 출생 차트 보고 한 줄 요약해줘" -->

> (해석 필요)

---

## 빅 3 조합 해석

<!-- AI에게: "내 빅3 (태양·달·상승) 조합 해석해줘" -->

- **태양 ({sun['sign']['name']})** — {sun['sign']['trait']}
- **달 ({moon['sign']['name']})** — {moon['sign']['trait']}
- **상승 ({asc['sign']['name'] if asc else '?'})** — {asc['sign']['trait'] if asc else '(시간 미상)'}

---

## 활용 — 다른 문서와 연결

- **태양궁 traits** → [philosophy.md](philosophy.md)의 *3개 축* 검증
- **달궁 traits** → [self_profile.md](self_profile.md)의 *감정 패턴* 진단
- **부족 원소** → [life_os.md](life_os.md)의 *6 레이어*로 보완
- **상승궁** → [life_compass.md](life_compass.md)의 *외부 첫인상* 인지

---

## 사주와의 차이

- **사주** ([saju.md](saju.md)): 한국·동양 — 천간지지·오행·음양
- **별자리** (이 문서): 서양 — 황도 12궁·행성·원소
- 두 시스템은 *다른 좌표계*. 같은 사람도 다른 측면을 비춤.
- 일치하는 부분 = 본질이 강하게 드러나는 영역
- 충돌하는 부분 = 본인 안의 *긴장·다층성*

---

## 한 줄

> **별자리는 *우주의 시계*가 출생 순간 본인에게 새긴 도장.**
> 운명 결정 ❌. *기질의 청사진*. 청사진 알면 어떤 집을 지을지 명확해짐.

---

## 갱신 이력

- {datetime.now().strftime("%Y-%m-%d")}: `scripts/calc_zodiac.py` 실행
"""
    return md


def main() -> int:
    args = parse_args()

    try:
        date_part = datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        sys.stderr.write(f"날짜 형식 오류: {args.date}\n")
        return 1

    time_known = args.time.lower() != "unknown"
    if time_known:
        try:
            t = datetime.strptime(args.time, "%H:%M")
            birth_dt = date_part.replace(hour=t.hour, minute=t.minute)
        except ValueError:
            sys.stderr.write(f"시간 형식 오류: {args.time}\n")
            return 1
    else:
        birth_dt = date_part.replace(hour=12, minute=0)  # sun sign만 정확

    try:
        location = resolve_location(args.place, args.lat, args.lon, args.tz)
    except ValueError as e:
        sys.stderr.write(f"{e}\n")
        return 1

    lat, lon, tz_hours = location
    result = calc_natal_chart(birth_dt, tz_hours, lat, lon, time_known)

    # 콘솔 요약
    print(f"양력: {args.date} {args.time}  ({args.place or f'lat={lat}, lon={lon}'})")
    print(f"UTC: {result['birth_utc'].strftime('%Y-%m-%d %H:%M')}")
    print()
    print("빅 3:")
    sun = next(p for p in result["planets"] if p["name"] == "태양")
    moon = next(p for p in result["planets"] if p["name"] == "달")
    print(f"  ☉ 태양궁: {sun['sign']['symbol']} {sun['sign']['name']} {sun['degree']:.1f}°")
    print(f"  ☽ 달궁:   {moon['sign']['symbol']} {moon['sign']['name']} {moon['degree']:.1f}°")
    if result["ascendant"]:
        asc = result["ascendant"]
        print(f"  ⬆ 상승궁: {asc['sign']['symbol']} {asc['sign']['name']} {asc['degree']:.1f}°")
    else:
        print("  ⬆ 상승궁: (시간 미상)")
    print()
    print("행성 배치:")
    for p in result["planets"]:
        print(f"  {fmt_planet(p)}")
    print()
    print(f"원소 분포: 불 {result['elements']['불']} / 땅 {result['elements']['땅']} / 바람 {result['elements']['바람']} / 물 {result['elements']['물']}")

    if args.print_only:
        return 0

    output_path = Path(args.output) if args.output else (
        Path(__file__).parent.parent / "templates" / "zodiac.md"
    )
    md_content = render_zodiac_md(args, result, location, time_known)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(md_content, encoding="utf-8")
    print(f"\n✅ 저장됨: {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
