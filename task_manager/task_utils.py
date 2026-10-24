from task_manager.validation import (
    validate_due_date,
    validate_task_description,
    validate_task_title,
)

tasks = []

def add_task(title, description, due_date):
    if not validate_task_title(title):
        return None
    if not validate_task_description(description):
        return None
    if not validate_due_date(due_date):
        return None

    task = {
        "title": title.strip(),
        "description": description.strip(),
        "due_date": due_date,
        "completed": False,
    }
    tasks.append(task)
    print("Task added successfully!")
    return task

def mark_task_as_complete(index, tasks=tasks):
    if not isinstance(index, int) or index < 0 or index >= len(tasks):
        print("Invalid task number.")
        return False
    if tasks[index]["completed"]:
        print("Task is already complete.")
        return False

    tasks[index]["completed"] = True
    print("Task marked as complete!")
    return True

def view_pending_tasks(tasks=tasks):
    pending = [(index, task) for index, task in enumerate(tasks, start=1) if not task["completed"]]
    if not pending:
        print("No pending tasks.")
        return []

    for index, task in pending:
        print(f"{index}. {task['title']} - {task['description']} (Due: {task['due_date']})")
    return [task for _, task in pending]

def calculate_progress(tasks=tasks):
    if len(tasks) == 0:
        print("No tasks currently.")
        return 0

    completed = sum(task["completed"] for task in tasks)
    progress = completed / len(tasks) * 100
    return progress
