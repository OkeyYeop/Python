import paramiko ## SSH접속 관련 패키지
import time
from getpass import getpass
import datetime


TNOW = datetime.datetime.now().replace(microsecond=0)

username = 'ID'  ## 원격 접속 ID
password = 'password'  ## 원격 접속 PW

count = 0

DEVICE_LIST = open ('5F_Internet_Cisco.txt', encoding='UTF8') ## ip_list.txt에 ip목록 작성 필
for TTT in DEVICE_LIST:
    TTT = TTT.strip()              ## 개행문자 참여 무시 -> .strip()
    print ('\n #### Connecting to the device' + TTT + '####\n' )
    SESSION = paramiko.SSHClient()
    SESSION.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    SESSION.connect(TTT,port=22,
                    username=username,
                    password=password,
                    look_for_keys=False,
                    allow_agent=False)

    DEVICE_ACCESS = SESSION.invoke_shell()
    DEVICE_ACCESS.send(b'enable\n')
    DEVICE_ACCESS.send(b'rufghs0803\n')
    DEVICE_ACCESS.send(b'terminal len 0\n')
    DEVICE_ACCESS.send(b'show run\n')
    DEVICE_ACCESS.send(b'\n')
    DEVICE_ACCESS.send(b'\n')
    DEVICE_ACCESS.send(b'\n')
    DEVICE_ACCESS.send(b'show log\n')
    DEVICE_ACCESS.send(b'show proc cpu | i five\n')
    DEVICE_ACCESS.send(b'show ver | i uptime\n')
    time.sleep(5)
    output = DEVICE_ACCESS.recv(65000)
    print (output.decode('ascii'))
    #f = open("hostname.txt", 'r', encoding='UTF8')
    #call_name = (f.readline()).strip()    ## ().strip() 사용해서 개행문자 참여 무시

    count = count + 1
    file_variable = open('hostname.txt', 'r', encoding='UTF8')
    all_lines_variable = file_variable.readlines()
    #print(all_lines_variable[ count - 1])

    SAVE_FILE = open( (all_lines_variable[ count - 1]).strip() + '.txt' , 'a+', encoding='UTF8')   ## Config Backup 파일
    SAVE_FILE.write(output.decode('ascii'))
    SAVE_FILE.close

    SESSION.close

input(print('실행이 완료됐습니다. 아무키나 눌러주세요'))