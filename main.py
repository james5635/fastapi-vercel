from contextlib import asynccontextmanager
from http import HTTPStatus
from telegram import Update
from telegram.ext import Application, CommandHandler
from telegram.ext._contexttypes import ContextTypes
from fastapi import FastAPI, Request, Response
from dotenv import load_dotenv
import os
from typing import Final
load_dotenv()
TOKEN: Final = os.getenv("TOKEN") or ""
WEBHOOK_URL : Final = os.getenv("WEBHOOK_URL") or ""

# Initialize python telegram bot
ptb = (
    Application.builder()
    .updater(None)
    .token(TOKEN) # replace <your-bot-token>
    .read_timeout(7)
    .get_updates_read_timeout(42)
    .build()
)

@asynccontextmanager
async def lifespan(_: FastAPI):
    await ptb.bot.setWebhook("") # replace <your-webhook-url>
    async with ptb:
        await ptb.start()
        yield
        await ptb.stop()

# Initialize FastAPI app (similar to Flask)
app = FastAPI(lifespan=lifespan)

@app.post("/")
async def process_update(request: Request):

    req = await request.json()
    print(req)
    update = Update.de_json(req, ptb.bot)
    await ptb.process_update(update)
    return Response(status_code=HTTPStatus.OK)
@app.get("/")
def hello():
    return "hello world"

# Example handler
async def start(update, _: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text("starting...")




if __name__ == "__main__":
    import uvicorn
    ptb.add_handler(CommandHandler("start", start))
    uvicorn.run(app)