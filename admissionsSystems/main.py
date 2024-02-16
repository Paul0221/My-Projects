from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "This will be the home page"}


@app.get("/upload")
async def upload():
    return {"message": "This will be the page where students upload their grades & personal statements"}


@app.get("/view_applicants")
async def view_applicants():
    return {"message": "This will be the main page for admissions team"}
