import socket
import sys
import json

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_name = sys.argv[1]
server_address = (server_name, 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
sock.listen(1)

# 6 users, 10 rooms total
v3,w,h = 3, 6, 10
mat_rot = [[[0.0 for i in range(v3)] for x in range(w)] for y in range(h)]

BUFFER = 128 
dataStr = ""

while True:
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'client connected:', client_address
        while True:
            data = connection.recv(BUFFER)
            dataStr += data
            
            print >>sys.stderr, 'received "%s"' % data
            if data:
                #connection.sendall(data)
                if len(data) < BUFFER:#this could be buggy, if the size happens to equal to buffer size
                    json_data = json.loads(dataStr)

                    aRoom = json_data["room"]
                    aPos = json_data["pos"]
                    aRotX = json_data["rot"][0]
                    aRotY = json_data["rot"][1]
                    aRotZ = json_data["rot"][2]

                    if aRoom >= 0 and aRoom < h and aPos >= 0 and aPos < w:
                        # Update value
                        mat_rot[aRoom][aPos][0] = aRotX
                        mat_rot[aRoom][aPos][1] = aRotY
                        mat_rot[aRoom][aPos][2] = aRotZ

                        info = str(mat_rot[aRoom])
                        connection.sendall(info)
                    else:
                        connection.sendall('Invalid data')
                    dataStr = ""
            else:
                break
    finally:
        connection.close()
