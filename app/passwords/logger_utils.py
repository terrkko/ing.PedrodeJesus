import datetime

LOG_FILE = 'app/activity.log'

def log_action(user, action, service):
    timestamp = datetime.datetime.now().isoformat()
    line = f"[{timestamp}] User: {user}, Action: {action}, Service: {service}\n"
    with open(LOG_FILE, 'a') as f:
        f.write(line)
