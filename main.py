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


# ----- 테스트용 코드 (Quiz 클래스가 잘 동작하는지 확인) -----
if __name__ == "__main__":
    sample = Quiz(
        "Python의 창시자는?",
        ["Guido", "Linus", "Bjarne", "James"],
        1,
    )
    sample.display(1)
    print("\n1번을 고르면 정답?", sample.is_correct(1))
    print("2번을 고르면 정답?", sample.is_correct(2))