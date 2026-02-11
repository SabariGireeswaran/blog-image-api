from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from database import SessionLocal,engine, Base
from sqlalchemy.orm import Session
import shutil
import os

from database import SessionLocal, engine, Base
from models import Post

from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI()

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

#--------- DB session dependency ---------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#--------- CREATE POST ---------------
@app.post("/posts")
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    image_path = None

    if image:
        file_path=f"uploads/{image.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await image.read())
        image_path = file_path
    
    new_post = Post(
        title=title,
        content=content,
        image_path=image_path
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {
        "id": new_post.id,
        "title": new_post.title,
        "content": new_post.content,
        "image_url": f"/{image_path}" if image_path else None
    }

@app.get("/")
def home():
    return {"message": "Blog API  running"}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()

    result = []
    for p in posts:
        result.append({
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "image_url": f"/{p.image_path}" if p.image_path else None
        })
    return result

@app.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(404, "Post not found")
    
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "image_url": f"http://127.0.0.1:8000/{post.image_path}" if post.image_path else None
    }