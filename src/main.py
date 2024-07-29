import uvicorn
from fastapi import FastAPI


app = FastAPI(
    name='backend app for KeyFlex project',
)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
