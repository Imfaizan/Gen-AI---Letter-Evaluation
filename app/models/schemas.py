from pydantic import BaseModel

class LetterEvaluationRequest(BaseModel):
    input_letter: str

class LetterEvaluationResponse(BaseModel):
    highlighted_letter: str
