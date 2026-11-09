# Git 이력 (GIT_HISTORY)

`python tools/export_git_log.py`로 Git 명령을 실제로 실행해서 기록한 결과입니다.

- 기록 일시: 2026-11-09 19:41
- 원격 저장소: https://github.com/fdyoung6-codyssey/1-2-quiz-game
- 전체 커밋 수 (main 기준): **31개**
- 병합(merge) 커밋 수: **6개**

## 1. 원격 저장소 연결 (push 대상)

```text
$ git remote -v
origin	https://github.com/fdyoung6-codyssey/1-2-quiz-game.git (fetch)
origin	https://github.com/fdyoung6-codyssey/1-2-quiz-game.git (push)
```

## 2. 브랜치 목록 (로컬 + 원격)

```text
$ git branch -a
  feature/delete-quiz
  feature/evidence
  feature/hint
  feature/history
  feature/play-options
  feature/play-quiz
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/feature/delete-quiz
  remotes/origin/feature/evidence
  remotes/origin/feature/hint
  remotes/origin/feature/history
  remotes/origin/feature/play-options
  remotes/origin/feature/play-quiz
  remotes/origin/main
```

## 3. 커밋 그래프 (브랜치 생성 · 병합 기록)

`|\` 는 브랜치가 갈라진 곳, `|/` 는 main으로 병합된 곳입니다.

```text
$ git log --oneline --graph --all
*   54d2fa5 Merge: feature/evidence 병합 (평가 보완)
|\  
| * c0d0bbb Docs: README 보완 (클래스 설계, 커밋 규칙, 백업, 유지보수 가이드)
| * ab168fe Docs: 실행 로그와 성능 측정 결과를 마크다운으로 기록
| * c331569 Test: 입력 검증·저장·백업·1000개 성능 자동 테스트 추가
| * 66fadd9 Feat: 저장 전 자동 백업 및 손상 시 백업 복구 기능 추가
|/  
* 6d4f01e Docs: README 파일 구조에 docs/screenshots 추가
* 8334c53 Docs: 실행 화면 스크린샷 추가 (docs/screenshots)
* 58266ce Docs: README에 보너스 기능과 state.json 필드(hint, history) 반영
*   67f2bd2 Merge: feature/history 병합 (점수 기록 히스토리)
|\  
| * 338f71b Feat: 게임 기록 히스토리 기능 추가 (날짜, 문제 수, 점수, 힌트) (보너스 5)
|/  
*   8fdb9b6 Merge: feature/hint 병합 (힌트 기능)
|\  
| * 4ef95d1 Feat: 힌트 기능 추가 (0 입력 시 힌트, 사용 시 0.5점) (보너스 3)
|/  
*   4b0b16b Merge: feature/delete-quiz 병합 (퀴즈 삭제)
|\  
| * c3a57de Feat: 퀴즈 삭제 기능 추가 (삭제 확인, 파일 반영) (보너스 4)
|/  
*   0803023 Merge: feature/play-options 병합 (랜덤 출제, 문제 수 선택)
|\  
| * 37d069d Feat: 풀 문제 수 선택 기능 추가 (보너스 2)
| * eaa59ee Feat: 퀴즈 랜덤 출제 기능 추가 (보너스 1)
|/  
* 18704fc Docs: README에 clone/pull 실습 기록 추가
* 7aded8c Docs: README 작성 (개요, 주제, 실행 방법, 기능, 파일 구조, 데이터 설명)
* 50de16a Feat: Ctrl+C, EOF 입력 중단 시 저장 후 안전 종료 처리
* b6e2a65 Feat: state.json 파일 저장/불러오기 기능 구현 (UTF-8, 손상 시 복구)
* 24680b6 Feat: 점수 확인 기능 구현 (최고 점수 갱신)
* cf65d36 Feat: 퀴즈 추가 기능 구현 (빈 입력, 정답 번호 검증 포함)
* 983edda Feat: 퀴즈 목록 기능 구현
*   be0c4df Merge: feature/play-quiz 브랜치 병합 (퀴즈 풀기 기능)
|\  
| * a0e22e6 Feat: 퀴즈 풀기 기능 구현(정답/오답 표시, 결과 출력)
|/  
* dc2ab36 Feat: QuizGame 클래스와 메인 메뉴 구현(잘못된 입력 처리 포함)
* c9cdae8 Feat: 기본 퀴즈 데이터 5개 작성(Python.Git 기초)
* 3a68803 Feat: Quiz 클래스 작성 (문제 출력, 정답 확인)
* dfcb2ec Fix: README 파일명 오타 수정
* 3bddc83 init: 프로젝트 초기 구조 생성(README, .gitignore, main.py)
```

## 4. 로컬과 원격(origin/main) 동기화 확인

```text
$ git status -sb
## main...origin/main
```

## 5. checkout · merge · pull 기록 (reflog)

작업 폴더에서 실제로 실행한 checkout, merge, pull 명령의 기록입니다.

```text
$ git reflog (checkout/merge/pull 줄만)
54d2fa5 HEAD@{2026-11-09 19:40:54 +0900}: merge feature/evidence: Merge made by the 'ort' strategy.
6d4f01e HEAD@{2026-11-09 19:40:49 +0900}: checkout: moving from feature/evidence to main
6d4f01e HEAD@{2026-11-09 19:34:18 +0900}: checkout: moving from main to feature/evidence
67f2bd2 HEAD@{2026-11-09 18:09:18 +0900}: merge feature/history: Merge made by the 'ort' strategy.
8fdb9b6 HEAD@{2026-11-09 18:09:14 +0900}: checkout: moving from feature/history to main
8fdb9b6 HEAD@{2026-11-09 18:01:28 +0900}: checkout: moving from main to feature/history
8fdb9b6 HEAD@{2026-11-09 18:00:38 +0900}: merge feature/hint: Merge made by the 'ort' strategy.
4b0b16b HEAD@{2026-11-09 18:00:33 +0900}: checkout: moving from feature/hint to main
4b0b16b HEAD@{2026-11-09 17:52:27 +0900}: checkout: moving from main to feature/hint
4b0b16b HEAD@{2026-11-09 17:51:07 +0900}: merge feature/delete-quiz: Merge made by the 'ort' strategy.
0803023 HEAD@{2026-11-09 17:51:01 +0900}: checkout: moving from feature/delete-quiz to main
0803023 HEAD@{2026-11-09 17:35:39 +0900}: checkout: moving from main to feature/delete-quiz
0803023 HEAD@{2026-11-09 17:33:14 +0900}: checkout: moving from main to main
0803023 HEAD@{2026-11-09 17:30:45 +0900}: merge feature/play-options: Merge made by the 'ort' strategy.
18704fc HEAD@{2026-11-09 17:30:38 +0900}: checkout: moving from feature/play-options to main
18704fc HEAD@{2026-11-09 17:17:34 +0900}: checkout: moving from main to feature/play-options
18704fc HEAD@{2026-11-09 17:11:57 +0900}: pull: Fast-forward
be0c4df HEAD@{2026-11-09 14:42:56 +0900}: merge feature/play-quiz: Merge made by the 'ort' strategy.
dc2ab36 HEAD@{2026-11-09 14:42:47 +0900}: checkout: moving from feature/play-quiz to main
dc2ab36 HEAD@{2026-11-09 14:26:42 +0900}: checkout: moving from main to feature/play-quiz
3bddc83 HEAD@{2026-11-09 14:10:13 +0900}: commit (initial): init: 프로젝트 초기 구조 생성(README, .gitignore, main.py)
```

## 6. clone 기록

저장소를 별도 폴더(`1-2-quiz-game-clone`)에 clone한 뒤 수정 → commit → push 한 기록입니다.

```text
$ cd ..\1-2-quiz-game-clone && git reflog
18704fc HEAD@{2026-11-09 17:11:37 +0900}: commit: Docs: README에 clone/pull 실습 기록 추가
7aded8c HEAD@{2026-11-09 17:09:30 +0900}: clone: from https://github.com/fdyoung6-codyssey/1-2-quiz-game.git
```

```text
$ cd ..\1-2-quiz-game-clone && git remote -v
origin	https://github.com/fdyoung6-codyssey/1-2-quiz-game.git (fetch)
origin	https://github.com/fdyoung6-codyssey/1-2-quiz-game.git (push)
```
