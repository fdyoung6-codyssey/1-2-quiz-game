# 🎯 나만의 퀴즈 게임

- **GitHub 저장소:** https://github.com/fdyoung6-codyssey/1-2-quiz-game
- **실행 증거:** [docs/RUN_LOG.md](docs/RUN_LOG.md) (실제 실행 화면 로그 10개 시나리오)
- **Git 이력 증거:** [docs/GIT_HISTORY.md](docs/GIT_HISTORY.md) (커밋 그래프, 브랜치, clone/pull 기록)
- **성능 측정:** [docs/PERFORMANCE.md](docs/PERFORMANCE.md) (100 / 1,000 / 10,000개 측정)
- **스크린샷:** [docs/screenshots/](docs/screenshots/)

## 1. 프로젝트 개요

터미널에서 실행하는 **Python 콘솔 퀴즈 게임**입니다.
메뉴에서 번호를 선택해 퀴즈를 풀고, 새 퀴즈를 추가·삭제하고, 최고 점수와 게임 기록을 확인할 수 있습니다.
퀴즈, 최고 점수, 게임 기록은 `state.json` 파일에 저장되어 프로그램을 종료한 뒤 다시 실행해도 유지됩니다.

## 2. 퀴즈 주제와 선정 이유

- **주제:** Python · Git 기초
- **선정 이유:** 이번 미션에서 배우는 Python 문법(함수, 리스트, 클래스, 예외 처리)과
  Git 명령어(add, commit, push, pull 등)를 퀴즈로 풀어 보며 스스로 복습하기 위해 선택했습니다.

### 기본 퀴즈 목록 (state.json이 없을 때 사용)

| 번호 | 문제 | 정답 |
|---:|---|---|
| 1 | Python에서 화면에 글자를 출력하는 함수는? | 2. `print()` |
| 2 | Python에서 리스트(list)를 만드는 올바른 방법은? | 2. `[1, 2, 3]` |
| 3 | 클래스로 객체를 만들 때 자동으로 실행되는 메서드는? | 3. `__init__` |
| 4 | Git에서 변경 내용을 기록(저장)하는 명령어는? | 2. `git commit` |
| 5 | GitHub(원격 저장소)의 변경사항을 내 컴퓨터로 가져오는 명령어는? | 3. `git pull` |

## 3. 실행 방법

### 개발 환경
- Python 3.10 이상
- 외부 라이브러리 없음 (표준 라이브러리 `json`, `os`, `random`, `shutil`, `datetime`만 사용)

### 실행
```bash
git clone https://github.com/fdyoung6-codyssey/1-2-quiz-game.git
cd 1-2-quiz-game
python main.py
```

### 테스트 · 증빙 자료 만들기
```bash
python -m unittest discover -s tests -v   # 자동 테스트 15개
python tools/record_run_log.py            # 실제 실행 로그 → docs/RUN_LOG.md
python tools/benchmark.py                 # 성능 측정 → docs/PERFORMANCE.md
python tools/export_git_log.py            # Git 이력 → docs/GIT_HISTORY.md
```

### 실행 예시 (요약)

전체 로그는 [docs/RUN_LOG.md](docs/RUN_LOG.md)에 있습니다.

```text
선택: abc
⚠️ 잘못된 입력입니다. 1-6 사이의 숫자를 입력하세요.
선택: 1

몇 문제를 풀까요? (1-6): 3

[문제 1]
GitHub(원격 저장소)의 변경사항을 내 컴퓨터로 가져오는 명령어는?

  1. git push
  2. git init
  3. git pull
  4. git checkout

정답 입력 (힌트: 0): 0
💡 힌트: '당기다'라는 뜻의 영어 단어입니다.
정답 입력: 3
✅ 정답입니다! (힌트 사용: 0.5점)
```

## 4. 기능 목록

| 메뉴 | 기능 | 설명 |
|---|---|---|
| 1 | 퀴즈 풀기 | 풀 문제 수를 고르면 문제를 무작위 순서로 출제하고 정답/오답과 최종 점수를 보여줌 |
| 2 | 퀴즈 추가 | 문제, 선택지 4개, 정답 번호, 힌트(선택)를 입력받아 등록 후 파일에 저장 |
| 3 | 퀴즈 목록 | 등록된 퀴즈 문제를 번호와 함께 출력 |
| 4 | 점수 확인 | 최고 점수와 최근 10회 게임 기록 출력 |
| 5 | 퀴즈 삭제 | 번호를 골라 확인(y/n) 후 삭제하고 파일에 반영 |
| 6 | 종료 | 데이터를 저장하고 프로그램 종료 |

### 보너스 기능
| 보너스 | 기능 | 설명 |
|---|---|---|
| 1 | 랜덤 출제 | `random.shuffle()`로 문제 순서를 섞음 (원래 목록 순서는 유지) |
| 2 | 문제 수 선택 | 퀴즈를 시작할 때 몇 문제를 풀지 선택 |
| 3 | 힌트 | 정답 입력에서 `0`을 누르면 힌트 표시, 힌트를 보고 맞히면 0.5점 |
| 4 | 퀴즈 삭제 | 삭제 전 한 번 더 확인하고 삭제 결과를 파일에 반영 |
| 5 | 게임 기록 히스토리 | 게임마다 날짜·시간, 푼 문제 수, 맞힌 수, 점수, 힌트 사용 횟수를 저장 |

### 입력 / 예외 처리
- 입력값 앞뒤 공백 제거 후 처리
- 숫자가 아닌 입력, 범위 밖 숫자, 빈 입력 → 안내 메시지 후 다시 입력
- `Ctrl+C`(KeyboardInterrupt), 입력 종료(EOFError) → 데이터 저장 후 안전하게 종료
- `state.json`이 없으면 기본 퀴즈로 시작
- `state.json`이 손상되었으면 **백업(`state.json.bak`)에서 복구**, 백업도 손상되었으면 기본 퀴즈로 복구
- 저장 실패(권한 문제, 다른 프로그램이 파일 사용 중 등) 시 원인과 조치 방법 안내

## 5. 파일 구조

```
1-2-quiz-game/
├── main.py                 # 프로그램 전체 코드 (Quiz, QuizGame 클래스)
├── state.json              # 퀴즈 목록, 최고 점수, 게임 기록 저장 파일 (자동 생성)
├── state.json.bak          # 저장 직전 상태 백업 (자동 생성, Git 제외)
├── README.md               # 프로젝트 설명서
├── .gitignore              # Git에 올리지 않을 파일 목록
├── tests/
│   └── test_quiz_game.py   # 자동 테스트 (unittest)
├── tools/
│   ├── record_run_log.py   # 실행 로그 자동 기록
│   ├── benchmark.py        # 성능 측정
│   └── export_git_log.py   # Git 이력 기록
└── docs/
    ├── RUN_LOG.md          # 실행 증거
    ├── GIT_HISTORY.md      # Git 이력 증거
    ├── PERFORMANCE.md      # 성능 측정 결과
    └── screenshots/        # 실행 화면 스크린샷
```

## 6. 클래스 설계

### 클래스를 사용한 이유
- **추상화:** "퀴즈 한 문제"와 "게임 전체"를 각각 하나의 객체로 표현해, 코드를 읽을 때 무엇을 다루는지 바로 알 수 있습니다.
- **재사용성:** `Quiz` 틀 하나로 기본 퀴즈, 사용자가 추가한 퀴즈, 파일에서 불러온 퀴즈를 모두 같은 방식으로 만들고 사용합니다.
- **변경에 강함:** 힌트 기능을 추가할 때 `Quiz`에 `hint` 속성 하나만 더하면 출력·저장·불러오기가 모두 같은 객체를 쓰므로 수정 범위가 작았습니다.

### 클래스별 책임

| 클래스 | 책임 (하는 일) | 하지 않는 일 | 주요 메서드 |
|---|---|---|---|
| `Quiz` | 퀴즈 한 문제의 데이터(문제, 선택지, 정답, 힌트)를 가지고, 자신을 출력·채점·딕셔너리로 변환 | 입력 받기, 파일 저장 | `display()`, `is_correct()`, `to_dict()` |
| `QuizGame` | 퀴즈 목록·최고 점수·기록을 관리하고, 메뉴 진행·입력 검증·파일 저장/불러오기/백업을 담당 | 개별 문제의 채점 규칙 | `run()`, `play_quiz()`, `add_quiz()`, `show_quiz_list()`, `show_score()`, `delete_quiz()`, `load_data()`, `save_data()` |

### 주요 메서드의 입력 · 출력 · 부작용

| 메서드 | 입력 | 출력 (돌려주는 값) | 부작용 |
|---|---|---|---|
| `Quiz.is_correct(n)` | 사용자가 고른 번호 | `True` / `False` | 없음 |
| `Quiz.to_dict()` | 없음 | 저장용 딕셔너리 | 없음 |
| `get_number(prompt, min, max)` | 안내 문구, 허용 범위 | 올바른 정수 | 잘못된 입력 시 안내 출력 |
| `get_text(prompt)` | 안내 문구 | 비어 있지 않은 문자열 | 빈 입력 시 안내 출력 |
| `play_quiz()` | 키보드 입력 | 없음 | 점수·기록 갱신, 파일 저장 |
| `add_quiz()` / `delete_quiz()` | 키보드 입력 | 없음 | 퀴즈 목록 변경, 파일 저장 |
| `load_data()` | `state.json` (없으면 `.bak`) | 없음 | 퀴즈·점수·기록을 메모리에 적용 |
| `save_data()` | 메모리의 데이터 | 없음 | `.bak` 백업 생성 후 `state.json` 덮어쓰기 |

## 7. 데이터 파일 설명 (state.json)

- **경로:** 프로젝트 루트 (`main.py`와 같은 폴더)
- **인코딩:** UTF-8
- **역할:** 퀴즈 목록, 최고 점수, 게임 기록을 저장하여 프로그램을 다시 실행해도 데이터 유지
- **불러오는 시점:** 프로그램 시작 시 (`QuizGame()` 생성 → `load_data()`)
- **저장 시점:** 퀴즈 추가·삭제 후, 게임이 끝날 때, 프로그램 종료 시(Ctrl+C 포함)

### JSON을 선택한 이유
| 방식 | 장점 | 단점 |
|---|---|---|
| **JSON (선택)** | 표준 라이브러리만으로 읽고 쓰기 가능, 리스트·딕셔너리 구조와 같아 변환이 쉬움, 사람이 열어서 읽을 수 있음 | 파일 전체를 다시 써야 함 |
| 텍스트(txt) | 단순함 | 문제·선택지·정답을 구분하는 규칙을 직접 만들어야 함 |
| CSV | 표 형태에 적합 | 선택지 리스트, 기록 같은 중첩 구조 표현이 어려움 |
| SQLite | 대용량·검색에 강함 | 이 규모에는 과함, SQL 학습 필요 |

### 필드 구조

| 키 | 형태 | 설명 |
|---|---|---|
| `quizzes` | 리스트 | 퀴즈 목록 |
| `quizzes[].question` | 문자열 | 문제 |
| `quizzes[].choices` | 문자열 4개 리스트 | 선택지 |
| `quizzes[].answer` | 정수 (1~4) | 정답 번호 |
| `quizzes[].hint` | 문자열 | 힌트 (없으면 빈 문자열) |
| `best_score` | 정수 또는 null | 최고 점수 (100점 만점, 아직 풀지 않았으면 null) |
| `history` | 리스트 | 게임 기록 목록 |
| `history[].date` | 문자열 | 게임한 날짜·시간 (예: `2026-11-09 18:06`) |
| `history[].total` | 정수 | 푼 문제 수 |
| `history[].correct` | 정수 | 맞힌 문제 수 |
| `history[].score` | 정수 | 점수 |
| `history[].hints` | 정수 | 힌트 사용 횟수 |

### 예시

```json
{
    "quizzes": [
        {
            "question": "Python에서 화면에 글자를 출력하는 함수는?",
            "choices": ["input()", "print()", "len()", "str()"],
            "answer": 2,
            "hint": "화면에 '출력'한다는 영어 단어를 떠올려 보세요."
        }
    ],
    "best_score": 100,
    "history": [
        {
            "date": "2026-11-09 18:06",
            "total": 9,
            "correct": 9,
            "score": 100,
            "hints": 0
        }
    ]
}
```

### 백업과 복구

| 상황 | 프로그램 동작 | 사용자가 할 일 |
|---|---|---|
| `state.json` 없음 (첫 실행) | 기본 퀴즈 5개로 시작 | 없음 |
| `state.json` 손상 | `state.json.bak`(직전 저장 상태)에서 자동 복구 후 다시 저장 | 없음 |
| `state.json`, `.bak` 모두 손상 | 기본 퀴즈로 초기화 | 필요하면 GitHub의 `state.json`을 내려받아 교체 |
| 저장 실패 (권한, 파일 잠김) | 오류 원인과 조치 방법 출력, 이전 데이터는 `.bak`에 유지 | 파일을 연 프로그램 닫기, 읽기 전용 해제 후 다시 실행 |

- **백업 시점:** `save_data()`가 `state.json`을 덮어쓰기 **직전에** 기존 파일을 `state.json.bak`으로 복사합니다.
- **수동 복원 방법:** 프로그램을 종료한 뒤 `state.json.bak`을 복사해서 이름을 `state.json`으로 바꾸면 됩니다.

## 8. 성능

[docs/PERFORMANCE.md](docs/PERFORMANCE.md)에 100 / 1,000 / 10,000개 퀴즈로 측정한 저장·불러오기·목록·검색 시간과 메모리 사용량을 정리했습니다.
1,000개 기준으로 저장·불러오기 모두 수 밀리초(ms) 수준이며, 자동 테스트에서도 1,000개 저장·불러오기가 1초 안에 끝나는지 확인합니다.

## 9. 유지보수 가이드 (요구사항이 바뀔 때 수정할 곳)

| 바꾸고 싶은 것 | 수정할 곳 | 영향 범위 |
|---|---|---|
| 퀴즈에 새 정보 추가 (예: 난이도) | `Quiz.__init__`, `Quiz.to_dict()`, `QuizGame.read_state_file()`, `add_quiz()` | state.json 필드 추가 → README 필드 표도 수정 |
| 선택지 개수 변경 (4개 → 5개) | `add_quiz()`의 `range(1, 5)`, `play_quiz()`의 `get_number(..., 0, 4)` | 기본 퀴즈 데이터도 함께 수정 |
| 점수 계산 방식 변경 | `play_quiz()`의 `points`, `score` 계산 부분 | 최고 점수·기록 의미가 바뀜 |
| 메뉴 추가 | `show_menu()`, `run()`의 `get_number("선택: ", 1, N)`과 `elif` | 메뉴 번호가 바뀌면 README 기능 표 수정 |
| 저장 위치 / 형식 변경 | `STATE_FILE`, `load_data()`, `save_data()`, `read_state_file()` | 다른 메서드는 수정 불필요 (저장 책임이 한곳에 모여 있음) |
| 입력 검증 규칙 변경 | `get_number()`, `get_text()` | 모든 메뉴에 한꺼번에 적용 |

수정한 뒤에는 `python -m unittest discover -s tests -v`로 테스트를 실행해 기존 기능이 깨지지 않았는지 확인합니다.

## 10. Git 작업 규칙

### 커밋 단위
- **기능 하나를 완성하면 커밋 1개** (예: 메뉴, Quiz 클래스, 퀴즈 풀기, 추가, 목록, 점수, 저장, README)
- 실행해서 동작을 확인한 뒤에만 커밋
- 새 기능은 `feature/기능이름` 브랜치에서 개발하고, 완성 후 `git merge --no-ff`로 `main`에 병합 (병합 기록을 그래프에 남기기 위해)

### 커밋 메시지 템플릿
```
<종류>: <무엇을 했는지 한 줄 요약> (<세부 내용>)
```

| 종류 | 의미 | 이 저장소의 실제 예시 |
|---|---|---|
| `Feat` | 새 기능 | `Feat: 퀴즈 풀기 기능 구현(정답/오답 표시, 결과 출력)` |
| `Fix` | 오류 수정 | `Fix: README 파일명 오타 수정` |
| `Docs` | 문서 수정 | `Docs: README 작성 (개요, 주제, 실행 방법, 기능, 파일 구조, 데이터 설명)` |
| `Refactor` | 동작은 같고 구조만 개선 | `Refactor: QuizGame 저장 로직 분리` |
| `Test` | 테스트 추가 | `Test: 입력 검증·저장·백업 자동 테스트 추가` |
| `Merge` | 브랜치 병합 | `Merge: feature/play-quiz 브랜치 병합 (퀴즈 풀기 기능)` |

### 사용한 브랜치
`feature/play-quiz`, `feature/play-options`, `feature/delete-quiz`, `feature/hint`, `feature/history`, `feature/evidence`

## 11. Git 실습 기록

자세한 명령 결과는 [docs/GIT_HISTORY.md](docs/GIT_HISTORY.md)에 있습니다.

- 기능 단위로 커밋하고, 기능별 브랜치에서 개발한 뒤 `main`에 병합함
- `git clone`으로 저장소를 별도 폴더(1-2-quiz-game-clone)에 복제하여 README를 수정하고 push함
- 원래 작업 폴더에서 `git pull`로 변경사항을 가져와 반영을 확인함
- 사용한 Git 명령어: `init`, `add`, `commit`, `push`, `pull`, `checkout`, `clone`, `merge`
