from fastapi import FastAPI, Response, status
from app.schema import createData
import pymongo
from bson.objectid import ObjectId as BsonObjectId


myclient = pymongo.MongoClient('mongodb://127.0.0.1:27017')
app = FastAPI()

mydb = myclient['fastapi']
mytable = mydb['users']


@app.get('/', status_code=status.HTTP_200_OK)
def root(id, name):
    print(id, name)
    return{"body": "welcome to the users server"}


@app.get('/getuser', status_code=status.HTTP_200_OK)
def getusers():
    user = mytable.find()
    users = []
    for i in user:
        i['_id'] = str(i['_id'])
        users.append(i)
    return{"data": users}


@app.post('/createuser', status_code=status.HTTP_201_CREATED)
def createdata(data: createData):
    user = data.dict()
    x = mytable.insert_one(user)
    user = mytable.find_one({"_id": x.inserted_id})
    print(type(x.inserted_id))
    user['_id'] = str(x.inserted_id)
    return{"data": user}


@app.put('/updateuser/{id}', status_code=status.HTTP_202_ACCEPTED)
def updateuser(id, data: createData, responce: Response):
    d = data.dict()
    if len(id) != 24:
        responce.status_code = status.HTTP_404_NOT_FOUND
        return{"data": f"user {id} not found or miss length of user id"}
    user = mytable.find_one_and_update(
        {"_id": BsonObjectId(id)}, {"$set": d})
    if not user:
        responce.status_code = status.HTTP_404_NOT_FOUND
        return{"data": f"user {id} not found"}
    user['_id'] = str(user['_id'])
    return{"data": user}


@app.delete('/deleteuser/{id}', status_code=status.HTTP_204_NO_CONTENT)
def deluser(id: str, responce: Response):
    user = mytable.delete_one({"_id": BsonObjectId(id)})
    if user.deleted_count == 0:
        responce.status_code = status.HTTP_404_NOT_FOUND
        return{"data": f"user {id} not found"}
    return {"data": f"{id} user deleted"}


@app.get('/user/{id}', status_code=status.HTTP_200_OK)
def finduser(id, responce: Response):
    user = mytable.find_one({"_id": BsonObjectId(id)})
    print(user)
    if not user:
        responce.status_code = status.HTTP_404_NOT_FOUND
        return{"data": f"user {id} not found"}
    user['_id'] = str(user['_id'])
    return{"data": user}
