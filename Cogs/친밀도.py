# coding: utf-8
import discord, random
from discord.ext import commands
global guild_ids
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from main import guild_ids
from FriendlyRate import getCommandCount, getDayCount, getPenalty, getLastCallDate, getFriendlyRate, getRegisterDate, register, commandCallCalc

'''친밀도와 관련된 작업을 하는 프론트엔드
정보 명령어도 여기에 있고 다른 파일에서 쓰일 친밀함 여부를 정하는 것도 이 파일
표준(0~30 정도는 소심한 척 / 30~75는 조금 마음을 여는 듯 / 75~210은 마음을 완전히 열음 / 210~600은 호감을 보임 / 600 이상은 좋아하는 것 같이 달콤하게)을 따르는 명령어를 위해 0 1 2 3 4로 리턴하는 함수도 만들고
표준을 따르지 않는 명령어를 위해 친밀도 수치를 그대로 리턴하는 함수도 만들어야 함
물론 이 두 함수는 클래스 바깥에 있어야 한다!

에루짱의 색상은 임시로 fdeccf (머리 색에서 따옴)
'''

def friendlyRate(uid:int):
    friendly_rate = getFriendlyRate(uid)
    if friendly_rate <= 30:
        return 0
    elif friendly_rate <= 75:
        return 1
    elif friendly_rate <= 210:
        return 2
    elif friendly_rate <= 600:
        return 3
    else:
        return 4
    
def friendlyRateOrg(uid:int):
    return getFriendlyRate(uid)

class FriendlyRateFrontend(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.slash_command(name='호감도',guild_ids=guild_ids,description='자신의 호감도 현황을 볼 수 있어요!')
    async def friendlyRate_FrontEnd(self, ctx):
        friendly_rate = friendlyRate(ctx.author.id)
        match friendly_rate:
            case 0:
                e_title = f'현재 호감도는 {friendly_rate}입니다.'
                e_desc = random.choice(['브라이트 버니 사장 딸, 진저 에루라고 합니다. 잘 부탁드립니다.','저는 지금 목조 건물 마을에서 지내고 있습니다. 풍경도 좋고 좋은 사람들도 있어서 살기 좋은 마을 같습니다.', '브라이트 버니는 전국적으로 가맹점을 가지고 있는 유명한 커피 체인입니다. 언젠가 한 번 들려주시기를 고대하겠습니다.'])
            case 1:
                e_title = f'현재 호감도는 {friendly_rate}이에요.'
                e_desc = random.choice(['브라이트 버니 사장 딸, 진저 에루라고 해요. 잘 부탁드립니다.','목조 건물 마을에는 \'래빗 하우스\'라는 역사가 깊은 커피숍이 있습니다. 소문에 따르면 저녁에는 어른들의 공간으로 바뀐다고 해요.', '진저 나츠메라는 쌍둥이 동생이 있습니다. 왜인지 사람들은 나츠메가 언니인 것 같다고 그러지만, 제가 언니에요.'])
            case 2:
                e_title = f'현재 호감도는 {friendly_rate}이에요!'
                e_desc = random.choice(['브라이트 버니 사장 딸, 진저 에루라고 해요. 잘 부탁드려요!','브라이트 버니의 목조 건물 마을 지점에서 일하는 \'후이바 후유\'라는 알바생은 처음에는 어딘가 무서워 보였는데, 래빗 하우스에서 하룻밤 묵으면서 같이 논 것을 계기로 친해졌어요!','저는 전학을 자주 다녀서, 너무 친해지면 헤어질 때 괴로우니까 무난한 캐릭터를 연기하고 있어요. 나츠메는 소심한 이미지고, 전 쿨한 이미지에요! 어땠나요? 헤헤.\n(뒤에서 듣고 있던 마야 : 전혀 안 어울려.)'])
            case 3:
                e_title = f'현재 호감도는 {friendly_rate}입니닷!'
                e_desc = '임시 메세지'
            case 4:
                e_title = f'현재 호감도는 {friendly_rate}입니당!'
                e_desc = '임시 메세지'
            case _:
                e_title = f'현재 에루의 호감도는 {friendly_rate}이에요!'
                e_desc = '임시 메세지'
        embed = discord.Embed(title=e_title,description=e_desc,color=0xfdeccf)
        embed.add_field(name='에루 짱과 처음 만난 날',value=getRegisterDate(ctx.author.id),inline=False)
        embed.add_field(name='에루 짱과 함께한 날',value=f'{getDayCount(ctx.author.id)}일',inline=True)
        embed.add_field(name='명령어 사용 횟수',value=f'{getCommandCount(ctx.author.id)}회',inline=True)
        embed.add_field(name='누적 패널티',value=getPenalty(ctx.author.id),inline=True)
        await ctx.respond(embed=embed)
    
    @commands.slash_command(name='회원가입',description='에루봇의 원활한 이용을 위한 데이터 생성과 회원가입을 할 수 있어요!',guild_ids=guild_ids)
    async def register_FrontEnd(self,ctx,text:discord.Option(str,'약관에 동의하시면 \'동의\'라고 입력해주세요!',required=False)):
        if text == '동의':
            a = register(ctx.author.id)
            if a == 1:
                embed = discord.Embed(title='회원가입이 완료되었습니다.',description='앞으로 부디 잘 부탁드리겠습니다.\n에루봇 가입 만으로 에루봇과 하늘봇의 데이터가 전부 생성되었습니다. 하늘봇의 개시는 며칠 후 예정되어 있으니 잠시만 기다려주시면 감사드리겠습니다.',color=0xfdeccf)
            elif a == -1:
                match friendlyRate(ctx.author.id):
                    case 1:
                        embed = discord.Embed(title='이미 데이터가 존재해요.',description='데이터는 중복으로 생성할 수 없어요.',color=0xfdeccf)
                    case 2:
                        embed = discord.Embed(title=f'{ctx.author}님은 이미 에루랑 친한 사이잖아요?',description='설마 잊어버리신 건가요?',color=0xfdeccf)
                    case 3 | 4:
                        embed = discord.Embed(title=f'{ctx.author}님은 이미 에루랑 많이 친한 사이잖아요?',description='제 곁에 오래 있어주셨으면서, 설마 잊어버리신 건가요?',color=0xfdeccf)
                    case _:
                        embed = discord.Embed(title='이미 데이터가 존재합니다.',description='데이터는 중복으로 생성할 수 없습니다.',color=0xfdeccf)
            else:
                embed = discord.Embed(title='회원가입 중 오류가 발생했습니다.',description='번거롭지만 하토를 불러주십시오.',color=0xfdeccf)
        else:
            embed = discord.Embed(title='어서 오세요. 회원증 좀 보여 주시겠어요?',description='회원가입은 아래의 약관에 동의하셔야 가능합니다. 약관에 동의하시면 \'/회원가입 동의\'라는 명령어를 입력해 주십시오.\nhttps://github.com/SorameHato/EluBot/blob/main/%EB%94%94%EC%BD%94%EB%B4%87%20%EC%95%BD%EA%B4%80.txt',color=0xfdeccf)
        await ctx.respond(embed=embed)
    
    @commands.slash_command(name='회원가입동의',description='(모바일용) 에루봇의 원활한 이용을 위한 데이터 생성과 회원가입을 할 수 있어요!',guild_ids=guild_ids)
    async def register_FrontEndMobile(self,ctx):
        await self.register_FrontEnd(ctx,'동의')

def setup(bot):
    bot.add_cog(FriendlyRateFrontend(bot))