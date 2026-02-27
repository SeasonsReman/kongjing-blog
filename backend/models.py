from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PostCreate(BaseModel):
    title: str
    summary: str
    content: str
    category: str
    mood: str
    cover_image: Optional[str] = None


class PostUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    mood: Optional[str] = None
    cover_image: Optional[str] = None


class Post(BaseModel):
    id: int
    title: str
    summary: str
    content: str
    category: str
    mood: str
    cover_image: Optional[str]
    date: str
    views: int
    likes: int

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    title: str
    tag: str
    priority: Optional[str] = "普通"


class TaskUpdate(BaseModel):
    done: Optional[bool] = None
    title: Optional[str] = None
    tag: Optional[str] = None


class Task(BaseModel):
    id: int
    title: str
    tag: str
    priority: str
    done: bool

    class Config:
        from_attributes = True


class NoteCreate(BaseModel):
    content: str


class Note(BaseModel):
    id: int
    content: str
    created_at: str

    class Config:
        from_attributes = True
