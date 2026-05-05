from fastapi import FastAPI, HTTPException, Query
from models import Task
import storage
from datetime import datetime
from typing import Optional

app = FastAPI()

#1. GET /
@app.get("/")
def root():
    return {"message": "Advanced Task API", "version": "2.0"}

#2. GET /tasks
@app.get("/tasks")
def get_tasks(
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    limit: Optional[int] = None,
    sort_by: Optional[str] = None
):
    return storage.get_all_tasks(completed, priority, limit, sort_by)

#3. GET /tasks/{task_id}
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = storage.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

#4. POST /tasks
@app.post("/tasks")
def create(task: Task):
    try:
        return storage.create_task(task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

#5. PUT /tasks/{task_id}
@app.put("/tasks/{task_id}")
def update(task_id: int, new_task: Task):
    result = storage.update_task(task_id, new_task)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result

#6. PATCH /tasks/{task_id}
@app.patch("/tasks/{task_id}")
def patch(task_id: int, data: dict):
    result = storage.patch_task(task_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result

#7. PATCH /tasks/{task_id}/complete
@app.patch("/tasks/{task_id}/complete")
def complete(task_id: int):
    try:
        result = storage.complete_task(task_id)
        if not result:
            raise HTTPException(status_code=404, detail="Task not found")
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

#8. DELETE /tasks/{task_id}
@app.delete("/tasks/{task_id}")
def delete(task_id: int):
    result = storage.delete_task(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}

#9. GET /tasks/search
@app.get("/tasks/search")
def search(
    keyword: Optional[str] = None,
    priority: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None
):
    return storage.search_tasks(keyword, priority, date_from, date_to)

#10. GET /tasks/stats
@app.get("/tasks/stats")
def stats():
    return storage.get_stats()