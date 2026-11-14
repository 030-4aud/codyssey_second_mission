# 🌀 주술회전 설정 모티브 탐구 퀴즈

## 1. 프로젝트 개요

일본 애니메이션·만화 **《주술회전》**의 세계관에 활용되거나 연상되는 문화적 소재를 실제 역사·종교·민속 자료와 연결해 알아보는 Python 콘솔 퀴즈 게임입니다.

애니메이션의 줄거리나 캐릭터 이름을 맞히는 데서 그치지 않고, 양면숙나 전승, 음양도와 식신, 불교 및 일본 신앙의 상징, 작가 인터뷰에 언급된 신화적 영향 등을 살펴보도록 구성했습니다.

> 참고: 작품 속 설정은 실제 종교·역사와 동일하지 않습니다. 문제와 해설에서는 역사 기록, 지역 전승, 작가 발언을 구분하고, 보도나 연구를 통해 확인되는 범위에서 설명합니다.

## 2. 퀴즈 주제와 선정 이유

**선정 주제:** 《주술회전》 설정의 문화적 모티브 — 일본 신화·민속·불교·음양도

**선정 이유:** 작품에는 양면숙나, 식신, 주술, 영역의 종교적 이미지 등 현실의 역사·민속·종교 개념을 떠올리게 하는 요소가 등장합니다. 이러한 소재의 배경을 조사하면 애니메이션을 더 깊게 감상할 수 있고, 프로그래밍으로 학습 내용을 퀴즈 형태로 정리할 수 있다고 생각했습니다.

## 3. 실행 방법

### 실행 환경

- Python 3.10 이상
- 외부 라이브러리 설치 불필요 (Python 표준 라이브러리만 사용)
- Windows PowerShell, 명령 프롬프트, macOS/Linux 터미널에서 실행 가능

### 실행 명령

프로젝트 폴더로 이동한 뒤 다음 명령을 실행합니다.

```bash
python main.py
```

Windows 환경에서 `python` 명령이 연결되어 있지 않다면 다음 명령을 사용할 수 있습니다.

```powershell
py main.py
```

## 4. 기능 목록

| 메뉴 | 기능 |
|---|---|
| 1. 퀴즈 풀기 | 등록된 문제를 무작위 순서로 출제하고 정답·오답 및 해설 표시 |
| 2. 퀴즈 추가 | 문제, 선택지 4개, 정답 번호를 입력해 새 퀴즈 등록 |
| 3. 퀴즈 목록 | 등록된 모든 문제 확인 |
| 4. 최고 점수 확인 | 지금까지의 최고 정답 수와 당시 전체 문제 수 확인 |
| 5. 종료 | 데이터를 저장하고 프로그램 종료 |

### 입력 및 예외 처리

- 숫자 입력 앞뒤의 공백을 제거합니다.
- 빈 입력, 숫자가 아닌 입력, 허용 범위를 벗어난 숫자는 안내 후 재입력받습니다.
- `Ctrl+C` 또는 입력 스트림 종료(`EOFError`) 시 저장을 시도하고 안전하게 종료합니다.
- `state.json`이 없으면 기본 퀴즈 데이터로 시작합니다.
- JSON 파일이 손상되었거나 구조가 올바르지 않으면 기본 데이터로 복구합니다.
- 저장은 임시 파일 작성 후 교체하는 방식으로 진행합니다.

## 5. 파일 구조

```text
jujutsu_motifs_quiz/
├── main.py                  # 프로그램 실행 및 안전 종료 처리
├── quiz.py                  # Quiz 클래스: 문제·선택지·정답·해설
├── quiz_game.py              # QuizGame 클래스: 메뉴·게임 진행·저장/불러오기
├── state.json                # 퀴즈 데이터와 최고 점수
├── README.md                 # 프로젝트 설명 및 실행 방법
├── .gitignore                # Git 제외 파일 설정
├── docs/
│   ├── sources.md            # 퀴즈 내용 참고 자료
│   └── screenshots/
│       └── README.md         # 제출용 실행 화면 캡처 안내
└── tests/
    └── test_quiz_game.py     # 표준 unittest 테스트
```

## 6. 데이터 파일 설명: state.json

`state.json`은 프로젝트 루트에 위치하며, 프로그램이 등록된 퀴즈와 최고 점수를 저장합니다. UTF-8 인코딩과 JSON 형식을 사용하므로 한글이 깨지지 않도록 `ensure_ascii=False`로 기록합니다.

| 키 | 자료형 | 설명 |
|---|---|---|
| `quizzes` | list | 퀴즈 객체의 목록 |
| `question` | str | 문제 문장 |
| `choices` | list[str] | 네 개의 선택지 |
| `answer` | int | 정답 번호 (1~4) |
| `explanation` | str | 정답에 대한 간단한 해설 |
| `best_score` | int 또는 null | 최고 정답 수. 아직 기록이 없으면 `null` |
| `best_total` | int 또는 null | 최고 기록 당시 전체 문제 수 |

퀴즈를 추가하거나 새로운 최고 기록이 나오면 파일에 자동 저장됩니다. 프로그램을 다시 실행해도 데이터가 유지됩니다.

## 7. 클래스 구조

### Quiz

- 속성: `question`, `choices`, `answer`, `explanation`
- 메서드: `display()`, `check_answer()`, `show_explanation()`, `to_dict()`, `from_dict()`
- 역할: 개별 퀴즈 한 문제의 데이터와 동작 관리

### QuizGame

- 속성: `state_path`, `quizzes`, `best_score`, `best_total`
- 메서드: `load_data()`, `save_data()`, `show_menu()`, `play_quiz()`, `add_quiz()`, `show_quizzes()`, `show_score()`, `run()` 등
- 역할: 게임 전체 흐름, 입력 처리, 점수 및 파일 입출력 관리

## 8. 테스트 실행

Python 표준 라이브러리의 `unittest`로 테스트할 수 있습니다.

```bash
python -m unittest discover -s tests -v
```

## 9. Git 작업 기록 및 GitHub 제출

기능별 커밋으로 작업 이력을 관리하고, 별도 브랜치에서 퀴즈 플레이 기능을 구현한 뒤 `main`에 병합합니다. GitHub 저장소를 만든 후 원격 저장소 주소를 연결해 push해야 온라인 제출이 완료됩니다.

기본 로컬 Git 이력이 포함된 프로젝트라면 아래 명령으로 원격 저장소를 연결할 수 있습니다.

```bash
git remote set-url origin https://github.com/본인계정/저장소이름.git
git push -u origin main
```

이 프로젝트에는 `origin` 주소 자리표시자가 설정되어 있으므로 `git remote set-url`로 본인 저장소 주소를 입력합니다. GitHub 인증은 본인 계정으로 진행해야 합니다. `clone`과 `pull` 실습은 README 마지막의 GitHub 복제 실습 절차를 참고하세요.

### GitHub clone / pull 실습

1. GitHub에 push한 저장소 주소를 복사합니다.
2. 기존 프로젝트 폴더와 다른 위치에서 저장소를 복제합니다.

```bash
git clone https://github.com/본인계정/저장소이름.git quiz-clone-practice
```

3. 복제한 폴더의 README에 실습 문장 한 줄을 추가하고 커밋 및 push합니다.

```bash
cd quiz-clone-practice
git add README.md
git commit -m "Docs: clone 실습 내용 추가"
git push
```

4. 원래 작업하던 프로젝트 폴더로 돌아가 pull 합니다.

```bash
cd ../jujutsu_motifs_quiz
git pull origin main
```

5. 원래 폴더의 README에도 실습 문장이 반영되었는지 확인합니다.

## 10. 제출 스크린샷 체크리스트

실제 실행 화면을 본인 컴퓨터에서 캡처해 `docs/screenshots/`에 저장합니다.

- `menu.png`: 실행 및 메뉴 화면
- `play.png`: 퀴즈 출제와 정답·결과 화면
- `add_quiz.png`: 퀴즈 추가 완료 화면
- `score.png`: 최고 점수 확인 화면
- `git-log.png`: `git log --oneline --graph --all` 결과
- 개발 환경: Python 버전, 터미널 또는 VS Code, Git 설정 화면

## 11. 참고 자료

퀴즈를 구성할 때 확인한 자료와 각 자료의 사용 범위는 [`docs/sources.md`](docs/sources.md)에 정리했습니다.

### 주요 Git 명령어 참고

```bash
git init                         # 로컬 저장소 생성
git add .                        # 변경 파일 스테이징
git commit -m "Feat: ..."        # 변경 이력 저장
git branch feature-name          # 작업 브랜치 생성
git checkout feature-name        # 브랜치 이동
git checkout main               # main으로 복귀
git merge feature-name           # 작업 브랜치 병합
git push -u origin main          # GitHub에 업로드
git clone 저장소주소             # 원격 저장소 복제
git pull origin main             # 원격 변경사항 가져오기
```

브랜치 생성과 이동은 `git switch -c feature-name` 명령으로 한 번에 수행할 수도 있습니다.
