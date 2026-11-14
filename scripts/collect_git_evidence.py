"""현재 저장소의 Git 원격·브랜치·커밋 증빙을 파일로 수집한다."""

from datetime import datetime
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "evidence" / "git-evidence.txt"


def run_git(*args):
    try:
        result = subprocess.run(
            ["git", *args], cwd=ROOT, text=True, encoding="utf-8",
            errors="replace", capture_output=True, check=False
        )
    except FileNotFoundError:
        return "[실행 불가] Git 명령을 찾을 수 없습니다. Git 설치 후 다시 실행하세요."
    if result.returncode == 0:
        return result.stdout.strip() or "(출력 없음)"
    return (result.stderr or result.stdout).strip() or f"명령 종료 코드: {result.returncode}"


sections = [
    "Git 증빙 수집 시각: " + datetime.now().astimezone().isoformat(timespec="seconds"),
    "프로젝트 경로: " + str(ROOT),
    "\n[git remote -v]\n" + run_git("remote", "-v"),
    "\n[git status --short --branch]\n" + run_git("status", "--short", "--branch"),
    "\n[git branch -vv]\n" + run_git("branch", "-vv"),
    "\n[git log --oneline --graph --decorate --all -n 40]\n" + run_git("log", "--oneline", "--graph", "--decorate", "--all", "-n", "40"),
    "\n[git ls-remote --heads origin]\n" + run_git("ls-remote", "--heads", "origin"),
]
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(sections) + "\n", encoding="utf-8")
print(f"Git 증빙을 저장했습니다: {OUTPUT.relative_to(ROOT)}")
print("원격 주소와 ls-remote 출력이 비어 있거나 오류면 origin 설정 및 인증을 확인하세요.")
