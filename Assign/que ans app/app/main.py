# app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mistral_integration import get_mistral_model, generate_questions_and_answers

app = FastAPI()

# Load the model once when the app starts
model = get_mistral_model()

class ParagraphInput(BaseModel):
    paragraph: str

class QAOutput(BaseModel):
    questions_and_answers: dict

@app.post("/generate-qa", response_model=QAOutput)
async def generate_qa(paragraph_input: ParagraphInput):
    try:
        questions_and_answers = generate_questions_and_answers(paragraph_input.paragraph, model)
        return {"questions_and_answers": questions_and_answers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
