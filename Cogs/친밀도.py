# coding: utf-8
import discord
from discord.ext import commands
global guild_ids
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from main import guild_ids
from FriendlyPoint import 

'''친밀도와 관련된 작업을 하는 프론트엔드
정보 명령어도 여기에 있고 다른 파일에서 쓰일 친밀함 여부를 정하는 것도 이 파일
표준(0~30 정도는 소심한 척 / 30~75는 조금 마음을 여는 듯 / 75~150은 마음을 완전히 열음 / 150~600은 호감을 보임 / 600 이상은 좋아하는 것 같이 달콤하게)을 따르는 명령어를 위해 0 1 2 3 4로 리턴하는 함수도 만들고
표준을 따르지 않는 명령어를 위해 친밀도 수치를 그대로 리턴하는 함수도 만들어야 함
물론 이 두 함수는 클래스 바깥에 있어야 한다!
'''

class FriendlyPointFrontend(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

async def setup(bot):
    await commands.add_cog(FriendlyPointFrontend(bot))