# AZM
# 18/09/2024


from typing import Optional
from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import pytesseract
from PIL import Image
app = FastAPI()   # fastapi instance



@app.get("/")
def all_files():
    # returns all the uploaded files
    path = f"/home/azm/projects/ocr_chatbot/uploaded_files"
    return {"files" : os.listdir(path)}

@app.post("/upload")
async def upload(uploaded_file: UploadFile):

    if uploaded_file.content_type not in ['application/pdf', 'image/png', 'image/jpeg']:
        raise HTTPException(status_code=400, detail="Only pdf and image(jpeg/png) files are accepted!")
    try:
        file_path = f"/home/azm/projects/ocr_chatbot/uploaded_files/{uploaded_file.filename}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.file.read())
            curr_img = pytesseract.image_to_string(Image.open('test-european.jpg'), lang='fra')
            print (curr_img)
            return {"message": "file saved successfully", "filename": uploaded_file.filename, "filetype" : uploaded_file.content_type, "extracted_text": curr_img}
    except Exception as e:
        return {"message": e.args}
    
