# AZM
# 18/09/2024

import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from ocr import extract
from qa_model import qa_model

app = FastAPI()   # fastapi instance


# main page, for testing
@app.get("/")
def all_files(request: Request):
    # returns all the uploaded files
    path = f"/home/azm/projects/ocr_chatbot/uploaded_files"
    return {"files" : os.listdir(path)}

#initialize the qa_class
qa_llm = qa_model()

# file upload, ocr and creating vector database
@app.post("/upload")
async def upload(uploaded_file: UploadFile):

    if uploaded_file.content_type not in ['application/pdf', 'image/png', 'image/jpeg']:
        raise HTTPException(status_code=400, detail="Only pdf and image(jpeg/png) files are accepted!")    
    
    try:
        file_path = f"/home/azm/projects/ocr_chatbot/uploaded_files/{uploaded_file.filename}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.file.read())
        extracted_text = extract(file_path)

        
        # chunk and make vectorbase for the document 
        txt_chunks = qa_llm.get_text_chunks(extracted_text)
        qa_llm.generate_embeddings()
        db = qa_llm.create_vectorstore()
        return {
            "extracted_text": extracted_text
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail= e.args)

# initialize llm chain and load local mistral model
@app.get("/init_pipeline")
def init_pipeline():
    try:
        qa_llm.llm_pipeline()
        return { "message " : " Pipeline successfully intitalized "}
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.args)


# endpoint for asking questions with existing 
@app.get("/ask")
def ask_(question:str):
    try:
        ans = qa_llm.get_answer(question=question)
        return {"Answer: " :ans}
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.args)


    
