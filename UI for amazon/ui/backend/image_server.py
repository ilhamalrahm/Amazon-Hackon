from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
import cv2 
import sys
import shutil
app=FastAPI()

@app.post("/img")
async def create_file(file:UploadFile):
    with open(f"{file.filename}","wb") as buf:
        shutil.copyfileobj(file.file,buf)
    
    image = cv2.imread(os.path.join(os.getcwd(),file.filename))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
    )

    print("[INFO] Found {0} Faces!".format(len(faces)))
    k=10
    print(image.shape)
    for (x, y, w, h) in faces:
        startx=int(max(x-k,0))
        endx=int(min(x+w+k,image.shape[0]))
        starty=int(max(y-k,0))
        endy=int(min(y+h+k,image.shape[1]))
        cv2.imwrite('faces_cropped.jpg', image[starty:endy,startx:endx])
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    status = cv2.imwrite('faces_detected.jpg', image)
    return FileResponse(os.path.join(os.getcwd(),'faces_cropped.jpg'))