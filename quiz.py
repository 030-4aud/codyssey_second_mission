"""개별 퀴즈의 데이터와 동작을 정의하는 모듈."""


class Quiz:
    """문제, 선택지, 정답, 해설을 보관하는 퀴즈 객체."""

    def __init__(self, question, choices, answer, explanation=""):
        question = str(question).strip()
        choices = [str(choice).strip() for choice in choices]

        if not question:
            raise ValueError("문제 내용은 비워 둘 수 없습니다.")
        if len(choices) != 4:
            raise ValueError("선택지는 반드시 4개여야 합니다.")
        if any(not choice for choice in choices):
            raise ValueError("선택지 내용은 비워 둘 수 없습니다.")
        if not isinstance(answer, int) or isinstance(answer, bool) or not 1 <= answer <= 4:
            raise ValueError("정답 번호는 1부터 4까지의 정수여야 합니다.")

        self.question = question
        self.choices = choices
        self.answer = answer
        self.explanation = str(explanation).strip()

    def display(self, number=None):
        """문제와 네 개의 선택지를 화면에 출력한다."""
        print("\n" + "-" * 56)
        if number is not None:
            print(f"[문제 {number}]")
        print(self.question)
        for index, choice in enumerate(self.choices, start=1):
            print(f"  {index}. {choice}")

    def check_answer(self, user_answer):
        """입력한 번호가 정답인지 반환한다."""
        return user_answer == self.answer

    def show_explanation(self):
        """등록된 해설이 있으면 출력한다."""
        if self.explanation:
            print(f"해설: {self.explanation}")

    def to_dict(self):
        """JSON 저장에 사용할 딕셔너리로 변환한다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "explanation": self.explanation,
        }

    @classmethod
    def from_dict(cls, data):
        """JSON에서 읽은 딕셔너리로 Quiz 객체를 생성한다."""
        if not isinstance(data, dict):
            raise ValueError("퀴즈 데이터는 객체 형태여야 합니다.")
        return cls(
            question=data.get("question", ""),
            choices=data.get("choices", []),
            answer=data.get("answer"),
            explanation=data.get("explanation", ""),
        )
