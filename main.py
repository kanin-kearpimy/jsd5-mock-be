from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ValidationError
import uuid

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
        "name": "Mock Name",
        "age": 99,
        "weight": 63.5,
        "status": "health",
    },
    {
        "id": "66a3f853-5c09-4412-a380-3cc1ebf08c9c",
        "name": "John Doe",
        "age": 35,
        "weight": 78.2,
        "status": "active",
    },
    {
        "id": "64715e05-b45b-4aba-b6d2-d7a4f61ccf0a",
        "name": "Alice Smith",
        "age": 28,
        "weight": 54.9,
        "status": "health",
    },
    {
        "id": "61ec7ef2-f2e5-460c-bfd0-c060a99d0f50",
        "name": "Jane Johnson",
        "age": 42,
        "weight": 67.0,
        "status": "recovered",
    },
    {
        "id": "6b72fbe1-5c72-42bb-a25f-8d00cef7e88a",
        "name": "Bob Brown",
        "age": 55,
        "weight": 80.7,
        "status": "health",
    },
]

KEYS = ["id", "name", "age", "weight", "status"]


class Member(BaseModel):
    id: uuid.UUID = uuid.uuid4()
    name: str
    age: int
    weight: float
    status: str


@app.get("/")
def root():
    return {"message": "Index Page"}


@app.get("/members")
def get():
    return data


@app.get("/members/{member_id}")
def get_by_id(member_id: str):
    global data
    new_data = filter(lambda member: member["id"] == member_id, data)
    one_data = list(new_data)
    if len(one_data) == 0:
        return {"message": "Not found"}

    return one_data[0]


@app.post("/members")
def create(member: Member):
    try:
        data.append(member)
        return {"message": "created"}
    except ValidationError as err:
        return {"error": str(err)}


@app.put("/members")
def update(member: Member):
    for index in range(len(data)):
        if data[index]["id"] == str(member.id):
            data[index] = member
            return {"message": "updated"}

    return {"message": "ID not found."}


@app.delete("/member/{member_id}")
def delete(member_id: str):
    global data
    new_data = filter(lambda member: member["id"] != member_id, data)
    data = list(new_data)
    return {"message": "deleted {member_id}"}
