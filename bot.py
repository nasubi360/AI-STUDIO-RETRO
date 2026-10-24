import discord
from google import genai

GEMINI_API_KEY = "AQ.Ab8RN6LrbSyJ7MBp7BxM_lt1rRUs6uaEvA-AyQPsPUi0guXmcg"
DISCORD_TOKEN = "MTU2MzM3OTk4NDAzNzMxNDY3MA.GJThmk.vAmwSVPrxqeVQ6QCyhpHWlu2My0b6JDlfUpOMk"

client_genai = genai.Client(api_key=GEMINI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
bot_client = discord.Client(intents=intents)

@bot_client.event
async def on_ready():
    print(f"ログインしました: {bot_client.user}")

@bot_client.event
async def on_message(message):
    if message.author == bot_client.user:
        return

    if message.content.startswith("!code"):
        code_text = message.content.replace("!code", "").strip()
        if not code_text:
            await message.channel.send("直してほしいコードやエラー文を後ろに書いてね！")
            return
        response = client_genai.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"以下のプログラミングコードのミスを指摘し、修正案を教えてください:\n{code_text}"
        )
        await message.channel.send(response.text)

    elif message.content.startswith("!sodan"):
        trouble_text = message.content.replace("!sodan", "").strip()
        if not trouble_text:
            await message.channel.send("相談内容を後ろに書いてね！")
            return
        response = client_genai.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"あなたは優しいカウンセラーAIです。以下の相談に温かくアドバイスしてください:\n{trouble_text}"
        )
        await message.channel.send(response.text)

bot_client.run(DISCORD_TOKEN)
