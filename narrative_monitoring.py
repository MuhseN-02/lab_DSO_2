import logging
import uuid
from datetime import datetime, timezone
import time
import random
from prometheus_client import start_http_server, Summary, Counter

# ----------------------
# Logging Setup
# ----------------------
logger = logging.getLogger("narrative_logger")
handler = logging.FileHandler("narrative_app.json")
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def log_event(actor, chapter, status, details=None):
    """Log structured narrative event"""
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_id": str(uuid.uuid4()),
        "actor": actor,
        "chapter": chapter,
        "status": status,
        "details": details or {}
    }
    logger.info(event)

# ----------------------
# Prometheus Metrics
# ----------------------
CHAPTER_TIME = Summary('chapter_processing_seconds', 'Time spent per chapter', ['chapter'])
FAILURE_COUNT = Counter('chapter_failures_total', 'Number of failures per chapter', ['chapter'])

# ----------------------
# Example Application Workflows
# ----------------------
def user_login(user):
    chapter = "UserLogin"
    actor = "AuthModule"

    with CHAPTER_TIME.labels(chapter=chapter).time():
        log_event(actor, chapter, "start", {"user": user})
        time.sleep(random.uniform(0.2, 0.6))  # Simulate processing
        if user != "admin":
            log_event(actor, chapter, "fail", {"user": user, "reason": "invalid_user"})
            FAILURE_COUNT.labels(chapter=chapter).inc()
        else:
            log_event(actor, chapter, "success", {"user": user})

def fetch_profile(user):
    chapter = "FetchProfile"
    actor = "ProfileModule"

    with CHAPTER_TIME.labels(chapter=chapter).time():
        log_event(actor, chapter, "start", {"user": user})
        time.sleep(random.uniform(0.1, 0.4))
        if random.random() < 0.1:  # Simulate occasional failure
            log_event(actor, chapter, "fail", {"user": user, "reason": "db_timeout"})
            FAILURE_COUNT.labels(chapter=chapter).inc()
        else:
            log_event(actor, chapter, "success", {"user": user})

def log_action(user, action):
    chapter = "LogAction"
    actor = "LoggingModule"

    with CHAPTER_TIME.labels(chapter=chapter).time():
        log_event(actor, chapter, "start", {"user": user, "action": action})
        time.sleep(random.uniform(0.05, 0.2))
        log_event(actor, chapter, "success", {"user": user, "action": action})

# ----------------------
# Simulate Multiple Workflows
# ----------------------
def simulate_workflows():
    users = ["admin", "guest", "mouhcine", "testuser"]
    actions = ["login", "update_profile", "view_report", "logout"]

    for _ in range(20):  # Simulate 20 workflow runs
        user = random.choice(users)
        user_login(user)
        fetch_profile(user)
        action = random.choice(actions)
        log_action(user, action)

# ----------------------
# Main
# ----------------------
if __name__ == "__main__":
    start_http_server(8000)  # Start Prometheus metrics server
    print("Prometheus metrics server running on http://localhost:8000/")

    try:
        while True:
            simulate_workflows()
            time.sleep(5)  # Wait 5 seconds before next batch
    except KeyboardInterrupt:
        print("Exiting...")
