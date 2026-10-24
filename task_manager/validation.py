from datetime import datetime

def validate_task_title(title):
    if not isinstance(title, str) or len(title.strip()) == 0:
        print("Task title cannot be empty.")
        return False
    return True
    
def validate_task_description(description):
    if not isinstance(description, str) or len(description.strip()) == 0:
        print("Task description cannot be empty.")
        return False
    return True
    
def validate_due_date(due_date):
    try:
        if datetime.strptime(due_date, "%Y-%m-%d").strftime("%Y-%m-%d") != due_date:
            raise ValueError
    except (TypeError, ValueError):
        print("Due date must be a valid date in YYYY-MM-DD format.")
        return False
    return True
