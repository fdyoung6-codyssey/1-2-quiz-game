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


# ----- 테스트용 코드 (기본 퀴즈가 잘 만들어졌는지 확인) -----
if __name__ == "__main__":
    quizzes = create_default_quizzes()
    print(f"기본 퀴즈 개수: {len(quizzes)}개")
    for number, quiz in enumerate(quizzes, start=1):
        quiz.display(number)