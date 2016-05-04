
# Pigeon IRC Bot Engine By Thiamine(lsw8075@snu.ac.kr)
# 피죤 IRC 봇 엔진 By 이승우
# 소스 일부는 norang님의 치즈봇에서 가져왔음을 밝힙니다.

import socket, ssl, re

# 아래는 기본 설정값입니다. 봇에 따라 바꿔주시면 됩니다.

HOST = "irc.uriirc.org"     # IRC 서버 주소
PORT = 16664                # IRC 포트
ID = "Columbiade"           # 봇 ID
NICK = '피죤'               # 봇 닉네임
FIRSTCHAN = '#bot-world'     # 실행되었을때 들어갈 채널
INVITABLE = True            # 주인 외에도 초대 가능한지
MASTERID = "lsw8075"        # 주인 ID

# 아래는 사용자가 내용을 정의하는 함수들입니다.
# 만약 함수가 문자열을 반환한다면, 채널에 바로 출력합니다.

# 접속했을 때
def onconnect():
    return '구구~ 내가 왔다구~'
# 채널에 들어왔을 때 (접속이나 초대 제외)
def onjoin(channel):
    pass
# 채널에서 나갈 때 (종료 제외)
def onpart(channel):
    return '구구국.. 나 간다구국..'
# 접속을 종료할 때
def onquit():
    return '구~ 잘있으라구!'
# 초대되었을 때
def oninvited(channel, nick):
    return '구구~ 불러줘서 고맙다구~'
# 옵을 받았을 때
def onoped(channel, nick):
    return '구구~♡'
# 옵을 잃었을 때
def ondeoped(channel, nick):
    return '내 옵 내놔라구ㅠㅠ'
# 옵을 여럿이 줘서 받았는지 잃었는지 모를 때
def onnooped(channel, nick):
    return '구?'
# 일반적인 대화
def ondialog(channel, nick, text):
    if text.find('닭둘기') != -1:
        deop(channel, nick, '구국.. 닭둘기라 부르지 말라구!')
    elif text.startswith('#'):
        if(len(text) == 4):
            try:
                r = int(text[1], 16) * 17
                g = int(text[2], 16) * 17
                b = int(text[3], 16) * 17
                if not (r in range(256)) or not (g in range(256)) or not (b in range(256)):
                    raise
                return '({:d}, {:d}, {:d})'.format(r,g,b)
            except:
                deop(channel, nick, '이상한 값 넣지 말라구!')
        if(len(text) == 7):
            try:
                r = int(text[1:3], 16)
                g = int(text[3:5], 16)
                b = int(text[5:7], 16)
                if not (r in range(256)) or not (g in range(256)) or not (b in range(256)):
                    raise
                return '({:d}, {:d}, {:d})'.format(r,g,b)
            except:
                deop(channel, nick, '이상한 값 넣지 말라구!')

# 불렀을 때
def oncalled(channel, nick, text):
    if text == '옵줘':
        op(channel, nick, '옵 드렸으니 사랑해달라구~')
    elif text == '빨래하자':
        return '빨래는 피죤~'
    elif text == '밥 먹자':
        return '구구~! 마시쪙? 마시쪙!'


# 명령어
def oncommand(channel, nick, command, args):
    if command == '!color' and len(args) == 3:
        try:
            r = int(args[0])
            g = int(args[1])
            b = int(args[2])
            if not (r in range(256)) or not (g in range(256)) or not (b in range(256)):
                raise
            res = '#{:02x}{:02x}{:02x}'.format(r, g, b)
            return res
        except:
            deop(channel, nick, '이상한 값 넣지 말라구!')

# 여기부터 엔진 부분.

# 엔진에서 사용하는 전역 값

chanlist = [FIRSTCHAN] # 채널 리스트
ismaster = False # 현재 마스터인지 확인하는 전역 변수. nick이 인자로 있는 콜백 함수 안에서만 써 주세요
UTF8 = 'utf-8'

# 아래는 사용자 부분에서 호출할 수 있는 함수들입니다.
def send_msg(channel, txt):
    '''메시지 보내기'''

    irc.send(bytes('PRIVMSG ' + channel + ' :' + txt + '\n', UTF8))

def join(channel:str, txt = ''):
    '''채널에 들어가기'''

    irc.send(bytes("JOIN %s\r\n" %channel, UTF8))
    chanlist.append(channel)
    if txt == '':
        txt = onjoin(channel)
    if txt != None:
        send_msg(channel, txt)

def part(channel:str, txt = ''):
    '''채널에서 나오기'''
    
    if txt == '':
        txt = onpart(channel)
    if txt != None:
        send_msg(channel, txt)
    chanlist.remove(channel)
    irc.send(bytes("PART %s\r\n" %channel, UTF8))

def op(channel:str, nick:str, txt=None):
    '''옵 주기 (callback only)'''

    irc.send(bytes('MODE ' + channel + ' +o ' + nick + '\n', UTF8))
    if txt != None:
        send_msg(channel, txt)

def deop(channel:str, nick:str, txt=None):
    '''옵 뺏기 (callback only)'''

    irc.send(bytes('MODE ' + channel + ' -o ' + nick + '\n', UTF8))
    if txt != None:
        send_msg(channel, txt)

def quit(txt = onquit()):
    '''연결 종료하기'''

    for chan in chanlist:
        if txt != None:
            send_msg(chan, txt)
    irc.send(bytes("QUIT\r\n", UTF8))
    print("Quit")

# 메시지 파싱 클래스
class Message:
    ID = ''           # 메시지를 보낸 사람의 ID
    nick = ''         # 메시지를 보낸 사람의 닉네임
    channel = ''      # 메시지를 보낸 채널
    msg = ''          # 메시지 내용
    msgType = ''      # 메시지 종류
    target = ''       # 메시지 목적어

    def __init__(self, origMsg):
        # TODO : 정규 표현식 배운 후 파싱 제대로 이해해 보기.
        parse = re.search('^(?:[:](\S+)!~?(\S+) )?(\S+)(?: (?!:)(.+?))?(?: [:](.+))?$', origMsg)
        if parse:
            self.msgType = parse.group(3)
            if self.msgType == 'PING':      # 핑
                self.ID = parse.group(5)
            elif self.msgType == 'JOIN':    # 입장
                self.ID = parse.group(2)
                self.channel = parse.group(5)
            elif self.msgType == 'MODE':    # MODE 변경. 옵/디옵 포함
                self.nick = parse.group(1)
                self.ID = parse.group(2)
                self.channel = parse.group(4).split(' ', maxsplit = 1)[0]
                self.msg = parse.group(4).split(' ', maxsplit = 1)[1]
            elif self.msgType == 'INVITE':  # 초대
                self.nick = parse.group(1)
                self.ID = parse.group(2)
                self.target = parse.group(4)
                self.channel = parse.group(5)
            elif self.msgType == 'PRIVMSG': # 대화
                self.nick = parse.group(1)
                self.ID = parse.group(2)
                self.channel = parse.group(4)
                self.msg = parse.group(5)
            else:
                pass

    def __repr__(self):
        return ('Message<type: %s chan: %s ID: %s nick: %s target: %s>'
                    %(self.msgType, self.channel, self.ID, self.nick, self.target))

    def __str__(self):
        return ('Message<type: %s chan: %s ID: %s nick: %s target: %s>'
                    %(self.msgType, self.channel, self.ID, self.nick, self.target))

# 엔진의 메인 처리기
def run():
    while True:

        # RAW 메시지 받아오기
        try:
            ircmsg_raw = irc.recv(8192).decode(UTF8)
        except KeyboardInterrupt:
            quit()
            return
        except UnicodeDecodeError as err:
            print("Unicode Error: {}".format(str(err)))
            continue
           
        ircmsg_raw = ircmsg_raw.strip("\n\r")

        if ircmsg_raw.find("PING :") != -1:
            irc.send(bytes("PONG :pingpong\n", UTF8))
            print("Pingpong")
            continue
        if ircmsg_raw[0] != ':':
            continue

        # 가공 후 각 메시지별로 처리
        msg = Message(ircmsg_raw)
        
        ismaster = (msg.ID == MASTERID)

        if msg.msgType == "INVITE": # 초대
            if INVITABLE or msg.ID == MASTERID:
                join(msg.channel, oninvited(msg.channel, msg.nick))

        elif msg.msgType == "MODE": # 옵 관련 처리
            if msg.msg == "+o " + NICK:
                txt = onoped(msg.channel, msg.nick)
                if txt != None:
                    send_msg(msg.channel, txt)
            elif msg.msg == "-o " + NICK:
                txt = ondeoped(msg.channel, msg.nick)
                if txt != None:
                    send_msg(msg.channel, txt)
            elif msg.msg.find(NICK) != -1:
                txt = onnooped(msg.channel, msg.nick)
                if txt != None:
                    send_msg(msg.channel, txt)

        elif msg.msgType == "PRIVMSG":
            if str(msg.msg)[0] == '!': # 명령어 처리
                arg = str(msg.msg).split(' ')
                txt = oncommand(msg.channel, msg.nick, arg[0], arg[1:])
                if txt != None:
                    send_msg(msg.channel, txt)
            elif str(msg.msg).startswith(NICK + ', '):
                txt = oncalled(msg.channel, msg.nick, str(msg.msg)[len(NICK + ', '):])
                if txt != None:
                    send_msg(msg.channel, txt)
            else: # 일반 대화 처리
                txt = ondialog(msg.channel, msg.nick, msg.msg)
                if txt != None:
                    send_msg(msg.channel, txt)

# 프로그램 초기화 부분

if __name__ == "__main__":
    irc_raw = socket.socket()
    irc_raw.connect((HOST, PORT))
    irc = ssl.wrap_socket(irc_raw)
    irc.send(bytes("NICK " + NICK + "\r\n", UTF8))
    irc.send(bytes("USER %s %s %s : %s\r\n" %(ID, ID, HOST, ID), UTF8))
    print("연결되었습니다.")
    join(FIRSTCHAN, onconnect())
    run()