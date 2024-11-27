import socket
from threading import Thread

from database import DataBase
from encryption import decrypt


class VerifyServer:
    RUN = True

    def __init__(self, ip: str):
        self.__ip = ip
        self.__port = 12999
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.bind((self.__ip, self.__port))
        self.__server_socket.listen(10)
        self.__db = DataBase()
        print(f"{self.__ip}:{self.__port}")

    @property
    def db(self):
        return self.__db

    def __check_key(self, key):
        return self.__db.exist_key(key)

    def __client_handler(self, client_socket):
        while VerifyServer.RUN:
            key = client_socket.recv(1024)
            if not key:
                break
            key = decrypt(key.decode("UTF-8"))
            if key == decrypt("1CA4F2330E1C5CD1C8AE2495F2016F265"):
                command = decrypt(client_socket.recv(1024).decode("UTF-8"))
                command = command.split()
                if command[0] == "ADD":
                    self.__db.add_key(command[1], command[2])
                    continue
            if self.__check_key(key):
                client_socket.send(b"1")    # Valid key
            else:
                client_socket.send(b"0")    # Invalid key

    def run(self):
        while VerifyServer.RUN:
            client_socket, addr = self.__server_socket.accept()

            client_handler = Thread(target=self.__client_handler, args=(client_socket, ))
            client_handler.start()
        self.__server_socket.close()

    def stop(self):
        self.db.dump_keys()
        VerifyServer.RUN = False


def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return None
    finally:
        s.close()


def test_verify_server1():
    my_ip = get_local_ip()
    server = VerifyServer(my_ip)
    server.run()


if __name__ == "__main__":
    test_verify_server1()
