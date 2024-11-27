import socket

from encryption import encrypt


class Client:
    def __init__(self):
        self.__server_ip = ""
        self.__server_port = ""
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self, server_ip, server_port):
        self.__server_ip = server_ip
        self.__server_port = server_port
        self.__client_socket.connect((self.__server_ip, self.__server_port))

    def send_message(self, message: str):
        message = encrypt(message + "\n")
        self.__client_socket.send(message.encode("UTF-8"))

        response = self.__client_socket.recv(1024).decode("UTF-8")
        # print(f"Received: {response}")
        return response

    def _send_admin_message(self, message: str):
        message = encrypt(message + "\n")
        self.__client_socket.send(message.encode("UTF-8"))

    def close_session(self):
        self.__client_socket.close()


def main():
    cl = Client()
    cl.connect_to_server("192.168.1.78", 12999)
    answer = cl.send_message("192.168.1.68:12673")
    print(answer)


def print_hello_all():
    print("Hello, niggs")


if __name__ == "__main__":
    main()
