from PIL import Image
import pytesseract


#file = "/home/azm/projects/ocr_chatbot/uploaded_files/New Image.jpg"

def extract(file: str):
    image = Image.open(file)
    text = pytesseract.image_to_string(image)
    #print (text)
    return text
      

