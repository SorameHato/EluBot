def josaBool(arg:str):
    # 받침이 없는 경우('에요' '는' '가' 등) True
    # 받침이 있는 경우('이에요' '은' '이' 등) False
    argEnd = arg[-1]
    if "가" <= argEnd <= "힣":
        if (ord(argEnd)-ord("가")) % 28 > 0:
            return False
        else:
            return True
    else:
        return arg + '(이)에요!'

def josa에요(arg:str):
    argEnd = arg[-1]
    if "가" <= argEnd <= "힣":
        if (ord(argEnd)-ord("가")) % 28 > 0:
            return arg + '이에요!'
        else:
            return arg + '에요!'
    else:
        return arg + '(이)에요!'

def josa은는(arg:str):
    argEnd = arg[-1]
    if "가" <= argEnd <= "힣":
        if (ord(argEnd)-ord("가")) % 28 > 0:
            return arg + '은'
        else:
            return arg + '는'
    else:
        return arg + '은(는)'

def josa이가(arg:str):
    argEnd = arg[-1]
    if "가" <= argEnd <= "힣":
        if (ord(argEnd)-ord("가")) % 28 > 0:
            return arg + '이'
        else:
            return arg + '가'
    else:
        return arg + '이(가)'

def josa을를(arg:str):
    argEnd = arg[-1]
    if "가" <= argEnd <= "힣":
        if (ord(argEnd)-ord("가")) % 28 > 0:
            return arg + '을'
        else:
            return arg + '를'
    else:
        return arg + '을(를)'

def josa와과(arg:str):
    argEnd = arg[-1]
    if "가" <= argEnd <= "힣":
        if (ord(argEnd)-ord("가")) % 28 > 0:
            return arg + '과'
        else:
            return arg + '와'
    else:
        return arg + '와(과)'

def josa랑(arg:str):
    argEnd = arg[-1]
    if "가" <= argEnd <= "힣":
        if (ord(argEnd)-ord("가")) % 28 > 0:
            return arg + '이랑'
        else:
            return arg + '랑'
    else:
        return arg + '(이)랑'

def josa아야(arg:str):
    argEnd = arg[-1]
    if "가" <= argEnd <= "힣":
        if (ord(argEnd)-ord("가")) % 28 > 0:
            return arg + '아'
        else:
            return arg + '야'
    else:
        return arg + '아(야)'

def josa로(arg:str):
    argEnd = arg[-1]
    if "가" <= argEnd <= "힣":
        if (ord(argEnd)-ord("가")) % 28 == 8:
            return arg + '로'
        elif (ord(argEnd)-ord("가")) % 28 > 0:
            return arg + '으로'
        else:
            return arg + '로'
    else:
        return arg + '(으)로'