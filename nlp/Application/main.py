from fastapi import FastAPI, Body
from huggingfaceSequence import (loadmodel, loaddata, get_myoptimizer, 
                                compute_metrics, postprocess, myEvaluator, 
                                evaluate_dataset, evaluateSeq_dataset, evaluateQA_dataset)
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

class Data(BaseModel):
    task: str
    text: str

model_checkpoint_translation =  pipeline("translation_en_to_de")
model_checkpoint_summarization = pipeline("summarization")
model_checkpoint_qa = pipeline("question-answering")

translation_pipeline = pipeline("translation", model=model_checkpoint_translation)
summarization_pipeline = pipeline("summarization", model=model_checkpoint_summarization)
qa_pipeline = pipeline("question-answering", model=model_checkpoint_qa)

@app.post("/process")
def process_text(data: Data = Body(...)):
    task = data.task
    text_input = data.text

    if task == "Translation":
        output = translation_pipeline(text_input)[0]["translation_text"]

    elif task == "Summarization":
        output = summarization_pipeline(text_input, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]

    elif task == "Question Answering":
        question, context = text_input.split(" ||| ")  # Split using a delimiter
        output = qa_pipeline({"question": question, "context": context})["answer"]

    return {"output": output}
