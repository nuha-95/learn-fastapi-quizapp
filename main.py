from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, sessionLocal
from sqlalchemy.orm import Session

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class choiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class questionBase(BaseModel):
    question_text: str
    choises: List[choiceBase]

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "QuizApp API is running"}

@app.get("/questions/{question_id}")
async def read_question(question_id: int, db: db_dependency):
    result = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not result:
        raise HTTPException(status_code=404, detail='Question is not found.')
    return result

@app.get("/choices/{question_id}")
async def read_choices(question_id: int, db: db_dependency):
    result = db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    if not result:
        raise HTTPException(status_code=404, detail='Choices not found.')
    return result

@app.get("/stats")
async def get_stats(db: db_dependency):
    total_questions = db.query(models.Questions).count()
    total_choices = db.query(models.Choices).count()
    return {
        "total_questions": total_questions,
        "total_choices": total_choices,
        "avg_choices_per_question": round(total_choices / total_questions, 2) if total_questions > 0 else 0
    }

@app.get("/questions/")
async def get_all_questions(db: db_dependency):
    questions = db.query(models.Questions).all()
    return questions

@app.post("/questions/")
async def create_questions(question: questionBase, db: db_dependency):
    db_questions = models.Questions(question_text=question.question_text)
    db.add(db_questions)
    db.commit()
    db.refresh(db_questions)
    for choice in question.choises:
        db_choice = models.Choices(choice_text=choice.choice_text, is_correct=choice.is_correct, question_id=db_questions.id)
        db.add(db_choice)
    db.commit()
    return {"id": db_questions.id, "message": "Question created successfully"}

@app.put("/questions/{question_id}")
async def update_question(question_id: int, question: questionBase, db: db_dependency):
    db_question = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail='Question not found.')
    
    db_question.question_text = question.question_text
    db.query(models.Choices).filter(models.Choices.question_id == question_id).delete()
    
    for choice in question.choises:
        db_choice = models.Choices(choice_text=choice.choice_text, is_correct=choice.is_correct, question_id=question_id)
        db.add(db_choice)
    
    db.commit()
    return {"message": "Question updated successfully"}

@app.delete("/questions/{question_id}")
async def delete_question(question_id: int, db: db_dependency):
    db_question = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail='Question not found.')
    
    db.query(models.Choices).filter(models.Choices.question_id == question_id).delete()
    db.query(models.Questions).filter(models.Questions.id == question_id).delete()
    db.commit()
    return {"message": "Question deleted successfully"}

# Mount the folder to serve the HTML file directly
app.mount("/terminal_static", StaticFiles(directory="static_terminal"), name="terminal_static")

# Serve the terminal doc as a page at /terminal
@app.get("/terminal", include_in_schema=False)
async def serve_terminal():
    return FileResponse(os.path.join("static_terminal", "index.html"))
