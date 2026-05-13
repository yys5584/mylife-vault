# QUICKSTART — Claude한테 시키기

CLI 초보자용. Claude Code 있으면 Claude한테 다 시키면 된다.
Python 설치·git·pip 같은 거 손으로 칠 필요 없다.

---

## 진짜 가장 빠른 방법 (5분)

### 1. Claude Code 설치 (1회)

https://claude.com/claude-code → 사용자 OS 다운로드 → 설치 → `claude` 명령으로 진입.

### 2. 사전 준비 — 사용자 정보만 메모

```
- 양력 생년월일 (YYYY-MM-DD)
- 출생 시간 (HH:MM, 모르면 "모름")
- 출생 도시 (시·구)
- 성별
- 거주지·직업·가족 구성 (간단히)
```

### 3. Claude한테 던지기

터미널 어디서든 `claude` 실행 후, 아래 한 줄 그대로 복붙.

```
이 vault 셋업해줘: https://github.com/yys5584/mylife-vault

내 홈 폴더에 클론 → 의존성 설치 → /mylife-setup 인터뷰 시작.
사주·별자리 자동 계산은 선택 — 내가 원하면 그때 돌려줘.
Python·pip 명령은 알아서. 막히면 물어봐.
```

Claude가 알아서 한다.

1. `git clone`으로 사용자 컴퓨터에 다운로드
2. `pip install -r scripts/requirements.txt` (권한 문제 만나면 `--user` 자동 추가)
3. 핵심 7개 입력 인터뷰 시작 (자기진단·철학·시스템 등)
4. (선택) 사주·별자리 원하면 그때 `calc_saju.py`·`calc_zodiac.py` 실행

Python 없으면 Claude가 "Python 먼저 설치해야 함" 안내 + 사용자 OS에 맞는 명령 알려준다. 따라하면 된다.

---

## 그래도 직접 하고 싶으면

```bash
# 1. 클론
git clone https://github.com/yys5584/mylife-vault.git ~/MYLIFE
cd ~/MYLIFE

# 2. 의존성
pip install -r scripts/requirements.txt
#  → "command not found" 나면 pip3
#  → "Permission denied" 나면 끝에 --user

# 3. Claude Code 진입
claude

# 4. 인터뷰
> /mylife-setup
```

---

## 인터뷰 페이스

| 페이스 | 핵심 7개 | 도메인 확장 포함 | 보조(사주·별자리) 포함 |
|---|---|---|---|
| 빠르게 (한 줄 단답) | ~25분 | ~55분 | +10분 |
| 보통 (생각하며) | ~45분 | ~95분 | +10분 |
| 깊이 (사례·검증) | ~80분 | ~165분 | +15분 |

처음엔 빠르게로 일단 다 채우고 분기 갱신 때 깊이 보강 추천. 사주·별자리는 관심 있을 때만 채워도 된다.

중간에 멈추기: "여기까지 저장하고 다음에 계속" 말하면 Claude가 저장하고 종료.

---

## 인터뷰 끝난 후

```bash
cd ~/MYLIFE && claude
> "오늘 자문 해줘"
> "이 결정 어떻게 봐?"
> "이 메시지 보낼까?"
> "내 사주 일간 기준 2027년 어때?"   # (선택) 사주·별자리는 명시 요청 시에만 답함
```

vault 채워지면 어떤 LLM이든 이 폴더를 컨텍스트로 받으면 사용자 맞춤 답변을 한다. 답변의 1순위 근거는 사용자가 직접 채운 자기진단·철학·시스템이고, 사주·별자리는 명시 요청 시만 색깔로 얹힌다.

---

## 자주 막히는 케이스 — 3개만

Q. 사주 결과가 만세력 사이트랑 다름

- `--true-solar` 옵션 적용했는지 확인. 자시 경계(23~01시)면 1시간 단위로 미세 조정
- 회귀 테스트 64/64 통과해서 한국 만세력과 검증된 상태. 차이 크면 [Issues](https://github.com/yys5584/mylife-vault/issues) 리포트

Q. 출생 도시가 인식 안 됨 (제천·청주 등)

- 구글 지도에서 출생지 검색 → 우클릭 → 좌표 복사 → Claude에게 "위경도 직접: 37.1326, 128.1914" 전달

Q. 출생 시간 모름

- "모름"으로 진행. 사주는 시주만 빠지고 나머지 정확. 별자리는 태양궁만 정확하고 달궁·상승궁은 의미 없음

---

## 갱신 + 백업

```bash
cd ~/MYLIFE && claude
> "분기 갱신 모드로 /mylife-setup"
```

사용자 vault 백업 원하면 Claude한테 "이 vault 내 private GitHub repo로 push해줘" 시키기. private repo 이름만 정해주면 알아서 한다.

---

## 다음

- [README.md](README.md) — 검증 체계·Credits·Disclaimer
- [SETUP.md](SETUP.md) — 인터뷰 섹션별 질문
- [Issues](https://github.com/yys5584/mylife-vault/issues) — 문제·제안

---

## 한 줄

CLI는 Claude한테 시키는 인터페이스. 사용자가 손으로 칠 필요 없다.
