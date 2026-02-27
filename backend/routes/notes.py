from fastapi import APIRouter
from database import get_connection
from models import Note, NoteCreate
from datetime import datetime

router = APIRouter(prefix="/api/notes", tags=["notes"])


@router.get("", response_model=list[Note])
def get_notes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM notes ORDER BY created_at DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


@router.post("", response_model=Note)
def create_note(data: NoteCreate):
    conn = get_connection()
    cur = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("INSERT INTO notes (content, created_at) VALUES (?, ?)", (data.content, now))
    note_id = cur.lastrowid
    conn.commit()
    cur.execute("SELECT * FROM notes WHERE id=?", (note_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row)


@router.delete("/{note_id}")
def delete_note(note_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
    return {"ok": True}
