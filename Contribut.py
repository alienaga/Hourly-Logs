import os
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

# ─── CONFIG ────────────────────────────────────────────────────────────────────
REPO_DIR          = Path(os.getenv("GIT_REPO_DIRECTORY", str(Path.home() / "OneDrive" / "Documents" / "GitHub" / "Logs-Automation")))
FILENAME          = "contrib_log.txt"
REMOTE            = "origin"
BRANCH            = "main"
GITHUB_URL        = "https://github.com/alienaga/Logs-Automation.git"
COMMITS_PER_DAY   = 10    # ← how many commits you want on each date
MINUTE_INTERVAL   = 60   # ← minutes between each commit
# ───────────────────────────────────────────────────────────────────────────────

def run(cmd, cwd=None, env=None):
    print(f"> {cmd}")
    subprocess.check_call(cmd, shell=True, cwd=cwd, env=env)

def generate_date_list(start: str, end: str):
    d0 = datetime.strptime(start, "%Y-%m-%d")
    d1 = datetime.strptime(end,   "%Y-%m-%d")
    return [(d0 + timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range((d1 - d0).days + 1)]

# e.g. fill June 2025
DATES = generate_date_list("2024-06-30", "2025-06-30")

def ensure_repo():
    REPO_DIR.mkdir(parents=True, exist_ok=True)
    os.chdir(REPO_DIR)

    if not (REPO_DIR / ".git").exists():
        run("git init")
        run(f"git remote add {REMOTE} {GITHUB_URL}")

    # align local `main` with remote/main
    run(f"git fetch {REMOTE} {BRANCH}")
    run(f"git checkout -B {BRANCH} {REMOTE}/{BRANCH}")

def make_commits():
    filepath = REPO_DIR / FILENAME
    filepath.touch(exist_ok=True)

    for day in DATES:
        for idx in range(COMMITS_PER_DAY):
            # compute a timestamp at 12:00 + idx * interval
            base = datetime.strptime(day, "%Y-%m-%d")
            commit_time = base + timedelta(hours=12, minutes=idx * MINUTE_INTERVAL)
            iso = commit_time.strftime("%Y-%m-%dT%H:%M:%S")

            # append a line to ensure a diff
            with open(filepath, "a", encoding="utf-8") as f:
                f.write(f"[{iso}] Contribution #{idx+1} on {day}\n")

            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"]    = iso
            env["GIT_COMMITTER_DATE"] = iso

            run(f"git add {FILENAME}", cwd=REPO_DIR, env=env)
            run(f'git commit -m "Auto-contrib {idx+1} on {day}"', cwd=REPO_DIR, env=env)

def push_up():
    run(f"git pull --rebase {REMOTE} {BRANCH}", cwd=REPO_DIR)
    run(f"git push {REMOTE} {BRANCH}",       cwd=REPO_DIR)

if __name__ == "__main__":
    ensure_repo()
    make_commits()
    push_up()