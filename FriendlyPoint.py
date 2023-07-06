import sqlite3, csv
from datetime import datetime as dt
from decimal import getcontext, Decimal
getcontext().prec = 2
commandPoint = Decimal(0.15)
dayPoint = Decimal(2.85)
threeDayPenalty = Decimal(-3.00)
sevenDayPenaltyInitial = Decimal(-14.00)
sevenDayPenaltyPerDay = Decimal(-2.00)

'''
에루짱의 친밀도 정리
주문토끼 9권에 나온 대로 에루짱은 브라이트 버니 회장 딸이라는 특성상
잦은 전학으로 인해 대충 어쩌고
암튼간
뭐 사실 코코아의 언니 파워엔 바로 넘어가버리긴 했지만
뭐 쨌든

테이블 구조 : uid INTEGER, last_call TEXT, gunba BLOB, command_count INTEGER, day_count INTEGER, total_penalty REAL, friendly_point REAL
명령어 사용 한 번 : +0.15 (command_count 행)
매일 최초 명령어 사용(05:15를 기준으로 초기화) : 추가 +2.85 (day_count 행)
3일 이상 에루봇을 사용하지 않다가 사용 : 포인트 -3 감소 및 에루짱이 외로워하는 대사 출력
다만 군바나 학업 등으로 자주 디코에 접속하지 못 하는 상황에서는 대사만 출력하고 포인트는 깎지 않음
(gunba, 그치만 8일 이상 미접속은 군바라도 예외 없이 깎음)
일주일 이상 에루봇을 사용하지 않다가 사용 (8일차부터) : -14 (+ 이후 1일 당 -2 추가) + 에루짱이 삐진 듯 한 대사 출력
그러니까 8일 : -11, 9일 : -13, 10일 : -15, 11일 : -17 ...

main.py에서 슬래시커맨드를 사용하면 정보나 랭크 커맨드 같은 게 아닌 이상
무조건적으로 event를 발생시켜서 commandCallCalc 함수를 호출

getCommandCount(uid:int)
command_count를 얻은 후 int형으로 return

__addCommamdCount__(uid:int,count:int,sep=False)
command_count를 count만큼 올리고 단독 사용 여부(sep)가 True라면 __calcFriendlyPoint__ 호출
만약 내리고 싶으면 count에 음수 입력


getDayCount(uid:int)
day_count를 얻은 후 int형으로 return

__addDayCount__(uid:int,count:int,sep=False)
day_count를 count만큼 올리고 단독 사용 여부(sep)가 True라면 __calcFriendlyPoint__ 호출
만약 내리고 싶으면 count에 음수 입력


getPenalty(uid:int)
total_penalty를 얻은 후 decimal형으로 return

__addPenalty__(uid:int,count:decimal,sep=False)
total_penalty를 count만큼 올리고 단독 사용 여부(sep)가 True라면 __calcFriendlyPoint__ 호출
만약 내리고 싶으면 count에 음수 입력

__setPenalty__(uid:int,amount:decimal)
이 함수는 절대로 함수 안에서 쓰지 말 것! 데이터에 오류가 생겼을 때나 고정소수점 연산에 문제가 생겨서
부동소수점으로 저장되는 등의 상황에 내가 데이터를 수동으로 수정하기 위한 함수임
uid의 penalty를 amount로 ''설정''하고 __calcFriendlyPoint__ 호출


getLastCallDate(uid:int)
last_call을 얻은 후 datetime형으로 return

__updateLastCallDate__(uid:int, date:dt)
마지막으로 호출한 날짜를 얻은 후(getLastCallDate) 그게 오늘이라면 단순히 현재 시점을 datetime 형식으로 테이블에 기록
만약 아니라면 __addDayCount__(1)을 일단 호출한 후 last_call이
어제 또는 그저께 : 에루짱이 반가워하는 대사를 출력
3~7일 전 : 에루짱이 외로워하는 대사를 출력
    gunba == true : 아무 것도 하지 않음
    gunba == false : __addPenalty__(3)
8일 이상 전 : 에루짱이 삐진 듯한 대사를 출력
__addPenalty__(14+2*(며칠만에 접속했는지 일수-8))
그런 다음 __calcFriendlyPoint__ 호출


commandCallCalc(uid:int, date:dt)
무조건 명령어 카운트를 올림(__addCommandCount__(uid, 1))
그런 다음 __updateLastCallDate__(uid, date) 호출
그런 다음 __calcFriendlyPoint__(uid) -> 이걸 return

__calcFriendlyPoint__(uid:int)
friendly_point를 getCommandCount(uid)*commandPoint+getDayCount(uid)*dayPoint-getPenalty(uid)로 설정
friendly_point를 return

getFriendlyPoint(uid:int)
friendly_point를 얻은 후 Decimal형으로 return

정보 함수에는 다음과 같이 출력
에루 짱과의 친밀도 : FriendlyPoint.getFriendlyPoint(uid),inline=False

에루 짱과 함께한 날 : FriendlyPoint.getDayCount(uid),inline=False

명령어 사용 횟수 : FriendlyPoint.getCommandCount(uid),inline=True
누적 패널티 : FriendlyPoint.getPenalty(uid),inline=True
'''

def __connectDB__():
    '''
    DB에 연결한 다음 con과 cur을 return하는 함수
    이 함수를 쓸 때에는 conn, cur = __connectDB__() 처럼
    앞에 변수를 2개 줘서 써야 한다!
    '''
    sql_con = sqlite3.connect("..\친밀도.db")
    sql_cur = sql_con.cursor()
    return sql_con, sql_cur

def __logWrite__(uid,task:str,text:str):
    '''
    로그에 데이터를 기록하는 함수
    현재시간(dt형),uid,task,text 와 같은 형식의 csv로 저장된다.
    uid : 말 그대로 유저의 디스코드 아이디
    task : 작업명 또는 함수명 (변경, 커밋, 생성, 조회 등)
    text : 상세한 작업 내역 (친밀도 1024.50 (1130,300,0) → 1027.50 (1131,301,0) 변경 처럼 어떤 걸 어떻게 변경했는 지 등을 상세하게 기록)
    '''
    with open('log.csv','a',encoding='utf-8',newline='') as a:
        writer = csv.writer(a)
        writer.writerow([dt.now(),uid,task,text])

def __commit__(sql_con,closeCon=False):
    '''
    데이터를 커밋하고 로그에 커밋했다는 사실을 기록하는 함수
    덤으로 closeCon = True로 하면 연결도 끊어준다
    '''
    sql_con.commit()
    __logWrite__('-','커밋','커밋 완료')
    if closeCon:
        __closeCon__(sql_con)

def __closeCon__(sql_con)
    '''
    조회함수 같은 건 커밋을 할 필요가 없으니까
    closeCon을 단독으로 사용하기
    '''
    sql_con.close()
    __logWrite__('-','closeCon','DB 연결 종료')


def __createDB__(sql_con,sql_cur):
    '''
    이 함수는 수동으로만 사용되어야 하는 함수!
    에루봇을 처음 가동하기 전이나 DB 파일을 날려먹었을 때 등
    테이블이 전부 날라가거나 생성되지 않은 상황에서만 사용
    day_count가 기본값이 1인 이유는 register을 할 때 last_call이
    현재 시간으로 기록되기 때문에 따로 처리를 안 해주면 day_count가
    0부터 시작하기 때문! 첫째 날도 빼먹으면 안 되니까
    '''
    sql_cur.execute('''CREATE TABLE IF NOT EXISTS friendly_point (
    uid INTEGER UNIQUE PRIMARY KEY,
    last_call TEXT,
    gunba BLOB DEFAULT 0,
    command_count INTEGER DEFAULT 0,
    day_count INTEGER DEFAULT 1,
    total_penalty REAL DEFAULT 0,
    friendly_point REAL DEFAULT 0);''')
    __logWrite__('-','생성','테이블 생성 완료')
    __commit__(sql_con,True)

    