from fastapi import FastAPI
from multiprocessing import Process
import bot

app = FastAPI()


@app.get("/")
def hello_world():
    return {"hello world": "From Web"}


if __name__ == "__main__":
    import uvicorn
    t = Process(target=bot.run)
    t1 = Process(target=uvicorn.run, args=[app])
    t.start()
    t1.start()
    t.join()
    t1.join()
    # uvicorn.run(app)
