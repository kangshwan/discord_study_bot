import discord
import random
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.environ.get("TOKEN")
intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)
TEST = False

@client.event
async def on_ready():
    print(f'{client.user}로 로그인 성공!')
    if TEST:
        print("TEST 진행중...")
    await client.wait_until_ready()
    CHANNEL_ID = 1229379739253342238
    channel = client.get_channel(CHANNEL_ID)
    while not client.is_closed():
        now = datetime.now()
        if now.hour == 0 and now.minute == 0:
            print('DAY CHECKING')
            await channel.send("[🌠 ⋆⭒˚｡⋆ Today I Learn 🎇 ]")
        await asyncio.sleep(60)  # 60초(1분)마다 반복


@client.event
async def on_message(message):
    if TEST:
        if message.content.startswith('!선택'):
            # 메시지가 '!선택'으로 시작하는 경우에만 실행
            channel = message.channel
            members = channel.members
            # channel_name = '문제선택자'
            channel_name = '테스트선택자'
            guild = message.guild
            choice_channel = discord.utils.get(guild.channels, name = channel_name)
            async for msg in choice_channel.history(limit=1):
                if msg.content == '.':
                    filtered_members = [member.id for member in members if not member.bot]
                else:
                    filtered_members = list(map(int, msg.content.split(', ')))
                    
            # 메시지가 온 채널을 얻음
            # 채널에 있는 모든 멤버를 얻음
            # filtered_members = [member for member in members if not member.bot]
            # "지켜보고있다"라는 아이디를 가진 멤버를 제외한 나머지 멤버들을 필터링
            if filtered_members:
                selected_member = random.choice(filtered_members)
                # 필터링된 멤버 중에서 무작위로 한 명을 선택
                await channel.send(f'선택된 멤버: {guild.get_member(selected_member).mention}')
                # filtered_members.remove(selected_member)
                # if filtered_members:
                #     await choice_channel.send((', ').join(map(str, filtered_members)))
                # else:
                #     await choice_channel.send('.')
            else:
                await channel.send("선택할 수 있는 멤버가 없습니다.")
        if message.content.startswith('!풀이현황'):
            # 메시지가 '!최근댓글'로 시작하는 경우에만 실행
            channel_name = '1일-1코테'  # 여기에 원하는 채널 이름을 넣어주세요
            guild = message.guild
            # 메시지가 온 서버(길드)를 얻어옴
            channel = discord.utils.get(guild.channels, name=channel_name)
            # 채널 이름으로 채널을 찾음
            thread = channel.threads[-1]
            if thread:
                solvers = set()
                async for msg in thread.history(limit=None):
                    # 채널의 최근 메시지를 가져옴
                    solvers.add(msg.author)
                if solvers:
                    solver_names = ", ".join([solver.nick if solver.nick != None else solver.global_name for solver in solvers])
                    await message.channel.send(f'오늘({datetime.today().strftime("%m.%d")})의 코테를 푼 사람: {solver_names}')
                members = channel.members
                ids = [member.id for member in members]
                unsolvers = set()
                for member in members:
                    if member not in solvers and not member.bot:
                        unsolvers.add(member)
                unsolver_names = ", ".join([unsolver.nick if unsolver.nick != None else unsolver.global_name for unsolver in unsolvers])
                await message.channel.send(f'오늘({datetime.today().strftime("%m.%d")})의 코테를 풀지 않은 사람: {unsolver_names}')
            
            else:
                await message.channel.send(f'채널 {channel_name}을(를) 찾을 수 없습니다.')
    else:
        if message.content.startswith('!선택'):
            # 메시지가 '!선택'으로 시작하는 경우에만 실행
            channel = message.channel
            members = channel.members
            channel_name = '문제선택자'
            # channel_name = '테스트선택자'
            guild = message.guild
            choice_channel = discord.utils.get(guild.channels, name = channel_name)
            async for msg in choice_channel.history(limit=1):
                if msg.content == '.':
                    filtered_members = [member.id for member in members if not member.bot]
                else:
                    filtered_members = list(map(int, msg.content.split(', ')))
                    
            # 메시지가 온 채널을 얻음
            # 채널에 있는 모든 멤버를 얻음
            # filtered_members = [member for member in members if not member.bot]
            # "지켜보고있다"라는 아이디를 가진 멤버를 제외한 나머지 멤버들을 필터링
            if filtered_members:
                selected_member = random.choice(filtered_members)
                # 필터링된 멤버 중에서 무작위로 한 명을 선택
                await channel.send(f'선택된 멤버: {guild.get_member(selected_member).mention}')
                filtered_members.remove(selected_member)
                if filtered_members:
                    await choice_channel.send((', ').join(map(str, filtered_members)))
                else:
                    await choice_channel.send('.')
            else:
                await channel.send("선택할 수 있는 멤버가 없습니다.")

        if message.content.startswith('!풀이현황'):
            # 메시지가 '!최근댓글'로 시작하는 경우에만 실행
            channel_name = '1일-1코테'  # 여기에 원하는 채널 이름을 넣어주세요
            guild = message.guild
            # 메시지가 온 서버(길드)를 얻어옴
            channel = discord.utils.get(guild.channels, name=channel_name)
            # 채널 이름으로 채널을 찾음
            thread = channel.threads[-1]
            if thread:
                solvers = set()
                async for msg in thread.history(limit=None):
                    # 채널의 최근 메시지를 가져옴
                    solvers.add(msg.author)
                if solvers:
                    solver_names = ", ".join([solver.nick if solver.nick != None else solver.global_name for solver in solvers])
                    await message.channel.send(f'오늘({datetime.today().strftime("%m.%d")})의 코테를 푼 사람: {solver_names}')
                members = channel.members
                ids = [member.id for member in members]
                unsolvers = set()
                for member in members:
                    if member not in solvers and not member.bot:
                        unsolvers.add(member)
                unsolver_names = ", ".join([unsolver.mention for unsolver in unsolvers])
                await message.channel.send(f'오늘({datetime.today().strftime("%m.%d")})의 코테를 풀지 않은 사람: {unsolver_names}')
            
            else:
                await message.channel.send(f'채널 {channel_name}을(를) 찾을 수 없습니다.')
    if message.content.startswith('!도움') or message.content.startswith('!help') or message.content.startswith('!h'):
        channel = message.channel
        await channel.send(">>  !선택  << 으로 무작위 한명을 선택할 수 있습니다.\n8명이 모두 뽑히기 전까지는 중복되지 않습니다.\n")
        await channel.send(">>  !풀이현황  << 으로 가장 최근에 게시된 스레드에 풀이를 올린 사람을 확인할 수 있습니다.\n풀이를 올리지 않았다면 멘션됩니다.\n")
        await channel.send("1일 1코테 올리는 방법:\n====================\n!선택\n[ x월 x일 x요일 ]\n##코딩테스트 링크##\n====================\n으로 올리면 깔끔하게 선택까지 됩니다!")
        await channel.send("문제 풀이 올리는 방법: 1일 1코테에 스레드를 생성해 주시면 됩니다!\n스레드 이름은 [ x월 x일 x요일 ](복붙가능)으로 하면 좋습니다.(보기에)\n※※문제풀이 이외에 잡담을 남기면 문제를 풀었다고 표기될 수 있습니다.※※")

    if message.content.startswith('!test'):
        channel = message.channel
        
        members = channel.members
        ids = [member.id for member in members]
        member_name = [member.nick if member.nick != None else member.global_name for member in members]
        await channel.send(f'{ids}')
        await channel.send(f'{member_name}')

client.run(TOKEN)
