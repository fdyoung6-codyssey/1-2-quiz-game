# 나만의 퀴즈 게임 - 프로그램 시작 파일


class Quiz:
    """퀴즈 한 문제를 표현하는 클래스"""

    def __init__(self, question, choices, answer):
        # __init__ : 퀴즈를 새로 만들 때 자동으로 실행되는 함수
        # self : "지금 만들어지는 이 퀴즈 자신"을 가리킴
        self.question = question  # 문제 (글자)
        self.choices = choices    # 선택지 4개 (리스트)
        self.answer = answer      # 정답 번호 1~4 (숫자)

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


def create_default_quizzes():
    """처음 실행할 때 사용할 기본 퀴즈 5개를 만들어 리스트로 돌려준다"""
    return [
        Quiz(
            "Python에서 화면에 글자를 출력하는 함수는?",
            ["input()", "print()", "len()", "str()"],
            2,
        ),
        Quiz(
            "Python에서 리스트(list)를 만드는 올바른 방법은?",
            ["(1, 2, 3)", "[1, 2, 3]", "{1, 2, 3}", "<1, 2, 3>"],
            2,
        ),
        Quiz(
            "클래스로 객체를 만들 때 자동으로 실행되는 메서드는?",
            ["__start__", "__main__", "__init__", "__run__"],
            3,
        ),
        Quiz(
            "Git에서 변경 내용을 기록(저장)하는 명령어는?",
            ["git add", "git commit", "git push", "git clone"],
            2,
        ),
        Quiz(
            "GitHub(원격 저장소)의 변경사항을 내 컴퓨터로 가져오는 명령어는?",
            ["git push", "git init", "git pull", "git checkout"],
            3,
        ),
    ]


class QuizGame:
    """퀴즈 게임 전체(퀴즈 목록, 최고 점수, 메뉴)를 관리하는 클래스"""

    def __init__(self):
        self.quizzes = create_default_quizzes()  # 퀴즈 목록 (리스트)
        self.best_score = None                   # 최고 점수 (아직 안 풀었으면 None)

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
        print("5. 종료")
        print("=" * 40)

    def play_quiz(self):
        """저장된 퀴즈를 순서대로 출제하고 결과를 보여준다"""
        # 퀴즈가 하나도 없는 경우
        if len(self.quizzes) == 0:
            print("📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        total = len(self.quizzes)  # 전체 문제 수
        correct = 0                # 맞힌 문제 수
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")

        for number, quiz in enumerate(self.quizzes, start=1):
            print("-" * 40)
            quiz.display(number)
            user_answer = self.get_number("\n정답 입력: ", 1, 4)

            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!")
                correct += 1  # 맞힌 개수 1 증가
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        # 결과 계산: 맞힌 비율을 100점 만점으로 바꾸기
        score = int(correct / total * 100)
        print("=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        print("=" * 40)

    def run(self):
        """프로그램의 중심: 메뉴를 보여주고 선택한 기능을 실행한다"""
        while True:
            self.show_menu()
            choice = self.get_number("선택: ", 1, 5)

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                print("🚧 퀴즈 추가 기능은 준비 중입니다.")
            elif choice == 3:
                print("🚧 퀴즈 목록 기능은 준비 중입니다.")
            elif choice == 4:
                print("🚧 점수 확인 기능은 준비 중입니다.")
            elif choice == 5:
                print("👋 프로그램을 종료합니다. 다음에 또 만나요!")
                break  # while 반복을 끝내서 프로그램 종료


def main():
    game = QuizGame()  # 게임 객체 만들기
    game.run()         # 게임 시작


if __name__ == "__main__":
    main()