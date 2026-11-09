# 나만의 퀴즈 게임 - 프로그램 시작 파일

import json    # JSON 파일을 읽고 쓰는 표준 라이브러리
import os      # 파일 경로를 다루는 표준 라이브러리
import random  # [보너스 1] 문제 순서를 섞는 표준 라이브러리
import shutil  # [백업] 파일을 복사하는 표준 라이브러리
from datetime import datetime  # [보너스 5] 현재 날짜·시간을 구하는 표준 라이브러리

# 데이터 파일 위치: main.py와 같은 폴더(프로젝트 루트)의 state.json
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")


def get_backup_file():
    """[백업] 백업 파일 경로 (state.json → state.json.bak)"""
    return STATE_FILE + ".bak"


class Quiz:
    """퀴즈 한 문제를 표현하는 클래스"""

    def __init__(self, question, choices, answer, hint=""):
        # __init__ : 퀴즈를 새로 만들 때 자동으로 실행되는 함수
        # self : "지금 만들어지는 이 퀴즈 자신"을 가리킴
        self.question = question  # 문제 (글자)
        self.choices = choices    # 선택지 4개 (리스트)
        self.answer = answer      # 정답 번호 1~4 (숫자)
        self.hint = hint          # [보너스 3] 힌트 (없으면 빈 글자 "")

    def display(self, number):
        """문제와 선택지를 화면에 보여준다"""
        print(f"\n[문제 {number}]")
        print(self.question)
        print()
        # enumerate : 리스트를 돌면서 번호(1부터)와 값을 함께 꺼냄
        for i, choice in enumerate(self.choices, start=1):
            print(f"  {i}. {choice}")

    def is_correct(self, user_answer):
        """사용자가 입력한 번호가 정답이면 True, 아니면 False"""
        return user_answer == self.answer

    def to_dict(self):
        """퀴즈를 JSON으로 저장할 수 있는 딕셔너리로 바꾼다"""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,  # [보너스 3] 힌트도 함께 저장
        }


def create_default_quizzes():
    """처음 실행할 때 사용할 기본 퀴즈 5개를 만들어 리스트로 돌려준다"""
    return [
        Quiz(
            "Python에서 화면에 글자를 출력하는 함수는?",
            ["input()", "print()", "len()", "str()"],
            2,
            "화면에 '출력'한다는 영어 단어를 떠올려 보세요.",
        ),
        Quiz(
            "Python에서 리스트(list)를 만드는 올바른 방법은?",
            ["(1, 2, 3)", "[1, 2, 3]", "{1, 2, 3}", "<1, 2, 3>"],
            2,
            "대괄호를 사용합니다.",
        ),
        Quiz(
            "클래스로 객체를 만들 때 자동으로 실행되는 메서드는?",
            ["__start__", "__main__", "__init__", "__run__"],
            3,
            "'초기화(initialize)'의 줄임말입니다.",
        ),
        Quiz(
            "Git에서 변경 내용을 기록(저장)하는 명령어는?",
            ["git add", "git commit", "git push", "git clone"],
            2,
            "-m 옵션으로 메시지를 함께 남깁니다.",
        ),
        Quiz(
            "GitHub(원격 저장소)의 변경사항을 내 컴퓨터로 가져오는 명령어는?",
            ["git push", "git init", "git pull", "git checkout"],
            3,
            "'당기다'라는 뜻의 영어 단어입니다.",
        ),
    ]


class QuizGame:
    """퀴즈 게임 전체(퀴즈 목록, 최고 점수, 기록, 메뉴)를 관리하는 클래스"""

    def __init__(self):
        self.quizzes = []       # 퀴즈 목록 (리스트)
        self.best_score = None  # 최고 점수 (아직 안 풀었으면 None)
        self.history = []       # [보너스 5] 게임 기록 목록 (딕셔너리들의 리스트)
        self.load_data()        # 시작할 때 파일에서 불러오기

    # ---------- 파일 저장 / 불러오기 ----------

    def read_state_file(self, path):
        """[백업] JSON 파일 하나를 읽어서 퀴즈·최고 점수·기록을 적용한다 (실패하면 예외 발생)"""
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)  # JSON 글자 → 파이썬 딕셔너리

        quizzes = []
        for item in data["quizzes"]:
            # [보너스 3] 예전 파일에는 hint가 없으므로 get()으로 없으면 "" 사용
            quizzes.append(Quiz(item["question"], item["choices"], item["answer"], item.get("hint", "")))

        # 모든 값을 문제없이 읽은 뒤에 한꺼번에 적용 (중간에 실패하면 기존 값 유지)
        self.quizzes = quizzes
        self.best_score = data["best_score"]
        self.history = data.get("history", [])  # [보너스 5] 예전 파일에는 history가 없음

    def reset_to_default(self):
        """기본 퀴즈로 초기화한다"""
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.history = []

    def load_data(self):
        """state.json에서 데이터를 불러온다. 손상되었으면 백업 → 기본 퀴즈 순서로 복구한다."""
        # 1) 파일이 없으면 (처음 실행) → 기본 퀴즈 사용
        if not os.path.exists(STATE_FILE):
            print("📂 저장된 파일이 없어 기본 퀴즈로 시작합니다.")
            self.reset_to_default()
            return

        # 2) state.json 읽기
        try:
            self.read_state_file(STATE_FILE)
            best_text = "없음" if self.best_score is None else f"{self.best_score}점"
            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {best_text}, 기록 {len(self.history)}회)")
            return
        except (json.JSONDecodeError, KeyError, TypeError, OSError):
            print("⚠️ state.json이 손상되었거나 읽을 수 없습니다.")

        # 3) [백업] state.json이 손상되었으면 백업 파일(state.json.bak)로 복구 시도
        backup_file = get_backup_file()
        if os.path.exists(backup_file):
            try:
                self.read_state_file(backup_file)
                print(f"♻️ 백업 파일에서 복구했습니다. (퀴즈 {len(self.quizzes)}개)")
                self.save_data()  # 복구한 내용으로 state.json을 다시 만든다
                return
            except (json.JSONDecodeError, KeyError, TypeError, OSError):
                print("⚠️ 백업 파일도 손상되었습니다.")

        # 4) 백업도 없거나 손상되었으면 → 기본 퀴즈로 초기화
        print("⚠️ 기본 퀴즈로 복구합니다.")
        self.reset_to_default()

    def save_data(self):
        """퀴즈 목록, 최고 점수, 게임 기록을 state.json에 저장한다 (저장 전에 백업)"""
        quiz_list = []
        for quiz in self.quizzes:
            quiz_list.append(quiz.to_dict())  # Quiz 객체 → 딕셔너리

        data = {
            "quizzes": quiz_list,
            "best_score": self.best_score,
            "history": self.history,  # [보너스 5] 게임 기록도 저장
        }

        try:
            # [백업] 덮어쓰기 전에 지금 state.json을 state.json.bak으로 복사
            if os.path.exists(STATE_FILE):
                shutil.copyfile(STATE_FILE, get_backup_file())

            with open(STATE_FILE, "w", encoding="utf-8") as file:
                # ensure_ascii=False : 한글을 그대로 저장
                # indent=4 : 사람이 읽기 좋게 줄 바꿈과 들여쓰기
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError as error:
            print(f"⚠️ 파일 저장 중 오류가 발생했습니다: {error}")
            print("   → state.json이 다른 프로그램에서 열려 있거나 읽기 전용인지 확인한 뒤 다시 시도하세요.")
            print("   → 이전 데이터는 state.json.bak에 남아 있습니다.")

    # ---------- 입력 도우미 ----------

    def get_number(self, prompt, min_num, max_num):
        """숫자를 입력받는다. 올바른 숫자가 들어올 때까지 다시 물어본다."""
        while True:
            text = input(prompt).strip()  # strip() : 앞뒤 공백 제거

            # 1) 빈 입력 (그냥 Enter)
            if text == "":
                print("⚠️ 입력이 비어 있습니다. 숫자를 입력하세요.")
                continue

            # 2) 숫자가 아닌 입력 (예: abc)
            try:
                number = int(text)
            except ValueError:
                print(f"⚠️ 잘못된 입력입니다. {min_num}-{max_num} 사이의 숫자를 입력하세요.")
                continue

            # 3) 범위를 벗어난 숫자 (예: 9)
            if number < min_num or number > max_num:
                print(f"⚠️ 잘못된 입력입니다. {min_num}-{max_num} 사이의 숫자를 입력하세요.")
                continue

            return number  # 올바른 숫자면 돌려주고 반복 종료

    def get_text(self, prompt):
        """글자를 입력받는다. 비어 있으면 다시 물어본다."""
        while True:
            text = input(prompt).strip()
            if text == "":
                print("⚠️ 내용이 비어 있습니다. 다시 입력하세요.")
                continue
            return text

    # ---------- 메뉴 기능 ----------

    def show_menu(self):
        """메인 메뉴를 출력한다"""
        print()
        print("=" * 40)
        print("       🎯 나만의 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 퀴즈 삭제")
        print("6. 종료")
        print("=" * 40)

    def play_quiz(self):
        """저장된 퀴즈를 출제하고 결과를 보여준다"""
        # 퀴즈가 하나도 없는 경우
        if len(self.quizzes) == 0:
            print("📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        # [보너스 2] 몇 문제를 풀지 선택 (1 ~ 전체 퀴즈 수)
        max_count = len(self.quizzes)
        total = self.get_number(f"\n몇 문제를 풀까요? (1-{max_count}): ", 1, max_count)
        correct = 0       # 맞힌 문제 수
        points = 0        # [보너스 3] 점수 계산용 (그냥 맞히면 1점, 힌트 보고 맞히면 0.5점)
        hint_count = 0    # [보너스 3] 힌트를 본 횟수

        # [보너스 1] 원래 목록은 그대로 두고 복사본을 섞어서 출제
        quiz_order = self.quizzes[:]
        random.shuffle(quiz_order)
        quiz_order = quiz_order[:total]  # 섞은 목록에서 앞에서부터 total개만 사용

        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")
        print("💡 정답 입력에서 0을 누르면 힌트를 볼 수 있어요. (힌트를 보고 맞히면 0.5점)")

        for number, quiz in enumerate(quiz_order, start=1):
            print("-" * 40)
            quiz.display(number)
            used_hint = False  # [보너스 3] 이 문제에서 힌트를 봤는지

            user_answer = self.get_number("\n정답 입력 (힌트: 0): ", 0, 4)

            # [보너스 3] 0을 입력하면 힌트 보여주기
            if user_answer == 0:
                if quiz.hint == "":
                    print("💡 이 문제는 힌트가 없습니다.")
                else:
                    print(f"💡 힌트: {quiz.hint}")
                    used_hint = True
                    hint_count += 1
                user_answer = self.get_number("정답 입력: ", 1, 4)

            if quiz.is_correct(user_answer):
                correct += 1  # 맞힌 개수 1 증가
                if used_hint:
                    points += 0.5
                    print("✅ 정답입니다! (힌트 사용: 0.5점)")
                else:
                    points += 1
                    print("✅ 정답입니다!")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        # 결과 계산: 얻은 점수를 100점 만점으로 바꾸기
        score = int(points / total * 100)
        print("=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if hint_count > 0:
            print(f"💡 힌트 사용: {hint_count}회 (힌트를 본 문제는 0.5점)")

        # [보너스 5] 이번 게임 기록을 history에 추가
        record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),  # 예: 2026-11-09 15:30
            "total": total,         # 푼 문제 수
            "correct": correct,     # 맞힌 문제 수
            "score": score,         # 점수
            "hints": hint_count,    # 힌트 사용 횟수
        }
        self.history.append(record)

        # 최고 점수와 비교해서 더 높으면 갱신
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")
        print("=" * 40)

        self.save_data()  # [보너스 5] 게임이 끝날 때마다 기록과 점수를 저장

    def show_quiz_list(self):
        """저장된 퀴즈 목록을 번호와 함께 보여준다"""
        # 퀴즈가 하나도 없는 경우
        if len(self.quizzes) == 0:
            print("📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("-" * 40)

    def add_quiz(self):
        """새 퀴즈를 입력받아 목록에 추가한다"""
        print("\n📌 새로운 퀴즈를 추가합니다.")

        question = self.get_text("문제를 입력하세요: ")

        # 선택지 4개를 하나씩 입력받아 리스트에 담기
        choices = []
        for i in range(1, 5):
            choice = self.get_text(f"선택지 {i}: ")
            choices.append(choice)

        answer = self.get_number("정답 번호 (1-4): ", 1, 4)

        # [보너스 3] 힌트는 선택 사항이라 빈 입력도 허용 (그냥 Enter면 힌트 없음)
        hint = input("힌트 (없으면 Enter): ").strip()

        # 입력받은 내용으로 Quiz 객체를 만들어 목록에 추가
        new_quiz = Quiz(question, choices, answer, hint)
        self.quizzes.append(new_quiz)
        self.save_data()  # 추가한 퀴즈를 바로 파일에 저장
        print("✅ 퀴즈가 추가되었습니다!")

    def show_score(self):
        """최고 점수와 게임 기록을 보여준다"""
        # 아직 퀴즈를 한 번도 안 푼 경우
        if self.best_score is None:
            print("📭 아직 퀴즈를 풀지 않았습니다. 먼저 퀴즈를 풀어 보세요!")
            return

        print(f"\n🏆 최고 점수: {self.best_score}점")

        # [보너스 5] 게임 기록 히스토리 (최근 10회, 최신 기록부터)
        print(f"\n📜 게임 기록 (총 {len(self.history)}회, 최근 10회까지 표시)")
        print("-" * 40)
        if len(self.history) == 0:
            print("아직 저장된 게임 기록이 없습니다.")
        else:
            recent = self.history[-10:]      # [-10:] : 리스트 뒤에서 10개
            for record in reversed(recent):  # reversed : 순서를 거꾸로 (최신 기록부터)
                print(
                    f"{record['date']} | {record['correct']}/{record['total']}문제 정답 | "
                    f"{record['score']}점 | 힌트 {record['hints']}회"
                )
        print("-" * 40)

    def delete_quiz(self):
        """[보너스 4] 번호를 입력받아 퀴즈를 삭제한다"""
        if len(self.quizzes) == 0:
            print("📭 삭제할 퀴즈가 없습니다.")
            return

        self.show_quiz_list()  # 먼저 목록을 보여준다
        count = len(self.quizzes)
        number = self.get_number(f"삭제할 퀴즈 번호 (1-{count}): ", 1, count)

        # 리스트 번호는 0부터 시작하므로 1을 뺀다
        target = self.quizzes[number - 1]

        # 실수로 지우지 않도록 한 번 더 확인
        confirm = self.get_text(f"'{target.question}' 퀴즈를 삭제할까요? (y/n): ").lower()
        if confirm != "y":
            print("↩️ 삭제를 취소했습니다.")
            return

        self.quizzes.pop(number - 1)  # pop : 해당 위치의 항목을 리스트에서 꺼내 삭제
        self.save_data()              # 삭제 결과를 파일에 반영
        print("🗑️ 퀴즈가 삭제되었습니다.")

    def run(self):
        """프로그램의 중심: 메뉴를 보여주고 선택한 기능을 실행한다"""
        while True:
            self.show_menu()
            choice = self.get_number("선택: ", 1, 6)

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quiz_list()
            elif choice == 4:
                self.show_score()
            elif choice == 5:
                self.delete_quiz()
            elif choice == 6:
                self.save_data()  # 종료 전에 저장
                print("💾 데이터를 저장했습니다.")
                print("👋 프로그램을 종료합니다. 다음에 또 만나요!")
                break  # while 반복을 끝내서 프로그램 종료


def main():
    game = QuizGame()  # 게임 객체 만들기 (이때 파일에서 데이터를 불러옴)
    try:
        game.run()     # 게임 시작
    except (KeyboardInterrupt, EOFError):
        # KeyboardInterrupt : Ctrl+C를 눌렀을 때
        # EOFError : 입력이 갑자기 끊겼을 때 (Windows에서는 Ctrl+Z 후 Enter)
        print("\n\n⚠️ 입력이 중단되었습니다. 데이터를 저장하고 안전하게 종료합니다.")
        game.save_data()
        print("👋 프로그램을 종료합니다.")


if __name__ == "__main__":
    main()
