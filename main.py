from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()         #Initialize 

class Paitent(BaseModel):
    
    id : Annotated[str, Field(..., description='Id of the paitent', examples=['P001'])]
    name : Annotated[str, Field(..., description='Name of the paitent')]
    city : Annotated[str, Field(..., description='City in which the paitent is living')]
    age : Annotated[int, Field(..., gt=0, lt= 120, description='Age of the paitent')]
    gender : Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the paitent')]
    height : Annotated[float, Field(..., gt=0, description='Height of the paitent in mtrs')]
    weight : Annotated[float, Field(..., gt=0, description='Weight of the paitent in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round((self.weight)/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'

class updatePaitent(BaseModel):
    name : Annotated[Optional[str],Field(default=None)]
    city : Annotated[Optional[str], Field(default=None)]
    age : Annotated[Optional[int], Field(default=None)]
    gender : Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None)]
    height : Annotated[Optional[float], Field(default=None)]
    weight : Annotated[Optional[float], Field(default=None)]

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data 

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

@app.get("/")                   #Route, Endpoint
def hello():                                            
    return {'message':'Patient Management System'}          #Response

@app.get("/about")
def about():
    return {'message':'A fully functional API to manage your patient records.'}

@app.get("/view")
def view():
    data = load_data()          #Load data from Json file
    return data                 #return data as response


#Path parameter
@app.get("/patient/{patient_id}")               #to find the info of a specific patient  
def view_patient(patient_id:str = Path(...,description='ID of patient in the DB', example='P001')):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')

#Query parameter
@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'), order: str = Query('asc', description='Sort in asc or desc')):
    valid_feilds = ['height', 'weight', 'bmi']

    if sort_by not in valid_feilds:
        raise HTTPException(status_code=400, detail = f'Invalid feild select from {valid_feilds}')
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400, detail='Invalid order select by asc or desc')
    
    data = load_data()  
    sort_order = True if order=='desc' else False
    sorted_data = sorted(data.values(), key=lambda x:x.get(sort_by, 0), reverse=sort_order)
    return sorted_data

@app.post("/post")
def create_patient(patient: Paitent):
    #load exisitng data
    data = load_data()

    #check if the patient already exist in the database
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    #new patient add to the database
    data[patient.id] = patient.model_dump(exclude=['id'])

    #save into json file 
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'Paitent created successfully'})

@app.put('/edit/{paitent_id}')
def update_paitent(paitent_id:str, paitent_update:updatePaitent):

    data = load_data()

    if paitent_id not in data:
        raise HTTPException(status_code=404, detail='Paitent not found')
    
    exisiting_paitent_info = data[paitent_id]

    updated_paintent_info = paitent_update.model_dump(exclude_unset = True)

    for key, value in updated_paintent_info.items():
        exisiting_paitent_info[key] = value

        exisiting_paitent_info['id'] = paitent_id
        paitent_pydantic_object = Paitent(**exisiting_paitent_info)

        exisiting_paitent_info = paitent_pydantic_object.model_dump(exclude=id)


        data[paitent_id] = exisiting_paitent_info

        save_data(data)

        return JSONResponse(status_code=200, content={'message':'Paitent information updated'})
    

@app.delete('/delete/{paitent_id}')
def delete_paitent(paitent_id: str):

    data = load_data()

    if paitent_id not in data:
        raise HTTPException(status_code=404, detail='Paitent not found')
    
    del data[paitent_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message' : 'Paitent deleted successfully'})

