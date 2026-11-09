"""대용량 성능 측정 스크립트

퀴즈를 100개, 1,000개, 10,000개로 늘려 가며
저장(save_data) · 불러오기(load_data) · 목록 출력 · 키워드 검색 시간과
메모리 사용량(tracemalloc), state.json 파일 크기를 측정해 docs/PERFORMANCE.md에 기록한다.

- 실제 state.json은 건드리지 않도록 임시 폴더를 사용한다.

실행 방법 (프로젝트 루트에서):
    python tools/benchmark.py
"""

import contextlib
import io
import os
import platform
import sys
import tempfile
import time
import tracemalloc
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import main  # noqa: E402

OUTPUT = os.path.join(ROOT, "docs", "PERFORMANCE.md")
SIZES = [100, 1_000, 10_000]
REPEAT = 5  # 각 측정을 5번 반복해서 평균을 낸다


def make_quizzes(count):
    return [
        main.Quiz(
            f"성능 테스트 문제 {i}번: Python 리스트에 항목을 추가하는 메서드는?",
            ["insert()", "append()", "add()", "push()"],
            2,
            f"힌트 {i}",
        )
        for i in range(count)
    ]


def average_ms(func):
    times = []
    for _ in range(REPEAT):
        start = time.perf_counter()
        func()
        times.append((time.perf_counter() - start) * 1000)
    return sum(times) / len(times)


def measure(count):
    with contextlib.redirect_stdout(io.StringIO()):  # 측정 중 화면 출력 숨기기
        game = main.QuizGame()
        game.quizzes = make_quizzes(count)
        game.best_score = 80
        game.history = []

        save_ms = average_ms(game.save_data)
        load_ms = average_ms(game.load_data)
        list_ms = average_ms(game.show_quiz_list)
        search_ms = average_ms(lambda: [q for q in game.quizzes if "9999" in q.question])

    file_kb = os.path.getsize(main.STATE_FILE) / 1024

    tracemalloc.start()
    with contextlib.redirect_stdout(io.StringIO()):
        loaded = main.QuizGame()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert len(loaded.quizzes) == count  # 저장한 개수만큼 정확히 불러왔는지 확인

    return {
        "count": count, "save": save_ms, "load": load_ms, "list": list_ms,
        "search": search_ms, "file_kb": file_kb, "peak_mb": peak / 1024 / 1024,
    }


def main_benchmark():
    temp_dir = tempfile.mkdtemp()
    main.STATE_FILE = os.path.join(temp_dir, "state.json")

    results = []
    for size in SIZES:
        result = measure(size)
        results.append(result)
        print(f"  {size:>6,}개: 저장 {result['save']:.1f}ms, 불러오기 {result['load']:.1f}ms, "
              f"메모리 {result['peak_mb']:.2f}MB")

    k = next(r for r in results if r["count"] == 1_000)

    lines = [
        "# 성능 측정 (PERFORMANCE)",
        "",
        "`python tools/benchmark.py`로 퀴즈 개수를 늘려 가며 실제로 측정한 결과입니다.",
        "",
        f"- 측정 일시: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- 환경: Python {platform.python_version()} / {platform.system()} {platform.release()}",
        f"- 각 시간은 {REPEAT}회 반복 평균, 메모리는 `tracemalloc`으로 잰 불러오기 시 최대 사용량",
        "- 실제 state.json이 아닌 임시 폴더에서 측정",
        "",
        "## 측정 결과",
        "",
        "| 퀴즈 수 | 저장 (ms) | 불러오기 (ms) | 목록 출력 (ms) | 키워드 검색 (ms) | 파일 크기 (KB) | 메모리 최대 (MB) |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in results:
        lines.append(
            f"| {r['count']:,} | {r['save']:.1f} | {r['load']:.1f} | {r['list']:.1f} | "
            f"{r['search']:.2f} | {r['file_kb']:.0f} | {r['peak_mb']:.2f} |"
        )
    lines += [
        "",
        "## 분석",
        "",
        f"- **1,000개 기준**: 저장 약 {k['save']:.0f}ms, 불러오기 약 {k['load']:.0f}ms, 메모리 약 {k['peak_mb']:.1f}MB로 "
        "사용자가 기다림을 느끼지 않는 수준입니다.",
        "- 저장·불러오기·목록·검색은 모두 퀴즈를 처음부터 끝까지 한 번씩 확인하는 방식(O(n))이라, "
        "퀴즈 수가 10배 늘면 시간도 약 10배 늘어납니다.",
        "- 검색은 리스트를 처음부터 훑는 선형 검색입니다. 수만 개 이상으로 커지면 "
        "딕셔너리 색인이나 SQLite 같은 데이터베이스를 고려할 수 있습니다.",
        "- `save_data()`는 매번 파일 전체를 다시 씁니다. 퀴즈가 매우 많아지면 "
        "변경된 부분만 저장하는 방식이 필요하지만, 이 프로그램의 일반적인 사용량(수십~수백 개)에서는 충분합니다.",
        "",
        "## 같이 확인한 것",
        "",
        "- 각 크기마다 저장한 개수와 다시 불러온 개수가 같은지 `assert`로 확인했습니다.",
        "- 자동 테스트(`python -m unittest discover -s tests -v`)에도 1,000개 저장·불러오기 테스트가 들어 있습니다.",
        "",
    ]

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))
    print(f"✅ 성능 측정 결과를 저장했습니다: {os.path.relpath(OUTPUT, ROOT)}")


if __name__ == "__main__":
    main_benchmark()
