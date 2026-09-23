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
3. 질문 12개 인터뷰 시작 — 10분 (자기진단·철학·시스템·로드맵)
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

## 인터뷰 10분

질문 12개를 4개씩 세 번 묻는다. 한 번에 번호 붙여서 답하면 된다.

- 라운드 1 (3분) — 지금 나: 생년월일·하는 일·강점 3개·약점 3개
- 라운드 2 (4분) — 어디로 가나: 1순위 한 단어와 진짜 이유·이루면 보이는 장면·2·3순위·5년 뒤
- 라운드 3 (3분) — 뭐가 무너뜨리나: 반복 루프·무너지기 전 신호·안 하면 무너지는 것·이번 분기 목표 3개

되물음은 없다. 답이 한 줄이어도 그대로 받는다. 모르는 건 "패스" 하면 빈 칸으로 두고 넘어간다.

연인·직업·투자 같은 확장 문서는 인터뷰에서 안 묻는다. 보고서 다음 메뉴에서 고르면 그때 질문 2~3개로 채운다. 사주·별자리는 원할 때만 따로 5분.

중간에 멈추기: "여기까지 저장하고 다음에 계속" 말하면 Claude가 저장하고 종료.

---

## 인터뷰 끝난 후

인터뷰가 끝나면 셋업 완료 보고서가 자동으로 나온다. 보고서 끝에 상황별 상담 예시가 붙어 있고, 고민을 그대로 던지면 vault 위에서 답한다.

```bash
cd ~/MYLIFE && claude
> "이직 제안이 왔어. 연봉은 20% 오르는데 초기 스타트업이야. 갈까?"
> "요즘 일이 손에 안 잡혀. 번아웃인지 봐줘"
> "만난 지 한 달 됐는데 서운한 게 쌓였어. 지금 말해도 될까?"
> "이번 달 매매 기록이야. 내 룰 어긴 거 있나 봐줘"
> "나와 맞는 연인 유형 봐줘"
> "사주로도 같이 봐줘"   # (선택) 사주·별자리는 명시 요청 시만 색깔로 얹힘
```

vault 채워지면 어떤 LLM이든 이 폴더를 컨텍스트로 받으면 사용자 맞춤 답변을 한다. 답변의 1순위 근거는 사용자가 직접 채운 자기진단·철학·시스템이고, 사주·별자리는 명시 요청 시만 색깔로 얹힌다.

---

## 자주 막히는 케이스 — 3개만

Q. 사주 결과가 만세력 사이트랑 다름

- `--true-solar` 옵션 적용했는지 확인. 자시 경계(23~01시)면 1시간 단위로 미세 조정
- 회귀 테스트 64/64 통과해서 한국 만세력과 검증된 상태. 차이 크면 [Issues](https://github.com/yys5584/mylife-vault/issues) 리포트

Q. 출생 도시가 인식 안 됨 (춘천·청주 등)

- 구글 지도에서 출생지 검색 → 우클릭 → 좌표 복사 → Claude에게 "위경도 직접: 37.8813, 127.7298" 전달

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
- [SETUP.md](SETUP.md) — 10분 인터뷰 질문 12개
- [Issues](https://github.com/yys5584/mylife-vault/issues) — 문제·제안

---

## 한 줄

CLI는 Claude한테 시키는 인터페이스. 사용자가 손으로 칠 필요 없다.
