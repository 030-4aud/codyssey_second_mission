"""주술회전 설정 모티브 탐구 퀴즈 실행 파일."""

from quiz_game import QuizGame


def main():
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️ 입력이 중단되어 프로그램을 안전하게 종료합니다.")
        game.save_data()
        print("💾 저장 가능한 데이터 저장을 마쳤습니다. 다음에 다시 만나요!")


if __name__ == "__main__":
    main()
