# Git clone / pull 실습 기록

과제의 `clone`과 `pull` 명령을 확인하기 위해 별도의 로컬 bare remote를 이용해 동일한 흐름을 한 차례 실행했다. 이 연습은 Git 동작 검증용이며, **GitHub에 업로드한 기록을 의미하지는 않는다.** 실제 제출 전에는 GitHub 원격 저장소에 대해서도 아래 단계를 반복해야 한다.

실습에 사용한 명령 흐름:

```bash
git clone --bare /mnt/data/jujutsu_motifs_quiz /mnt/data/jujutsu_motifs_quiz_remote.git
git clone /mnt/data/jujutsu_motifs_quiz_remote.git /mnt/data/jujutsu_motifs_quiz_clone_practice
cd /mnt/data/jujutsu_motifs_quiz_clone_practice
git add docs/clone-pull-practice.txt
git commit -m "Docs: verify clone and pull workflow"
git push origin main
cd /mnt/data/jujutsu_motifs_quiz
git pull origin main
```

`pull` 이후 원본 작업 폴더에 `docs/clone-pull-practice.txt`가 들어온 것을 확인했다.
