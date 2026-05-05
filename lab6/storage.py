from datetime import datetime, timezone
from models import Task # Импорт модели Task из файла models.py

tasks = []
archived_tasks = []
current_id = 1

#Функция создаёт новую задачу.
def create_task(task: Task):
    global current_id

    for t in tasks:
        if t["title"] == task.title:
            raise ValueError("Task with this title already exists")

    new_task = task.model_dump() # Преобразуем Pydantic модель в словарь
    new_task["id"] = current_id # Устанавливаем уникальный ID для задачи
    new_task["created_at"] = datetime.now(timezone.utc) # Устанавливаем время создания задачи 
    new_task["completed_at"] = None # Изначально задача не выполнена, поэтому completed_at устанавливаем в None

    tasks.append(new_task)
    current_id += 1

    if len(tasks) > 20:
        archived_tasks.append(tasks.pop(0))
    return new_task

#Фильтрация и сортировка задач
def get_all_tasks(completed=None, priority=None, limit=None, sort_by=None):
    result = tasks.copy()

    if completed is not None:
        result = [t for t in result if t["completed"] == completed]

    if priority:
        result = [t for t in result if t["priority"] == priority]
# Сортировка по дате создания или приоритету
    if sort_by == "created_at":
        result.sort(key=lambda x: x["created_at"])
# Сортировка по приоритету: high > medium > low
    if sort_by == "priority":
        order = {"high": 1, "medium": 2, "low": 3}
        result.sort(key=lambda x: order[x["priority"]])

    if limit:
        result = result[:limit]

    return result

# Получение задачи по ID
def get_task(task_id: int):
    for t in tasks:
        if t["id"] == task_id:
            return t
    return None

# Удаление задачи по ID
def delete_task(task_id: int):
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            tasks.pop(i)
            return True
    return False

# Завершение задачи
def complete_task(task_id: int):
    task = get_task(task_id)

    if not task:
        return None

    if task["completed"]:
        raise ValueError("Task already completed")

    task["completed"] = True
    task["completed_at"] = datetime.now(timezone.utc)

    return task

# Обновление задачи
def update_task(task_id: int, new_task: Task):
    task = get_task(task_id)

    if not task:
        return None

    task["title"] = new_task.title
    task["description"] = new_task.description
    task["priority"] = new_task.priority
    task["deadline"] = new_task.deadline

    return task

# Частичное обновление задачи
def patch_task(task_id: int, data: dict):
    task = get_task(task_id)

    if not task:
        return None
# Обновляем только те поля, которые присутствуют в данных
    for key in ["title", "description", "priority", "deadline"]:
        if key in data:
            task[key] = data[key]

    return task

# Поиск задач по ключевому слову, приоритету и диапазону дат
def search_tasks(keyword=None, priority=None, date_from=None, date_to=None):
    result = tasks.copy()

    if keyword:
        result = [
            t for t in result
            if keyword.lower() in (t["title"] or "").lower()
            or keyword.lower() in (t["description"] or "").lower()
        ]

    if priority:
        result = [t for t in result if t["priority"] == priority]

    if date_from:
        result = [t for t in result if t["created_at"] >= date_from]

    if date_to:
        result = [t for t in result if t["created_at"] <= date_to]

    return result

# Получение статистики по задачам
def get_stats():
    now = datetime.now(timezone.utc )

    total = len(tasks)
    completed = len([t for t in tasks if t["completed"]])
    not_completed = total - completed
    overdue = len([
        t for t in tasks
        if t["deadline"] and t["deadline"] < now and not t["completed"]
    ])

    priority_stats = {
        "low": len([t for t in tasks if t["priority"] == "low"]),
        "medium": len([t for t in tasks if t["priority"] == "medium"]),
        "high": len([t for t in tasks if t["priority"] == "high"]),
    }

    return {
        "total": total,
        "completed": completed,
        "not_completed": not_completed,
        "overdue": overdue,
        "priority_distribution": priority_stats
    }