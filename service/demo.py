from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_healthcheck():
    return {"status": "Green"}

if __name__ == '__main__':
    uvicorn.run(app='demo:app', host="127.0.0.1", port=8000, reload=True, debug=True)