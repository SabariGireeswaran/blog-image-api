from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from database import SessionLocal,engine, Base
from sqlalchemy.orm import Session
import shutil
import os

from database import SessionLocal, engine, Base
from models import Post

Base.metadata.create_all(bind=engine)

app = FastAPI()

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
def create_post(
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    try:
        image_path = None
        if image:
            os.makedirs("uploads", exist_ok=True)
            file_path=f"uploads/{image.filename}"

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)

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
                "image_path": new_post.image_path
            }
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def home():
    return {"message": "Blog API  running"}