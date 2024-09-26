# AZM
# 18/09/2024

import os
from fastapi import ( FastAPI, UploadFile, File, 
                     HTTPException, Request,
                     Body, Depends, status)
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Dict

from ocr import extract
from qa_model import qa_model
from db_intitializer import get_db
from models import users as user_model
from schemas.users import CreateUserSchema, UserSchema, UserLoginSchema
from services.db import users as user_db_services

#import auth

app = FastAPI()   # fastapi instance
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
#app.include_router(auth.router)


# main page, for testing
@app.get("/")
def all_files(request: Request):
    # returns all the uploaded files
    path = f"uploaded_files/"
    return {"files" : os.listdir(path)}


@app.get("/profile/{id}", response_model=UserSchema)
def profile(id:int, session:Session=Depends(get_db)):
    """Processes request to retrieve user
    profile by id
    """
    return user_db_services.get_user_by_id(session=session, id=id)



@app.post('/login', response_model=Dict)
def login(
        payload: UserLoginSchema = Body(),
        session: Session = Depends(get_db)
    ):

    try:
        user:user_model.User = user_db_services.get_user(
            session=session, email=payload.email
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials"
        )

    is_validated:bool = user.validate_password(payload.password)
    if not is_validated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials"
        )

    return user.generate_token()


@app.post('/signup', response_model=UserSchema)
def signup(
    payload: CreateUserSchema = Body(), 
    session:Session=Depends(get_db)
):
    """Processes request to register user account."""
    payload.hashed_password = user_model.User.hash_password(payload.hashed_password)
    return user_db_services.create_user(session, user=payload)

#initialize the qa_class
qa_llm = qa_model()

# file upload, ocr and creating vector database
@app.post("/upload")
async def upload(uploaded_file: UploadFile):

    if uploaded_file.content_type not in ['application/pdf', 'image/png', 'image/jpeg']:
        raise HTTPException(status_code=400, detail="Only pdf and image(jpeg/png) files are accepted!")    
    
    try:
        file_path = f"uploaded_files/{uploaded_file.filename}"
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


    
