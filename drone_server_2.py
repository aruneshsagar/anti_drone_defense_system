import time

from droneEdit import GET
import socket

host = '192.168.137.48'
port = 5431


def GET(data_0):
	response = GET(data_1)
	print("Response is : ", response)


def dataTransfer(conn):
    # A big loop that sends/receives data until told not to.
    while True:
        with open('readme.txt') as f:
            contents = f.read()
            print(contents)
        # Receive the data
        time.sleep(1)
        conn.sendall(str.encode(contents,'utf-8'))
        print("Data has been sent!")
    conn.close()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")
    s.bind((host, port))
    print("Socket bind comlete.")
    s.listen(1)  # Allows one connection at a time.
    conn, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    while True:
        try:
            dataTransfer(conn)
        except:
            break
if __name__ == "__main__":
	main()
        

