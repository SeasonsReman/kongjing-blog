from fastapi import APIRouter, HTTPException
from database import get_connection
from models import Post, PostCreate, PostUpdate
from datetime import datetime

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.get("", response_model=list[Post])
def get_posts(category: str = None, mood: str = None):
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT * FROM posts WHERE 1=1"
    params = []
    if category:
        query += " AND category = ?"
        params.append(category)
    if mood:
        query += " AND mood = ?"
        params.append(mood)
    query += " ORDER BY date DESC"
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


@router.post("", response_model=Post)
def create_post(data: PostCreate):
    conn = get_connection()
    cur = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cur.execute(
        "INSERT INTO posts (title,summary,content,category,mood,cover_image,date,views,likes) VALUES (?,?,?,?,?,?,?,0,0)",
        (data.title, data.summary, data.content, data.category, data.mood, data.cover_image, today)
    )
    post_id = cur.lastrowid
    conn.commit()
    cur.execute("SELECT * FROM posts WHERE id=?", (post_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row)


@router.get("/{post_id}", response_model=Post)
def get_post(post_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE posts SET views = views + 1 WHERE id=?", (post_id,))
    conn.commit()
    cur.execute("SELECT * FROM posts WHERE id=?", (post_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Post not found")
    return dict(row)


@router.put("/{post_id}", response_model=Post)
def update_post(post_id: int, data: PostUpdate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts WHERE id=?", (post_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Post not found")
    updates = {k: v for k, v in data.dict().items() if v is not None}
    if updates:
        set_clause = ", ".join(f"{k}=?" for k in updates)
        cur.execute(f"UPDATE posts SET {set_clause} WHERE id=?", list(updates.values()) + [post_id])
        conn.commit()
    cur.execute("SELECT * FROM posts WHERE id=?", (post_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row)


@router.delete("/{post_id}")
def delete_post(post_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM posts WHERE id=?", (post_id,))
    conn.commit()
    conn.close()
    return {"ok": True}


@router.post("/{post_id}/like")
def like_post(post_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE posts SET likes = likes + 1 WHERE id=?", (post_id,))
    conn.commit()
    cur.execute("SELECT likes FROM posts WHERE id=?", (post_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"likes": row["likes"]}
