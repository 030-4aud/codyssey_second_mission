# 퀴즈 설계서

## 목적
《주술회전》의 설정과 연결해 볼 수 있는 일본 역사·민속·종교 소재를 퀴즈로 탐구한다. 작품의 허구적 설정과 실제 기록·지역 전승·작가 발언을 동일시하지 않고 근거의 종류를 구분한다.

## 기본 퀴즈 수
기본 퀴즈는 **12개**이며 `QuizGame.default_quizzes()`에서 생성한다. `tests/test_quiz_game.py`의 `test_default_quiz_count_is_at_least_five_and_is_twelve`와 `docs/verification.md`의 별도 명령으로 실제 개수를 확인한다.

## 한 문제의 데이터 구조
- `question`: 문제 문장(str)
- `choices`: 네 개의 선택지(list[str])
- `answer`: 정답 번호(1~4, int)
- `explanation`: 해설(str)

## 주제 묶음
1. 양면숙나와 히다 지역 전승
2. 음양도와 음양료
3. 식신의 역사적 의미
4. 작가 인터뷰 보도 및 불교·일본 신격
5. 자료의 종류를 구분하는 비판적 읽기

개별 문제의 구체적인 출처 서지정보는 `docs/sources.md`에서 원문 확인 후 보완한다.
