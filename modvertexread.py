import sys
import struct

#Now we view the vertcies?
print("Viewing data") 
obj = open("funy.txt", "w")
#We open the .bin file(its believed that you used pidi's modextract tool
#to separate the file and used 0x10.bin)
fChk = open('0x10.bin', 'br')
with open('0x10.bin', 'br') as f:
    chk = struct.calcsize('>3f')
    print(chk)
    while f:
        data = f.read(12)
        try:
            vertex = struct.unpack('>3f',data)
        except struct.error as err:
            break #eof
        coord = str(str(vertex[0]) + " " + str(vertex[1]) + " " + str(vertex[2]))
        print(struct.unpack('>3f',data))
        obj.write("v  " + str(coord) + "\n")
print("0x10 finished extracting.")
eChk = open('0x11.bin', 'br')
with open('0x11.bin', 'br') as e:
    while e:
        data = e.read(12)
        try:
            face = struct.unpack('>3i',data)
        except struct.error as err:
            break #eof
        index = str(face[0]) + " " + str(face[1]) + " " + str(face[2])
        print(struct.unpack('>3f',data))
        obj.write("f  " + str(index) + "\n")
print("0x11 finished extracting.")
