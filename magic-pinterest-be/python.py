print("emo ca behet ktej")


from fastapi import FastAPI
from typing import Optional

# 1. Initialize the FastAPI application instance
app = FastAPI()

# 2. Define a basic GET endpoint at the root URL
@app.get("/")
def read_root():
    return {"message": "Welcome to my Python API yaayy punoi!"}

# 3. Define a GET endpoint with a path parameter and an optional query parameter
@app.get("/photo/")
def read_item( q: Optional[str] = None):
    return {
        "query_param": q,
        "status": "Success"
    }