from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel


app = FastAPI()


# Data model for the name input
class Name(BaseModel):
    name: str


stored_name = None


# Endpoint to post a name
@app.post("/post-name/", tags=["Names"])
def post_name(name: Name = Body(...)):
    global stored_name
    stored_name = name.name
    return {"message": f"Hello, {name.name}! Your name has been saved."}


# Endpoint to get the stored name
@app.get("/get-name/", tags=["Names"])
def get_name():
    #global stored_name
    if stored_name:
        return {"message": f"Hello, {stored_name}! This is your stored name."}
    else:
        raise HTTPException(status_code=404, detail="Name not found")