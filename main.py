from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ValidationError
import uuid
import json

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data = [
    {
        "id": "cc9754c4-f619-4921-bf7e-8a4fc9714e7f",
        "name": "mock",
        "lastname": "mocklastname",
        "position": "Manager",
    },
    {
        "id": "66a3f853-5c09-4412-a380-3cc1ebf08c9c",
        "name": "employee 1",
        "lastname": "em",
        "position": "Engineer",
    },
    {
        "id": "64715e05-b45b-4aba-b6d2-d7a4f61ccf0a",
        "name": "employee 2",
        "lastname": "lord",
        "position": "Designer",
    },
]

KEYS = ["id", "name", "lastname", "position"]


class Member(BaseModel):
    id: uuid.UUID = uuid.uuid4()
    name: str
    lastname: str
    position: str


@app.get("/")
def root():
    return {"message": "Index Page"}


@app.get("/members")
def get():
    return data


@app.post("/members")
def create(member: Member):
    try:
        data.append(json.loads(member.model_dump_json()))
        return {"message": "created"}
    except ValidationError as err:
        return {"error": str(err)}


@app.put("/members")
def update(member: Member):
    global data
    for index in range(len(data)):
        if data[index]["id"] == str(member.id):
            data[index] = json.loads(member.model_dump_json())
            return {"message": "updated"}

    return {"message": "ID not found."}


@app.delete("/member/{member_id}")
def delete(member_id: str):
    global data
    new_data = filter(lambda member: member["id"] != member_id, data)
    data = list(new_data)
    return {"message": "deleted {member_id}".format(member_id=member_id)}
