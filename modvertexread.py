import sys
import struct

#Now we view the vertcies?
print("Viewing data") 
obj = open("funy.txt", "w")
#We open the .bin file(its believed that you used pidi's modextract tool
#to separate the file and used 0x10.bin)
fChk = open('0x10.bin', 'br')
with open('0x10.bin', 'br') as f:
    while f:
        try:
            data = f.read(12)
        except (RuntimeError, struct.error):
            print("EOF reached")
            break
        vertex = struct.unpack('>3f',data)
        coord = str(str(vertex[0]) + " " + str(vertex[1]) + " " + str(vertex[2]))
        print(struct.unpack('>3f',data))
        obj.write("v  " + str(coord) + "\n")
print("0x10 finished extracting.")
eChk = open('0x11.bin', 'br')
with open('0x11.bin', 'br') as e:
    while e:
        try:
            data = e.read(12)
        except (RuntimeError, struct.error):
            print("EOF reached")
            break
        face = struct.unpack('>3f',data)
        index = str(face[0]) + " " + str(face[1]) + " " + str(face[2])
        print(struct.unpack('>3f',data))
        obj.write("f  " + str(index) + "\n")
print("0x11 finished extracting.")
