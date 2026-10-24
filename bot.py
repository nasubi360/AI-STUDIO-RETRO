import discord
from google import genai
from flask import Flask
from threading import Thread
import os

# --- 1. 24時間稼働のためのWebサーバー設定 (Render対策) ---
app = Flask('')

@app.route('/')
def home():
    return "I am alive and the bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. AIとDiscordボットの初期設定 ---
# ※ここに実際のAPIキーとDiscordトークンを入れてね！
GEMINI_API_KEY = "AQ.Ab8RN6LrbSyJ7MBp7BxM_lt1rRUs6uaEvA-AyQPsPUi0guXmcg"
DISCORD_TOKEN = "MTU2MzM3OTk4NDAzNzMxNDY3MA.GJYhJ4.GBWaGn6EN5ifthqaCyH6_LLt_9r7cqeYC0Upd4"

client_genai = genai.Client(api_key=GEMINI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
bot_client = discord.Client(intents=intents)

@bot_client.event
async def on_ready():
    print(f"ログインしました: {bot_client.user}")

@bot_client.event
async def on_message(message):
    # ボット自身の発言には反応しない
    if message.author == bot_client.user:
        return

    # ① !code で始まるメッセージ（コードミス指摘AI）
    if message.content.startswith("!code"):
        code_text = message.content.replace("!code", "").strip()
        if not code_text:
            await message.channel.send("直してほしいコードやエラー文を後ろに書いてね！例: `!code print('hello'`")
            return
            
        try:
            response = client_genai.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"以下のプログラミングコードやエラーログのミスを指摘し、修正案をわかりやすく教えてください:\n{code_text}"
            )
            await message.channel.send(response.text)
        except Exception as e:
            await message.channel.send(f"エラーが発生しました: {e}")

    # ② !sodan で始まるメッセージ（相談AI）
    elif message.content.startswith("!sodan"):
        trouble_text = message.content.replace("!sodan", "").strip()
        if not trouble_text:
            await message.channel.send("相談内容を後ろに書いてね！例: `!sodan 課題が難しくて泣きそう`")
            return
            
        try:
            response = client_genai.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"あなたはサークルメンバーのメンタルケアや悩み相談に乗る優しく共感力の高いカウンセラーAIです。以下の相談に対して、温かく、かつ建設的なアドバイスを返してください:\n{trouble_text}"
            )
            await message.channel.send(response.text)
        except Exception as e:
            await message.channel.send(f"エラーが発生しました: {e}")

# --- 3. 起動 ---
if __name__ == "__main__":
    # Webサーバーをバックグラウンドで起動
    keep_alive()
    # Discordボットを起動
    bot_client.run(DISCORD_TOKEN)