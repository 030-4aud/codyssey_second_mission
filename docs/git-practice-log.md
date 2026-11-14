# Git 작업 기록 및 증빙 생성 절차

이 문서는 기존 저장소에서 브랜치·병합·원격 업로드 실습을 재현하고 실제 결과를 남기기 위한 절차입니다. 현재 ZIP에는 사용자의 실제 GitHub 계정과 원격 저장소를 알 수 없어 특정 URL이나 commit/push 결과를 기록하지 않았습니다.

## 기능 브랜치와 병합

```bash
git switch main
git pull origin main
git switch -c feature/quiz-game
# 기능을 수정한 뒤
git add .
git commit -m "Feat(quiz): 퀴즈 플레이 흐름 구현"
python -m unittest discover -s tests -v
git switch main
git merge --no-ff feature/quiz-game -m "Merge: 퀴즈 플레이 기능 병합"
```

팀 작업이면 병합 전에 리뷰를 받고, 개인 과제면 테스트와 diff를 직접 검토합니다. 제출에서 작업 브랜치의 커밋 이력 보존이 중요하면 일반 merge commit을 사용합니다.

## 원격 저장소 연결 및 확인

```bash
git remote -v
git remote add origin https://github.com/본인계정/저장소이름.git
# origin이 이미 있으면 add 대신 set-url
git remote set-url origin https://github.com/본인계정/저장소이름.git
git push -u origin main
git ls-remote --heads origin
```

## 증빙 파일 생성

```bash
python scripts/collect_git_evidence.py
```

이 명령은 실제 현재 저장소에서 원격 URL, 상태, 브랜치, 커밋 그래프, 원격 브랜치 조회 결과를 `docs/evidence/git-evidence.txt`에 기록합니다. 명령 실행 후 파일을 열어 실패 메시지나 잘못된 URL이 없는지 확인합니다. 필요하면 터미널 화면도 `docs/screenshots/git-log.png`, `git-remote.png`, `git-push.png`로 캡처합니다.
