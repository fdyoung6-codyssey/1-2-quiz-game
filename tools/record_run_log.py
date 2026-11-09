"""실행 증거 자동 기록 스크립트

main.py를 실제로 실행하면서 미리 정한 입력을 차례대로 넣고,
화면에 출력된 내용을 그대로 docs/RUN_LOG.md에 기록한다.

- 실제 state.json은 건드리지 않도록 임시 폴더의 state.json을 사용한다.
- 사용자가 입력한 값은 프롬프트 뒤에 그대로 보이도록 기록한다.

실행 방법 (프로젝트 루트에서):
    python tools/record_run_log.py
"""

import builtins
import contextlib
import io
import os
import platform
import random
import sys
import tempfile
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import main  # noqa: E402  (프로젝트 루트의 main.py)

OUTPUT = os.path.join(ROOT, "docs", "RUN_LOG.md")


def run_scenario(inputs):
    """입력 목록을 차례대로 넣으며 main.main()을 실행하고 화면 출력을 문자열로 돌려준다.
    입력 목록에 예외 클래스(KeyboardInterrupt, EOFError)를 넣으면 그 시점에 예외를 발생시킨다."""
    queue = list(inputs)
    original_input = builtins.input

    def fake_input(prompt=""):
        if not queue:
            raise EOFError
        value = queue.pop(0)
        if isinstance(value, type) and issubclass(value, BaseException):
            name = "Ctrl+C" if value is KeyboardInterrupt else "Ctrl+Z, Enter (입력 종료)"
            print(f"{prompt}<{name}>")
            raise value
        print(f"{prompt}{value}")  # 사용자가 입력한 값도 화면에 보이게 기록
        return value

    buffer = io.StringIO()
    builtins.input = fake_input
    try:
        with contextlib.redirect_stdout(buffer):
            main.main()
    finally:
        builtins.input = original_input
    return buffer.getvalue().rstrip()


def main_record():
    random.seed(2026)  # 출제 순서를 매번 같게 만들어 기록을 재현할 수 있게 함
    temp_dir = tempfile.mkdtemp()
    main.STATE_FILE = os.path.join(temp_dir, "state.json")

    scenarios = []

    scenarios.append((
        "1. 첫 실행 · 메뉴 · 잘못된 입력 처리",
        "state.json이 없는 상태에서 실행 → 기본 퀴즈 사용. 글자, 범위 밖 숫자, 빈 입력, 앞뒤 공백을 차례로 입력.",
        run_scenario(["abc", "9", "", "  3  ", "6"]),
    ))

    scenarios.append((
        "2. 퀴즈 추가 (빈 입력 · 정답 번호 검증) → 목록 확인",
        "문제를 빈 칸으로 입력 → 다시 입력. 정답 번호에 0, abc 입력 → 다시 입력. 추가 후 목록이 6개인지 확인.",
        run_scenario([
            "2", "", "Git에서 브랜치를 합치는 명령어는?",
            "git merge", "git branch", "git log", "git status",
            "0", "abc", "1", "'합병하다'라는 뜻의 영어 단어입니다.",
            "3", "6",
        ]),
    ))

    scenarios.append((
        "3. 퀴즈 풀기 (문제 수 선택 · 랜덤 출제 · 힌트 · 정답/오답) → 점수와 기록 확인",
        "문제 수에 범위 밖 숫자(20) 입력 → 다시 입력. 3문제 풀기. 첫 문제에서 0을 눌러 힌트 사용.",
        run_scenario(["1", "20", "3", "0", "3", "2", "4", "4", "6"]),
    ))

    scenarios.append((
        "4. 프로그램 재시작 → 데이터 유지 확인",
        "다시 실행하면 저장된 퀴즈 6개, 최고 점수, 게임 기록을 불러옴.",
        run_scenario(["3", "4", "6"]),
    ))

    scenarios.append((
        "5. 퀴즈 삭제 (취소 → 삭제)",
        "6번 퀴즈를 n으로 취소한 뒤, 다시 y로 삭제. 목록이 5개로 줄어든 것을 확인.",
        run_scenario(["5", "6", "n", "5", "6", "y", "3", "6"]),
    ))

    scenarios.append((
        "6. Ctrl+C (KeyboardInterrupt) → 저장 후 안전 종료",
        "메뉴 선택 중 Ctrl+C. Traceback 없이 안내 메시지를 출력하고 저장 후 종료.",
        run_scenario(["3", KeyboardInterrupt]),
    ))

    scenarios.append((
        "7. 입력 종료 (EOFError) → 저장 후 안전 종료",
        "퀴즈 풀기 중 입력 스트림 종료(Windows: Ctrl+Z 후 Enter).",
        run_scenario(["1", "2", EOFError]),
    ))

    # 8. state.json 손상 → 백업 파일로 복구
    with open(main.STATE_FILE, "w", encoding="utf-8") as file:
        file.write('{"quizzes": [ 손상된 파일')
    scenarios.append((
        "8. state.json 손상 → 백업(state.json.bak)으로 복구",
        "state.json 내용을 일부러 깨뜨린 뒤 실행. 저장할 때마다 만들어 둔 백업 파일에서 복구.",
        run_scenario(["3", "6"]),
    ))

    # 9. state.json과 백업 모두 손상 → 기본 퀴즈로 복구
    for path in (main.STATE_FILE, main.get_backup_file()):
        with open(path, "w", encoding="utf-8") as file:
            file.write("깨진 파일")
    scenarios.append((
        "9. state.json과 백업 모두 손상 → 기본 퀴즈로 복구",
        "두 파일을 모두 깨뜨린 뒤 실행. 프로그램이 멈추지 않고 기본 퀴즈 5개로 시작.",
        run_scenario(["3", "6"]),
    ))

    # 10. 퀴즈가 하나도 없는 경우
    with open(main.STATE_FILE, "w", encoding="utf-8") as file:
        file.write('{"quizzes": [], "best_score": null, "history": []}')
    scenarios.append((
        "10. 퀴즈가 하나도 없는 경우 · 아직 풀지 않은 경우",
        "퀴즈 목록이 빈 파일로 실행. 풀기·목록·점수·삭제 모두 안내 메시지 출력.",
        run_scenario(["1", "3", "4", "5", "6"]),
    ))

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# 실행 로그 (RUN_LOG)",
        "",
        "`python tools/record_run_log.py`로 **main.py를 실제로 실행**하면서 기록한 화면 출력입니다.",
        "사용자가 입력한 값은 프롬프트 바로 뒤에 표시됩니다. (예: `선택: 3`)",
        "",
        f"- 기록 일시: {now}",
        f"- Python: {platform.python_version()} ({platform.system()})",
        "- 실제 state.json을 바꾸지 않도록 임시 폴더의 state.json으로 실행했습니다.",
        "- 출제 순서 재현을 위해 `random.seed(2026)`을 사용했습니다.",
        "",
        "## 목차",
        "",
    ]
    for title, _, _ in scenarios:
        lines.append(f"- {title}")
    lines.append("")

    for title, description, output in scenarios:
        lines += [f"## {title}", "", description, "", "```text", output, "```", ""]

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))
    print(f"✅ 실행 로그를 저장했습니다: {os.path.relpath(OUTPUT, ROOT)} (시나리오 {len(scenarios)}개)")


if __name__ == "__main__":
    main_record()
