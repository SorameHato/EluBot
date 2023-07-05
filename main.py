# coding: utf-8
import discord
from discord.ext import commands
import asyncio
from datetime import datetime as dt
import os
import sys
from skylib import tui
bot = discord.Bot()
elu_ver = "0.0 rev 1 build 1 @ 20230704"
guild_ids = [
    1030056186915082262 #테스트용 서버
    ]
bot.elu_ver = elu_ver

@bot.event
async def on_ready():
    global LoadedTime
    LoadedTime = str(dt.now().strftime("%Y년 %m월 %d일 %H시 %M분 %S.%f"))[:-3]+"초"
    bot.LoadedTime = LoadedTime
    print('┌──────────────────────────────────────────────────────────────────────┐')
    print('│'+tui.fixedWidth(f'{bot.user.name}(#{bot.user.id})으로 로그인되었습니다.',70,1)+'│')
    print('│'+tui.fixedWidth(f'봇이 시작된 시각 : {LoadedTime}',70,1)+'│')
    print('└──────────────────────────────────────────────────────────────────────┘')
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name='/도움말 | 에루봇 α'))

@bot.event
async def on_application_command_error(ctx, error):
    embed = discord.Embed(title='자세한 내용',description=error,color=0xfae5fa)
    embed.add_field(name="보낸 분",value=ctx.author,inline=False)
    embed.add_field(name="보낸 내용",value=ctx.message,inline=False)
    embed.set_footer(text=f'에루봇 버전 {ver}')
    await ctx.respond('아무래도 바보토끼가 또 바보토끼 한 것 같아요. 하토를 불러주세요!',embed=embed)
    raise error

def load_extensions():
    for filename in os.listdir('Cogs'):
        if filename.endswith('.py'):
            bot.load_extension('Cogs.{}'.format(filename[:-3]))

load_extensions()

with open('token.txt','r') as token:
    bot.run(token.readline())
