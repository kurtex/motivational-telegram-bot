import asyncio
import os
import random
import logging
from dotenv import load_dotenv
import schedule
import time
from telegram.ext import Application
from threading import Thread
from flaskServer import keep_alive

load_dotenv()  # Load variables from .env

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is missing from the .env file!")

CHAT_ID = os.getenv("CHAT_ID") # ID of the chat where the bot will send the messages
if not CHAT_ID:
    raise ValueError("CHAT_ID is missing from the .env file!")

#  Motivational quotes
FRASES = [
    "Hoy es un buen día para empezar algo increíble.",
    "Cree en ti mismo y todo será posible.",
    "El éxito es la suma de pequeños esfuerzos repetidos cada día.",
    "Cada día es una nueva oportunidad para ser mejor.",
    "Lo único imposible es aquello que no intentas.",
    "No cuentes los días, haz que los días cuenten.",
    "Haz de cada día tu obra maestra."
]


app = Application.builder().token(TOKEN).build()

# Create a new event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

async def enviar_frase():
    """Envía una frase motivacional al usuario."""
    frase = random.choice(FRASES)
    await app.bot.send_message(chat_id=CHAT_ID, text=f"🌟 Motivación del día:\n\n{frase}")

def enviar_frase_sync():
    """Función de envoltura para llamar a la función asíncrona desde el programador."""
    asyncio.run_coroutine_threadsafe(enviar_frase(), loop)

# Schedule a job for every day at 9am
schedule.every().day.at("09:00").do(enviar_frase_sync)

def run_scheduler():
    """Ejecuta el programador en un hilo separado."""
    while True:
        schedule.run_pending()
        time.sleep(60)  

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("🤖 Bot iniciado y programado para enviar mensajes cada día.")

    keep_alive()  # Init the Flask server

    # Init the loop in a separate thread
    thread_loop = Thread(target=loop.run_forever, daemon=True)
    thread_loop.start()

    # Init the scheduler in a separate thread
    thread_schedule = Thread(target=run_scheduler, daemon=True)
    thread_schedule.start()

    thread_schedule.join()  # Keep the main thread alive