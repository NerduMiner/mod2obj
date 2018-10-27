import sys
import struct

#Now we view the vertcies?
skip = 0
vertexNum = 0
normalNum = 0
faceNum = 0
print("Viewing data") 
obj = open("funy.txt", "w")
#We open the .bin file(its believed that you used pidi's modextract tool
#to separate the file and used 0x10.bin)
with open('0x10.bin', 'br') as f:
    while f:
        data = f.read(12)
        if skip < 2:
            print("Skipping padding...")
            skip += 1
            continue
        try:
            vertex = struct.unpack('>3f',data)
        except struct.error as err:
            break #eof
        #the following is for the more odd vertices I have found in navi.mod
        '''
        if vertex[0] > 10 or vertex[0] < -10:
            continue
        if vertex[1] > 10 or vertex[1] < -10:
            continue
        if vertex[2] > 10 or vertex[2] < -10:
            continue
        '''
        coord = str(str(round(vertex[0],4)) + " " + str(round(vertex[1],4)) + " " + str(round(vertex[2],4)))
        print(struct.unpack('>3f',data))
        obj.write("v  " + str(coord) + "\n")
        vertexNum += 1
print("0x10 finished extracting.")

skip = 0
with open('0x11.bin', 'br') as g:
    while g:
        data = g.read(12)
        if skip < 1:
            print("Skipping padding...")
            skip += 1
            continue
        try:
            normal = struct.unpack('>3f',data)
        except struct.error as err:
            break #eof
        index = str(round(normal[0],4)) + " " + str(round(normal[1],4)) + " " + str(round(normal[2],4))
        print(struct.unpack('>3f',data))
        obj.write("vn  " + str(index) + "\n")
        normalNum += 1
print("0x11 finished extracting.")
'''
with open('0x18.bin', 'br') as e:
    while e:
        data = e.read(32)
        try:
            face = struct.unpack('>8f',data)
        except struct.error as err:
            break #eof
        index = str(face[0]) + " " + str(face[1]) + " " + str(face[2]) + " " + str(face[3]) + " " + str(face[4]) + " " + str(face[5]) + " " + str(face[6]) + " " + str(face[7])
        print(struct.unpack('>8f',data))
        obj.write("f  " + str(index) + "\n")
print("0x18 finished extracting.")
'''
'''
with open('0x30.bin', 'br') as e:
    while e:
        data = e.read(16)
        try:
            face = struct.unpack('>4i',data)
        except struct.error as err:
            break #eof
        index = str(face[0]) + " " + str(face[1]) + " " + str(face[2]) + " " + str(face[3])
        print(struct.unpack('>4i',data))
        obj.write("f  " + str(index) + "\n")
print("0x30 finished extracting.")
'''
first = True
repeats = []
repeatNum = 0
#This value is found multiple times in door.mod
repeats.append([0,0,113,120])
with open('0x50.bin', 'br') as e:
    while e:
        data = e.read(4)
        try:
            face = struct.unpack('>4B',data)
        except struct.error as err:
            break #eof
        #Check if the faces reference out of bound indexes
        if face[0] > vertexNum:
            continue
        if face[1] > vertexNum:
            continue
        if face[2] > vertexNum:
            continue
        if face[3] > vertexNum:
            continue
        if face[0] + face[1] + face [2] + face[3] == 0:
            continue
        face = sorted(face)
        #Check for repeated faces
        #initialize the first oldface
        if first == True:
            oldface = face
        if face == oldface and not first:
            repeats.append(face)
            oldface = face
            first = False
            print("Repeat face found.")
            repeatNum += 1
            continue
        else:
            oldface = face
        if face in repeats and not first:
            repeats.append(face)
            first = False
            oldface = face
            print("Repeat face found.")
            repeatNum += 1
            continue
        else:
            oldface = face
        index = str(face[0]) + " " + str(face[1]) + " " + str(face[2]) + " " + str(face[3])
        print(struct.unpack('>4B',data))
        obj.write("f  " + str(index) + "\n")
        faceNum += 1
        first = False
#in the case that you are using 0x50 of door.mod
obj.write("f  0 0 113 120\n")
print("0x50 finished extracting.")
print(str(vertexNum) + " vertices created.")
print(str(normalNum) + " normals created.")
print(str(faceNum) + " faces created.")
print(str(repeatNum) + " repeat faces found.")
print(repeats)
