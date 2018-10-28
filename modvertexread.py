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
        #HARDCODE: Just in case we find a -0.0
        if round(vertex[0],4) == -0.0:
            continue
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
        #HARDCODE: All 0.0 must go away
        if round(normal[0],4) + round(normal[1],4) + round(normal[2],4) == 0.0:
            continue
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
oldchk = ()
with open('0x50.bin', 'br') as e:
    while e:
        data = e.read(6)
        try:
            face = struct.unpack('>6B',data)
        except struct.error as err:
            break #eof
        #HARDCODE: sometimes door.mod creates a 152 for face idk why
        if face[0] == 152:
            continue
        if face[2] == 152:
            continue
        #Check if the faces reference out of bound indexes
        for i in range(0,6,2):
            if face[i] > vertexNum:
                continue
        #Is the entire face 0?
        if face[0] + face[1] + face [2] + face [3] + face [4] + face [5]== 0:
            continue
        #Check if the faces referece out of bound normal indexes
        for i in range(1,6,2):
            if face[i] > normalNum:
                continue
        #Check for invalid faces
        #Is the first vertex referenced again?
        if face[0] == face[2]:
            print("invalid face found")
            continue
        if face[0] == face[4]:
            print("invalid face found")
            continue
        #Is the first vertex normal referenced again?
        if face[1] == face[3]:
            face = list(face)
            face[1] = 1
            face[3] = 2
            face[5] = 3
            face = tuple(face)
        #create our tuple we will use to check for repeats
        if first == True:
            oldface = face
            oldchk = oldface
        #Is previous face same as new one?
        if face == oldchk:
            repeats.append(face)
            oldface = face
            first = False
            print("Repeat face found.")
            repeatNum += 1
            continue
        else:
            oldface = face
        #Is our new face a part of the repeat list?
        if face in repeats:
            repeats.append(face)
            first = False
            oldface = face
            print("Repeat face found.")
            repeatNum += 1
            continue
        else:
            oldface = face
        index = str(face[0]) + "//" + str(face[1]) + " " + str(face[2]) + "//" + str(face[3]) + " " + str(face[4]) + "//" + str(face[5])
        print(struct.unpack('>6B',data))
        obj.write("f  " + str(index) + "\n")
        faceNum += 1
print("0x50 finished extracting.")
print(str(vertexNum) + " vertices created.")
print(str(normalNum) + " normals created.")
print(str(faceNum) + " faces created.")
print(str(repeatNum) + " repeat faces found.")
print(first)
print(repeats)
