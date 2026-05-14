# MYLIFE — 인생 OS 템플릿

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-64%2F64%20passing-brightgreen)](tests/)
[![Python](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)
[![사주](https://img.shields.io/badge/%EC%82%AC%EC%A3%BC-%ED%95%9C%EA%B5%AD%20%EB%A7%8C%EC%84%B8%EB%A0%A5%20%EA%B2%80%EC%A6%9D-red)](scripts/calc_saju.py)
[![별자리](https://img.shields.io/badge/%EB%B3%84%EC%9E%90%EB%A6%AC-NASA%20JPL%20DE421-blueviolet)](scripts/calc_zodiac.py)
[![CLI](https://img.shields.io/badge/CLI-Claude%20Code%20%7C%20Codex-orange)](AGENTS.md)
[![No Speculation](https://img.shields.io/badge/%EC%B6%94%EC%B8%A1%20%EA%B8%88%EC%A7%80-%EC%8B%A4%EC%B8%A1%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%A7%8C-critical)](CLAUDE.md)

성격·가정환경·금전·직업·관계·로드맵을 한 번 채워두면 AI가 사용자 입력을 1순위 근거로 답해준다. 인터뷰 마지막에 셋업 보고서가 나오고, 이어서 영역별(연인·직업·사이드·돈·친구·가족) 깊이 풀이를 받을 수 있다.

사주·별자리는 운세 수준의 참고 톤. 명시 요청할 때만 답변에 반영한다.

---

## 시작하기

### 개발자 (CLI 익숙, 3분)

```bash
git clone https://github.com/yys5584/mylife-vault.git ~/MYLIFE
cd ~/MYLIFE
pip install -r scripts/requirements.txt
claude          # 또는 codex
```

Claude Code에서는 `/mylife-setup` 입력하면 인터뷰 시작.
Codex CLI에서는 `MYLIFE 인터뷰 시작해줘` 입력. AGENTS.md를 자동으로 로드한다.

### CLI 초보자 (Python·git 처음, 30분)

[QUICKSTART.md](QUICKSTART.md) 따라가기.

- Python 설치 (Mac·Windows·Linux)
- Claude Code·Codex 설치
- git clone 또는 ZIP 다운로드
- pip install (권한 문제 해결법)
- 자주 막히는 7가지와 해결법

### 비개발자 (Claude.ai Project — 가장 쉬움)

```
1. https://github.com/yys5584/mylife-vault → "Code" → "Download ZIP" → 압축 풀기
2. claude.ai 가입 (Pro $20/월 권장 — 컨텍스트가 큼)
3. 좌측 "Projects" → "Create Project" → 이름 "MYLIFE"
4. 우측 "Project knowledge" → templates/ 안 12개 .md + CLAUDE.md + AGENTS.md 업로드
5. "Custom instructions"에 붙여넣기:
   "이 프로젝트 파일들을 컨텍스트로 사용.
    CLAUDE.md 룰 따르기. 빈 placeholder({{...}})는 인터뷰로 채울 것."
6. 채팅 시작 → "MYLIFE 인터뷰 시작해줘"
```

한계와 보완:

- 사주·별자리 자동 계산은 안 됨. [원광대 만세력](https://manse.wgtc.ac.kr/)과 [astro.com](https://astro.com)에서 결과 받아서 Claude에 붙여넣기
- 또는 개발자 친구한테 부탁: "이 깃허브 클론해서 setup 한 번 돌려서 결과 .md 12개 압축해줘"

### 노션·옵시디언 사용자

ZIP 다운로드 → 12개 .md 파일 import → 페이지 본문 복사해서 LLM에 컨텍스트로 던진다. 갱신·검색은 노션·옵시디언에서.

### 시간

| 페이스 | 핵심 7개 | 도메인 확장 포함 | 보조(사주·별자리) 포함 |
|---|---|---|---|
| 빠르게 (한 줄 단답) | ~30분 | ~60분 | +10분 |
| 보통 (생각하며) | ~50분 | ~100분 | +10분 |
| 깊이 (사례·검증) | ~90분 | ~175분 | +15분 |

섹션 3 (인생 철학 = 우선순위 1위 + 진짜 이유 + 달성 후 그림)이 인터뷰 전체에서 가장 무겁다. 시간 들더라도 빠뜨리지 않는다.

처음엔 빠르게로 일단 다 채우고, 분기 갱신 때 깊이 보강 추천. 사주·별자리는 관심 있을 때만 채워도 된다.

---

## 무엇이 들어있나

12개 마크다운 문서로 구성된 인생 운영체제. 한 번 채우면 어떤 LLM이든 이 폴더를 컨텍스트로 받아 사용자 맞춤 답변을 한다.

응답의 1순위 근거는 사용자가 직접 채운 문서. 사주·별자리는 운세 수준의 참고 톤이며 명시 요청 시에만 꺼낸다.

### 핵심 7개 (필수, 사용자 직접 입력)

| 문서 | 용도 |
|---|---|
| [philosophy.md](templates/philosophy.md) | 인생 우선순위 1위 + 진짜 이유 + 달성 후 그림 + WHY·WHAT·HOW. vault 전체의 동력 |
| [self_profile.md](templates/self_profile.md) | 자기 진단 + 가정환경·직업·신경 |
| [life_os.md](templates/life_os.md) | 6 레이어 통합 시스템 (신체부터 정체성까지) |
| [life_compass.md](templates/life_compass.md) | 매일 보는 한 페이지 컴파스 |
| [roadmap.md](templates/roadmap.md) | Daily부터 Yearly까지 시간 단위 |
| [relationship_protocol.md](templates/relationship_protocol.md) | 관계 룰 (사건·침묵·메시지·다음 관계). 해당 시 |
| [side_project_strategy.md](templates/side_project_strategy.md) | 사이드 운영 전략. 해당 시 |

### 도메인 확장 3개 (선택, 깊이)

| 문서 | 용도 |
|---|---|
| [love_style.md](templates/love_style.md) | 연애 스타일 — 애착 유형·궁합·데이트 룰·결혼 결정 필터 |
| [investment_style.md](templates/investment_style.md) | 투자 스타일 — 리스크·자산 배분·매매 트리거·위험 신호 |
| [career_style.md](templates/career_style.md) | 직업 스타일 — 일하는 방식·번아웃 패턴·이직 5필터 |

### 보조 도구 2개 (선택, 운세 색깔용)

응답의 근거가 아니라 톤. AI는 명시 요청 시에만 참조하고 일반 자문에는 안 낀다. 자세한 룰은 [CLAUDE.md](CLAUDE.md)의 "사주·별자리 — 위치 정의" 참조.

| 문서 | 용도 | 자동·수동 |
|---|---|---|
| [saju.md](templates/saju.md) | 사주 8자 + 십신 + 12운성 + 공망 + 신살 + 대운 + 세운 | 자동 (`scripts/calc_saju.py`) |
| [zodiac.md](templates/zodiac.md) | 출생 차트 (태양·달·상승궁 + 행성 9개) | 자동 (`scripts/calc_zodiac.py`) |

---

## 사주·별자리 정확도 — 검증된 실측 데이터만

룰([CLAUDE.md](CLAUDE.md) 절대 룰): LLM 추측 금지, 검증된 출처만.

```bash
# 사주 (--gender는 사용자 성별: male / female)
python scripts/calc_saju.py --date YYYY-MM-DD --time HH:MM --gender female --place "Seoul" --true-solar

# 별자리
python scripts/calc_zodiac.py --date YYYY-MM-DD --time HH:MM --place "Seoul"

# 도시 미지원 시 위경도 직접 (구글 지도에서 좌표 복사)
python scripts/calc_saju.py --date YYYY-MM-DD --time HH:MM --gender female --longitude XXX.XXXX --true-solar
python scripts/calc_zodiac.py --date YYYY-MM-DD --time HH:MM --lat XX.XXXX --lon XXX.XXXX --tz 9

# 회귀 테스트 (cross-check 검증, 64/64 통과)
python tests/test_saju_regression.py
python tests/test_zodiac_regression.py
```

### 사주 검증 체계 (라이브러리 2개 교차 검증)

| 단계 | 출처 | 역할 |
|---|---|---|
| 1차 (8자) | sajupy (한국 만세력 1900-2100) | Primary — 한국 표준 |
| 2차 (8자) | lunar-python (중국 만년력 + 천문 공식) | 교차 검증, 매 실행 자동 비교 |
| 추가 | lunar-python (대운·세운·12운성·공망·신살·지장간·납음) | 검증된 8자 위에 결정론 계산 |
| 한국 신살 | 표준 룰 직접 구현 (천을귀인·문창·양인·역마·도화·화개·장성) | 모든 만세력 사이트 공통 |
| 회귀 | `tests/test_saju_regression.py` (10 케이스) | 자시 경계·입춘 경계·진태양시 검증 |

두 라이브러리 8자가 불일치하면 자동으로 진행 중단하고 ⚠️ 경고 표시.

### 별자리 검증 체계 (엔진 2개 교차 검증)

| 단계 | 엔진 | 데이터 |
|---|---|---|
| 1차 | skyfield | NASA JPL DE421 ephemeris |
| 2차 | pyephem | libastro (XEphem 기반, 다른 코드 경로) |
| 추가 | 상승궁(Ascendant) | 천문 공식 직접 (Local Sidereal Time + 황도경사) |
| 회귀 | `tests/test_zodiac_regression.py` (6 케이스 × 9 행성 = 54) | 100% 일치 |

두 엔진 행성 별자리가 불일치하면 자동으로 진행 중단.

### Python 없는 환경

- 사주는 [원광디지털대 만세력](https://manse.wgtc.ac.kr/) 결과 → `templates/saju.md` 표에 직접 입력
- 별자리는 [astro.com](https://astro.com) Free Horoscopes → Birth Chart → 빅3 + 행성 → `templates/zodiac.md`에 직접 입력

### 왜 동양·서양 둘 다?

다른 좌표계. 두 시스템 공통으로 강한 영역은 본질이 강하게 드러난다. 충돌 영역은 사용자 안의 다층성.

---

## 사용 시나리오

인터뷰가 끝나면 셋업 완료 보고서가 나오고, 이어서 영역별 깊이 풀이 메뉴가 뜬다. 사주·별자리는 명시 요청 시에만 같이 얹는다.

| 영역 | LLM에게 | 작동 |
|---|---|---|
| 나와 맞는 연인 / 위험한 유형 | "나와 맞는 연인 유형 봐줘" | `love_style.md` + `relationship_protocol.md` + `self_profile.md` |
| 나와 맞는 직업·역할 | "나에게 맞는 직업 봐줘" | `career_style.md` + `self_profile.md` + `philosophy.md` |
| 나와 맞는 사이드 방향 | "어떤 사이드가 맞을까" | `side_project_strategy.md` + `self_profile.md` |
| 내 돈 그릇·재물 패턴 | "내 돈 그릇 어때" | `investment_style.md` + `philosophy.md` + `self_profile.md` |
| 친구·동료 함정 | "내가 자주 빠지는 인간관계 함정 봐줘" | `self_profile.md` 위험 신호 |
| 가족 영향 | "가족이 나에게 어떻게 영향 줬어" | `self_profile.md` 형성 사건 |
| (보조, 명시 요청 시만) 사주 같이 보기 | "사주로도 봐줘" | `saju.md` 박제 + 세운 |
| (보조, 명시 요청 시만) 별자리 같이 보기 | "별자리로도 봐줘" | `zodiac.md` 태양궁·달궁·상승궁 |

---

## 갱신 + 백업

### 갱신 주기

- 분기 1회 (3개월): `roadmap.md` 분기 목표, `life_compass.md` 5년 북극성 검토
- 연 1회 (생일·1월): 모든 문서 검토, 정체성 한 문장 갱신
- 사건 발생 시: `relationship_protocol.md`에 새 사건 추가, `self_profile.md` 위험 신호 갱신

### 사용자 vault 백업 (선택)

사용자가 채운 데이터는 민감 정보. 백업 원하면 별도 private repo 권장.

```bash
cd ~/MYLIFE
git remote remove origin
git remote add origin https://github.com/<본인>/<my-vault-private>.git
git push -u origin main
```

### 템플릿 업데이트 받기 (이 repo가 개선되면)

```bash
cd ~/MYLIFE
git remote add upstream https://github.com/yys5584/mylife-vault.git
git fetch upstream
git merge upstream/main   # 사용자 templates/ 충돌 시 사용자 거 유지
```

---

## 폴더 구조

```
mylife-vault/
├── README.md                       # 지금 보는 문서
├── CLAUDE.md                       # Claude Code 에이전트 룰 (절대 룰 포함)
├── AGENTS.md                       # Codex CLI 에이전트 룰
├── SETUP.md                        # 수동 인터뷰 가이드
├── LICENSE                         # MIT
├── .gitignore                      # de421.bsp, __pycache__ 등 제외
├── templates/                      # 12개 인생 템플릿 (핵심 7 + 도메인 3 + 보조 2)
│   ├── philosophy.md
│   ├── self_profile.md
│   ├── saju.md                     # 동양 — sajupy + lunar-python
│   ├── zodiac.md                   # 서양 — skyfield + pyephem
│   ├── life_os.md
│   ├── life_compass.md
│   ├── roadmap.md
│   ├── relationship_protocol.md
│   ├── side_project_strategy.md
│   ├── love_style.md               # 도메인 확장: 연애
│   ├── investment_style.md         # 도메인 확장: 투자
│   └── career_style.md             # 도메인 확장: 직업
├── .claude/
│   └── commands/
│       └── mylife-setup.md         # /mylife-setup 슬래시 커맨드
├── scripts/
│   ├── calc_saju.py                # 사주 자동 계산 (이중 검증)
│   ├── calc_zodiac.py              # 출생 차트 자동 계산 (이중 검증)
│   └── requirements.txt
└── tests/
    ├── test_saju_regression.py     # 10 케이스, 100% 통과
    └── test_zodiac_regression.py   # 7 × 9 = 63 케이스, 100% 통과
```

---

## 의존 라이브러리 (Credits)

이 프로젝트는 다음 오픈소스 라이브러리 위에 동작한다.

| 라이브러리 | 용도 | 라이선스 |
|---|---|---|
| [sajupy](https://github.com/0ssw1/sajupy) | 한국 만세력 1900-2100 사주 8자 | MIT |
| [lunar-python](https://github.com/6tail/lunar-python) | 중국 만년력 + 사주 추가 기능 | MIT |
| [skyfield](https://rhodesmill.org/skyfield/) | NASA JPL DE421 행성 위치 계산 | MIT |
| [pyephem (ephem)](https://rhodesmill.org/pyephem/) | XEphem의 libastro 코드 기반 천체역학 | MIT |

별도 외부 API 호출 없음. 모두 로컬 결정론 계산.

---

## Disclaimer

- 사주·별자리는 운세 수준의 참고 도구다. 답변의 근거가 아니고 운명 결정도 아니다. 사용자가 채운 자기진단·철학·시스템이 1순위.
- 인생의 큰 결정(이직·결혼·이주·치료 등)을 사주·별자리만으로 내리지 않는다. 외부 sounding board(친구·전문가) 1인은 별도로.
- 정신건강 진단을 자가 평가로 대체하지 않는다. 의심 시 정신건강의학과·임상심리사 상담.

---

## Issues / Contributing

- 버그·제안: [Issues](https://github.com/yys5584/mylife-vault/issues)
- 사주·별자리 라이브러리 결과 불일치 발견 시 회귀 테스트 케이스 추가 PR 환영
- 새 템플릿(영양·재무·운동 등) 추가 PR도 OK. 단 분석가 톤·새 문서 무한 추가 금지 룰 ([CLAUDE.md](CLAUDE.md)) 확인

---

## License

[MIT](LICENSE) — 코드 부분.
`templates/` 안 자기계발 프레임워크는 공개 도메인 심리학·코칭 개념 기반의 사용자 적용 가이드.

---

## 한 줄

분석은 9짜리. 컴파스가 그 9를 오늘의 행동으로 옮기는 다리.
다리 없으면 9짜리 분석도 3짜리 행동에 막혀서 안 옮겨진다.
