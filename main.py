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
        "id": uuid.uuid4(),
        "name": "mock",
        "lastname": "mocklastname",
        "position": "Manager",
    },
    {
        "id": uuid.uuid4(),
        "name": "employee 1",
        "lastname": "em",
        "position": "Engineer",
    },
    {
        "id": uuid.uuid4(),
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


@app.get("/members/{member_id}")
def get_by_id(member_id: uuid.UUID):
    global data
    new_data = filter(lambda member: member["id"] == member_id, data)
    one_data = list(new_data)
    if len(one_data) == 0:
        return {"message": "Not found"}

    return one_data[0]


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
