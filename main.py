"""주술회전 설정 모티브 탐구 퀴즈 실행 파일."""

from quiz_game import QuizGame


def main():
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError) as error:
        print("\n\n⚠️ 입력이 중단되어 프로그램을 안전하게 종료합니다.")
        game.log_event("WARNING", "INPUT_INTERRUPTED", "Ctrl+C 또는 입력 스트림 종료로 프로그램 중단", error)
        if game.save_data():
            print("💾 저장 성공: 데이터가 안전하게 저장되었습니다. 다음에 다시 만나요!")
        else:
            print("⚠️ 저장 실패: logs/quiz_game.log에서 원인을 확인하세요.")
    except Exception as error:
        game.log_event("ERROR", "UNHANDLED_EXCEPTION", "처리하지 못한 오류로 프로그램 종료", error)
        print(f"❌ 예기치 않은 오류가 발생했습니다: {error}")
        print("상세 원인은 logs/quiz_game.log에서 확인할 수 있습니다.")
        raise


if __name__ == "__main__":
    main()
