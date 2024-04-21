import discord
import random
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

TOKEN = os.environ.get("TOKEN")
intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)

TEST = True

@client.event
async def on_ready():
    global conn, cur
    print(f'{client.user}로 로그인 성공!')
    if TEST:
        
        conn = sqlite3.connect('test.db')
        cur = conn.cursor()
        print("TEST 진행중...")
    else:
        conn = sqlite3.connect('bot_database.db')
        cur = conn.cursor()
    await client.wait_until_ready()

    while not client.is_closed():
        TIL_CHANNEL_ID = 1229379739253342238
        til_channel = client.get_channel(TIL_CHANNEL_ID)
        
        CODE_TEST_ID = 1229379606281191424
        code_test_channel = client.get_channel(CODE_TEST_ID)

        now = datetime.now()
        if now.hour == 0 and now.minute == 0:
            print('DAY CHECKING')
            await til_channel.send("[🌠 ⋆⭒˚｡⋆ Today I Learn 🎇 ]")
            
            cur.execute(f'select count(*) from problems where uploaded = 0')
            row_count = cur.fetchone()[0]
            await code_test_channel.send(f'저장소가 업로드할 수 있는 문제 수: {row_count}')

        await asyncio.sleep(60)  # 60초(1분)마다 반복

        if now.hour==22 and now.minute == 0:
            
            print("uploading time!!!")


@client.event
async def on_message(message):
    if TEST:
        if message.content.startswith('!선택'):

            # 메시지가 '!선택'으로 시작하는 경우에만 실행
            channel = message.channel
            guild = message.guild

            # db에서 member_data 읽어옴
            cur.execute('SELECT * FROM member_data')

            rows = cur.fetchall()
            # 선택이 아직 안된 멤버 불러오기
            not_chosen = [row for row in rows if row[2] == 0]
            
            # random하게 선택
            selected_member = random.choice(not_chosen)
            member_id, member_name, _ = selected_member

            await channel.send(f'선택된 멤버: {guild.get_member(member_id).mention}')


            SELECTED_CHANNEL_ID = 1231572594478678116
            selected_channel = client.get_channel(SELECTED_CHANNEL_ID)
            await selected_channel.purge()
            await selected_channel.send(member_id)

        if message.content.startswith('!저장소'):
            cur.execute(f'select count(*) from problems where uploaded = 0')
            row_count = cur.fetchone()[0]
            await message.channel.send(f'저장소가 업로드할 수 있는 문제 수: {row_count}')
        
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
        
        if message.channel.id == 1231551496554807298:
            channel = message.channel
            members = [member for member in channel.members if not member.bot]
            if message.author in members:
                message_content = message.content
                cur.execute(f'select * from problems where problem_link = "{message_content}"')
                rows = cur.fetchall()
                
                # if problem is not in database
                if len(rows) == 0:
                    is_problem = True
                    backjoon, programmers, codetree, swea = False, False, False, False
                    if "acmicpc" in message_content:
                        print('this is backjoon')
                        backjoon = True
                    elif "programmers" in message_content:
                        print('this is programmers')
                        programmers = True
                    elif "codetree" in message_content:
                        print('this is codetree')
                        codetree = True
                    elif "swexpertacademy" in message_content:
                        print('this is SWEA')
                        swea = True
                    else:
                        await channel.send("코딩테스트 문제만 올려주세요.")
                        is_problem = False
                    if is_problem:
                        cur.execute(f'insert into problems (problem_link, backjoon, programmers, codetree, swea) values (?,?,?,?,?)', (message_content, backjoon, programmers, codetree, swea))
                        conn.commit()
                        await channel.send(f"문제가 저장되었습니다.")
                else:
                    await channel.send("데이터베이스에 해당 문제가 존재합니다.\n다른 문제를 올려주세요.")

    else:
        # 다음 사람을 선택하는 경우
        if message.content.startswith('!선택'):
            # 메시지가 '!선택'으로 시작하는 경우에만 실행
            channel = message.channel
            guild = message.guild

            # db에서 member_data 읽어옴
            cur.execute('SELECT * FROM member_data')

            rows = cur.fetchall()
            # 선택이 아직 안된 멤버 불러오기
            not_chosen = [row for row in rows if row[2] == 0 and row[0] != message.author.id]
            
            # 더이상 뽑을 사람이 없다면
            if len(not_chosen) == 0:
                # DB의 chosen 초기화
                cur.execute('UPDATE member_data SET chosen = False')

                # 뽑을 사람 다시 선택
                cur.execute('SELECT * FROM member_data')
                rows = cur.fetchall()
                not_chosen = [row for row in rows if row[2] == 0 and row[0] != message.author.id]
            
            # random하게 선택
            selected_member = random.choice(not_chosen)
            member_id, member_name, _ = selected_member

            await channel.send(f'선택된 멤버: {guild.get_member(member_id).mention}, {member_name}')
            cur.execute('UPDATE member_data SET chosen = True where id = ?', (member_id, ))

            # db에 저장
            conn.commit()

            # 선택된 멤버에 사용자 저장
            SELECTED_CHANNEL_ID = 1231572594478678116
            selected_channel = client.get_channel(SELECTED_CHANNEL_ID)
            await selected_channel.purge()
            await selected_channel.send(member_id)

        # 오늘의 문제 풀이 현황을 알고싶은 경우
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
        
        # 저장소에 몇개가 남았는지 확인
        if message.content.startswith('!저장소'):
            cur.execute(f'select count(*) from problems where uploaded = 0')
            row_count = cur.fetchone()[0]
            await message.channel.send(f'저장소가 업로드할 수 있는 문제 수: {row_count}')
        
        # 저장소에 문제 업로드
        if message.channel.id == 1231551496554807298:
            channel = message.channel
            members = [member for member in channel.members if not member.bot]
            if message.author in members:
                message_content = message.content
                cur.execute(f'select * from problems where problem_link = "{message_content}"')
                rows = cur.fetchall()
                
                # if problem is not in database
                if len(rows) == 0:
                    is_problem = True
                    backjoon, programmers, codetree, swea = False, False, False, False
                    if "acmicpc" in message_content:
                        print('this is backjoon')
                        backjoon = True
                    elif "programmers" in message_content:
                        print('this is programmers')
                        programmers = True
                    elif "codetree" in message_content:
                        print('this is codetree')
                        codetree = True
                    elif "swexpertacademy" in message_content:
                        print('this is SWEA')
                        swea = True
                    else:
                        await channel.send("코딩테스트 문제만 올려주세요.")
                        is_problem = False
                    if is_problem:
                        cur.execute(f'insert into problems (problem_link, backjoon, programmers, codetree, swea) values (?,?,?,?,?)', (message_content, backjoon, programmers, codetree, swea))
                        conn.commit()
                        await channel.send(f"문제가 저장되었습니다.")
                else:
                    await channel.send("데이터베이스에 해당 문제가 존재합니다.\n다른 문제를 올려주세요.")
    
    # 도움말 보기
    if message.content.startswith('!도움') or message.content.startswith('!help') or message.content.startswith('!h'):
        channel = message.channel
        await channel.send(">>    !선택    << 으로 무작위 한명을 선택할 수 있습니다.\n8명이 모두 뽑히기 전까지는 중복되지 않습니다.\n\
                            >>  !풀이현황  << 으로 가장 최근에 게시된 스레드에 풀이를 올린 사람을 확인할 수 있습니다.\n풀이를 올리지 않았다면 멘션됩니다.\n\
                            >>   !저장소   <<로 저장소에 업로드 할 수 있는 문제가 몇개 남은지 알 수 있습니다.\
                            1일 1코테 올리는 방법:\n====================\n!선택\n[ x월 x일 x요일 ]\n##코딩테스트 링크##\n====================\n으로 올리면 깔끔하게 선택까지 됩니다!\
                            문제 풀이 올리는 방법: 1일 1코테에 스레드를 생성해 주시면 됩니다!\n스레드 이름은 [ x월 x일 x요일 ](복붙가능)으로 하면 좋습니다.(보기에)\n\
                            ※※문제풀이 이외에 잡담을 남기면 문제를 풀었다고 표기될 수 있습니다.※※")

    if message.content.startswith('!test'):
        channel = message.channel
        
        members = channel.members
        ids = [member.id for member in members]
        member_name = [member.nick if member.nick != None else member.global_name for member in members]
        await channel.send(f'{ids}')
        await channel.send(f'{member_name}')

client.run(TOKEN)
