"""Git 이력 증빙 자동 기록 스크립트

원격 저장소 주소, 브랜치, 커밋 개수, 커밋 그래프(git log --oneline --graph),
clone/pull/checkout/merge 기록(reflog)을 docs/GIT_HISTORY.md에 텍스트로 저장한다.

실행 방법 (프로젝트 루트에서, 모든 커밋/push를 마친 뒤):
    python tools/export_git_log.py
"""

import os
import subprocess
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(ROOT, "docs", "GIT_HISTORY.md")
CLONE_DIR = os.path.join(os.path.dirname(ROOT), "1-2-quiz-game-clone")


def git(args, cwd=ROOT):
    """git 명령을 실행하고 출력 문자열을 돌려준다 (한글 파일 이름이 깨지지 않게 설정)"""
    result = subprocess.run(
        ["git", "-c", "core.quotepath=false", *args],
        cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    return (result.stdout or result.stderr).rstrip()


def block(command, output):
    return [f"```text", f"$ {command}", output, "```", ""]


def main():
    commit_count = git(["rev-list", "--count", "HEAD"])
    merge_count = git(["rev-list", "--count", "--merges", "HEAD"])
    reflog_keywords = ("clone", "pull", "checkout", "merge", "commit (initial)")
    reflog = git(["reflog", "--date=iso"])
    reflog_lines = [line for line in reflog.splitlines() if any(k in line for k in reflog_keywords)]

    lines = [
        "# Git 이력 (GIT_HISTORY)",
        "",
        "`python tools/export_git_log.py`로 Git 명령을 실제로 실행해서 기록한 결과입니다.",
        "",
        f"- 기록 일시: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "- 원격 저장소: https://github.com/fdyoung6-codyssey/1-2-quiz-game",
        f"- 전체 커밋 수 (main 기준): **{commit_count}개**",
        f"- 병합(merge) 커밋 수: **{merge_count}개**",
        "",
        "## 1. 원격 저장소 연결 (push 대상)",
        "",
        *block("git remote -v", git(["remote", "-v"])),
        "## 2. 브랜치 목록 (로컬 + 원격)",
        "",
        *block("git branch -a", git(["branch", "-a"])),
        "## 3. 커밋 그래프 (브랜치 생성 · 병합 기록)",
        "",
        "`|\\` 는 브랜치가 갈라진 곳, `|/` 는 main으로 병합된 곳입니다.",
        "",
        *block("git log --oneline --graph --all", git(["log", "--oneline", "--graph", "--all"])),
        "## 4. 로컬과 원격(origin/main) 동기화 확인",
        "",
        *block("git status -sb", git(["status", "-sb"])),
        "## 5. checkout · merge · pull 기록 (reflog)",
        "",
        "작업 폴더에서 실제로 실행한 checkout, merge, pull 명령의 기록입니다.",
        "",
        *block("git reflog (checkout/merge/pull 줄만)", "\n".join(reflog_lines)),
    ]

    lines += ["## 6. clone 기록", ""]
    if os.path.isdir(CLONE_DIR):
        clone_reflog = git(["reflog", "--date=iso"], cwd=CLONE_DIR)
        lines += [
            "저장소를 별도 폴더(`1-2-quiz-game-clone`)에 clone한 뒤 수정 → commit → push 한 기록입니다.",
            "",
            *block("cd ..\\1-2-quiz-game-clone && git reflog", clone_reflog),
            *block("cd ..\\1-2-quiz-game-clone && git remote -v", git(["remote", "-v"], cwd=CLONE_DIR)),
        ]
    else:
        lines += ["clone 폴더(`../1-2-quiz-game-clone`)를 찾지 못했습니다.", ""]

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))
    print(f"✅ Git 이력을 저장했습니다: {os.path.relpath(OUTPUT, ROOT)} (커밋 {commit_count}개, 병합 {merge_count}개)")


if __name__ == "__main__":
    main()
