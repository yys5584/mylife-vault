# QUICKSTART — CLI 초보자 가이드

> 터미널은 써봤지만 Python 설치·git·pip 같은 거 익숙하지 않은 분용. 끝까지 가면 30분 내로 본인 사주·별자리 + 인생 vault 완성.

---

## 0. 사전 준비 — 본인 정보 메모

시작 전 다음 정보 메모장에 적어두세요. 인터뷰 중 물어봅니다.

- 양력 생년월일 (YYYY-MM-DD)
- 출생 시간 (24시간 형식, 모르면 "모름")
- 출생 도시 (시·구 까지)
- 성별 (남/여)
- 거주지
- 직업·소득 구조
- 가족 구성

---

## 1. Python 설치 (이미 있으면 건너뛰기)

### 확인 — 이미 깔려있는지 체크

터미널 열고:
```bash
python --version
# 또는
python3 --version
```

→ `Python 3.10` 이상 나오면 OK. 없으면:

### Mac
```bash
# Homebrew 있으면
brew install python@3.12

# Homebrew 없으면 https://brew.sh/ 한 줄 설치 후 위 명령
```

### Windows
1. https://www.python.org/downloads/ 접속
2. "Download Python 3.12.x" 클릭
3. 설치 시 **"Add Python to PATH"** 체크 (중요!)
4. 설치 끝나면 새 터미널 (cmd 또는 PowerShell) 열기

### Linux (Ubuntu·Debian)
```bash
sudo apt update && sudo apt install python3 python3-pip python3-venv
```

### 검증
```bash
python --version    # Mac/Win
python3 --version   # Linux/Mac (둘 다 시도)
pip --version       # 또는 pip3 --version
```

둘 다 버전 나오면 통과.

---

## 2. Claude Code 또는 Codex CLI 설치

둘 중 *하나*만 있으면 됩니다. 처음이면 **Claude Code 추천** (UX 더 매끄러움).

### Claude Code (추천)
1. https://claude.com/claude-code 접속
2. 본인 OS 설치 파일 다운로드
3. 설치 후 터미널에서:
   ```bash
   claude --version
   ```
   버전 나오면 완료.
4. 처음 실행 시 `claude` 입력 → 브라우저 인증 1회 (Anthropic 계정 필요. 없으면 가입)

### Codex CLI (대안)
```bash
# npm 있으면
npm install -g @openai/codex

# 설치 후
codex --version
```

OpenAI API 키 또는 ChatGPT 로그인 필요.

---

## 3. 이 vault 다운로드

터미널 어디서든 (홈 폴더 권장):

```bash
cd ~                                                          # 홈 폴더로
git clone https://github.com/yys5584/mylife-vault.git MYLIFE  # 다운로드
cd MYLIFE                                                     # 폴더 진입
```

`git`이 없으면:
- Mac: `brew install git` 또는 Xcode Command Line Tools
- Windows: https://git-scm.com/download/win 설치
- 혹은 GitHub 페이지에서 Code → Download ZIP → 압축 풀기 (`cd ~/MYLIFE` 대신 압축 푼 경로로 이동)

---

## 4. 사주·별자리 라이브러리 설치

```bash
pip install -r scripts/requirements.txt
```

**자주 막히는 곳**:
- `pip` 없다고 나오면 → `pip3`로 시도
- 권한 에러 (`Permission denied`) → 끝에 `--user` 추가:
  ```bash
  pip install --user -r scripts/requirements.txt
  ```
- 가상환경 쓰는 게 정석이지만 처음이면 그냥 위처럼 전역 설치도 OK

설치 확인:
```bash
python -c "import sajupy, lunar_python, skyfield, ephem; print('OK')"
```

`OK` 출력되면 통과.

---

## 5. 본인 사주·별자리 미리 계산 (옵션, 인터뷰 중에도 가능)

```bash
# 사주 — 본인 정보로 바꿔서 실행
python scripts/calc_saju.py \
  --date 1990-03-15 \
  --time 14:30 \
  --gender male \
  --place "Seoul" \
  --true-solar

# 별자리
python scripts/calc_zodiac.py \
  --date 1990-03-15 \
  --time 14:30 \
  --place "Seoul"
```

**도시가 인식 안 되면** (제천·청주 등 중소도시):
1. 구글 지도에서 출생지 검색
2. 우클릭 → 좌표 복사 (예: `37.1326, 128.1914`)
3. 위경도 직접 입력:
   ```bash
   python scripts/calc_saju.py --date 1990-03-15 --time 14:30 --gender male \
     --longitude 128.1914 --true-solar
   python scripts/calc_zodiac.py --date 1990-03-15 --time 14:30 \
     --lat 37.1326 --lon 128.1914 --tz 9
   ```

성공하면 `templates/saju.md`와 `templates/zodiac.md`가 자동으로 채워짐.

**출생 시간 모름**: `--time unknown` 사용. 사주는 시주만 빠지고, 별자리는 태양궁만 정확 (달궁·상승궁 의미 없음).

---

## 6. 인터뷰 시작

```bash
claude    # 또는 codex
```

Claude Code가 열리면:

```
/mylife-setup
```

→ Claude가 순서대로 질문 시작. 답하면 12개 마크다운 파일이 자동으로 채워짐.

**페이스**:
- **빠르게 (~30분)**: 한 줄 단답으로 핵심만 — 처음엔 이거 추천
- **보통 (~50분)**: 생각하며 답
- **깊이 (~90분)**: 사례·검증·후속 질문 받으며

처음 채울 땐 *빠르게*로 일단 다 채우고, 나중에 분기 갱신 때 깊이 보강하는 게 정신건강에 좋음.

**중간에 멈추기**: "여기까지 저장하고 다음에 계속" 말하면 됨. Claude가 채워진 부분 저장하고 종료.

---

## 7. 인터뷰 끝난 후

vault 채워졌으니 어떤 LLM이든 이 폴더 컨텍스트로 받으면 본인 맞춤 답변.

**Claude Code에서**:
```bash
cd ~/MYLIFE
claude

> "오늘 자문 해줘"
> "이 결정 어떻게 봐?"
> "이 메시지 보낼까?"
> "내 사주 일간 기준 2027년 어때?"
```

**다른 LLM (Claude.ai 웹·ChatGPT 등)에서**: `templates/` 안 파일 내용을 복사 → 채팅에 붙여넣기 → "이 컨텍스트로 답해줘"

---

## 자주 발생하는 문제

### Q. `python: command not found`
- Mac/Linux: `python3`로 대신 시도
- Windows: 설치 시 "Add to PATH" 체크 안 했음. Python 재설치하며 체크하기

### Q. `pip install` 권한 에러
- `--user` 플래그 추가:
  ```bash
  pip install --user -r scripts/requirements.txt
  ```

### Q. `claude` / `codex` 명령 못 찾음
- 설치 후 새 터미널 창 열기 (PATH 갱신용)
- Claude Code 설치 경로가 PATH에 들어갔는지 확인

### Q. de421.bsp 다운로드가 너무 오래 걸림
- 17MB짜리 NASA 천문 데이터. 첫 1회만 받으면 됨. 인터넷 안 좋으면 5-10분 걸림.

### Q. 사주 결과가 만세력 사이트와 다름
- 회귀 테스트 64/64 통과 상태로 한국 만세력과 검증됨. 차이 있으면:
  1. 진태양시 보정 옵션 (`--true-solar`) 사용했는지 확인
  2. 출생 시간이 야자시(23:00-01:00) 경계면 1시간 단위로 미세 조정
  3. 그래도 다르면 [Issues](https://github.com/yys5584/mylife-vault/issues)에 리포트

### Q. `/mylife-setup` 슬래시 명령 안 먹음
- Claude Code 안에서 *프롬프트 입력 첫 글자*가 `/`이어야 함
- 이 vault 폴더 안에서 실행했는지 확인 (`pwd`로 경로 체크, 끝이 `MYLIFE`여야)

### Q. 인터뷰 도중 막힘
- "이 질문 잘 모르겠어" 라고 말하면 Claude가 reframe해줌
- 그래도 막히면 "모름"으로 답하고 다음 섹션으로

---

## 갱신 + 백업

### 분기 1회 갱신
```bash
cd ~/MYLIFE
claude
> "분기 갱신 모드로 /mylife-setup"
```

### 백업 (선택, 본인 데이터 보호용)
본인 채운 vault는 *민감 정보*. private repo로 백업하려면:
```bash
cd ~/MYLIFE
git remote remove origin
git remote add origin https://github.com/<본인id>/<my-vault-private>.git
# 새 private repo는 GitHub 웹에서 미리 생성
git push -u origin main
```

### 템플릿 업데이트 받기
```bash
cd ~/MYLIFE
git remote add upstream https://github.com/yys5584/mylife-vault.git
git fetch upstream
git merge upstream/main
# 충돌 시 본인 templates/ 안 데이터 우선 보존
```

---

## 다음 단계

- [README.md](README.md) — 전체 개요 + 검증 체계
- [SETUP.md](SETUP.md) — 인터뷰 섹션별 상세 질문
- [CLAUDE.md](CLAUDE.md) — AI 에이전트 룰 (LLM이 답할 때 따르는 규칙)

문제·제안: https://github.com/yys5584/mylife-vault/issues
