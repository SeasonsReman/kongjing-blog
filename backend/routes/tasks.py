from fastapi import APIRouter, HTTPException
from database import get_connection
from models import Task, TaskCreate, TaskUpdate

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=list[Task])
def get_tasks():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


@router.post("", response_model=Task)
def create_task(data: TaskCreate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (title, tag, priority, done) VALUES (?, ?, ?, 0)",
        (data.title, data.tag, data.priority)
    )
    task_id = cur.lastrowid
    conn.commit()
    cur.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row)


@router.patch("/{task_id}", response_model=Task)
def update_task(task_id: int, data: TaskUpdate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    updates = {k: v for k, v in data.dict().items() if v is not None}
    if "done" in data.dict() and data.done is not None:
        updates["done"] = 1 if data.done else 0
    if updates:
        set_clause = ", ".join(f"{k}=?" for k in updates)
        cur.execute(f"UPDATE tasks SET {set_clause} WHERE id=?", list(updates.values()) + [task_id])
        conn.commit()
    cur.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    row = cur.fetchone()
    conn.close()
    result = dict(row)
    result["done"] = bool(result["done"])
    return result


@router.delete("/{task_id}")
def delete_task(task_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return {"ok": True}
