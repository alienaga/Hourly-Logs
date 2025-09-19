import time
import os
import datetime
import subprocess

# Configuration
LOOP_INTERVAL_MINUTES = 60  # Adjust as needed
REPO_URL = os.getenv("GIT_REPO_URL", "https://github.com/alienaga/Auto-Commit-Github.git")  # Read from environment variable or use default
LOGS_DIR = "logs"

# Ensure logs directory exists
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

def generate_status_data():
    """Generate status data with timestamp."""
    return f"Status update at {datetime.datetime.now()}"

def log_status_data(status_data):
    """Log status data to a file with today's date."""
    today = datetime.datetime.now().strftime("%Y%m%d")
    log_file = os.path.join(LOGS_DIR, f"Log_{today}.txt")
    with open(log_file, "a") as f:
        f.write(f"{status_data}\n")

def git_operations():
    """Perform Git operations: add, commit, and push."""
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Auto-commit: status update"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e}")

if __name__ == "__main__":
    while True:
        status_data = generate_status_data()
        log_status_data(status_data)
        git_operations()
        time.sleep(LOOP_INTERVAL_MINUTES * 60)