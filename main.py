from fastapi import FastAPI, HTTPException, Form, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List
import pandas as pd
import random

app = FastAPI(title="Students APIs")

class Student(BaseModel):
    Name : str
    Roll_no : int = random.randint(0,1000)
    Emailid : str
    City : Optional[str] = 'Bangalore'

Db = []

@app.get('/')
async def index():
    return({"Status" : 200, "Output" : "Sever is running..."})

@app.post("/uploadfile/")
def create_upload_file(file: UploadFile = File(...)):
    # contents = await file.read()
    if file.filename.endswith('.csv'):
        df = pd.read_csv(file.file)
        contents = df.to_dict('record')
        return {"filename": file.filename, "Content": contents}

@app.get('/students')
def getAllStudents():
    global Db
    print(Db)
    return {"Status":200, "Output": Db}

@app.get('/students/{Roll_no}') #path parameters
def getStudent(Roll_no : int):
    global Db
    lst = list()
    found = False
    for item in Db:
        if item['Roll_no'] == Roll_no:
            lst.append(item)
            found = True

    if found:
        return {"Status":200, "Output":lst}
    else:
        raise HTTPException(status_code=412, detail="Roll No does not exist")


@app.post('/students/')
def createStudent(student: Student):
    global Db
    dict1 = {
        "Name":student.Name,
        "Roll_no": student.Roll_no,
        "Emailid": student.Emailid,
        "City": student.City
    }
    Db.append(dict1)
    print(Db)
    print("************************")
    # return {"Status": 200, "Output": dict1} #dict1 is same as student
    return {"Status":200, "Output":student}

@app.delete('/students/{Roll_no}')
def deleteStudent(Roll_no: int):
    global Db
    found = False
    for item in Db:
        if item['Roll_no'] == Roll_no:
            del Db[Db.index(item)]
            found = True
            break
    if found:
        return {"Status":200, "Output": item}
    else:
        raise HTTPException(status_code=412, detail="Roll No does not exist")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
