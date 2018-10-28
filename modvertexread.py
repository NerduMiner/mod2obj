import sys
import struct

#G R O U N D B R E A K I N G  T I M E
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
        #HARDCODE: Some models are mean and place in large positions so we
        #no them out of existance
        if round(vertex[0],4) == -100:
            continue
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
paddingDone = False
stripFound = False
repeats = []
repeatNum = 0
skip = 0
oldchk = ()
vertices = 0
with open('0x50.bin', 'br') as e:
    #D A N G E R T I M E
    while e:
        #The .mod starts a triangle strip primitive with 0x98, the next 2 bytes
        #describe how many vertices are in the strip
        #There is some padding at the start so we have to skip reading that
        if not stripFound:
            data = e.read(1)
            try:
                start = struct.unpack('>1B',data)
                if start[0] == 152:
                    stripFound = True
                    continue
                else:
                    continue
            except struct.error as err:
                print("EOF")#trolled
                break
        #Have we found a new triangle strip?
        if stripFound:
            #Find how many vertices are in the strip
            data = e.read(2)
            try:
                vertices = struct.unpack('>1H',data)
            except struct.error as err:
                print(vertices)
        print(str(vertices[0]) + " vertices found in strip")
        for x in range(int(vertices[0]/3)):
            #Read 18 bytes of face data
            data = e.read(18)
            try:
                #Convert the data into the vertex, normal and texture references
                face = struct.unpack('>9H',data)
            except struct.error as err:
                break #eof
            for x in range(0,9,2):
                if face[x] > vertexNum or face[x] > 10000:
                    print("Invalid face found")
                    continue
            for x in range(1,9,2):
                if face[x] > normalNum or face[x] > 10000:
                    print("Invalid face found")
                    continue
            #We don't support textures yet so we only add vertices and normals to the face
            index = str(face[0]) + "//" + str(face[1]) + " " + str(face[3]) + "//" + str(face[4]) + " " + str(face[6]) + "//" + str(face[7])
            print(face)
            obj.write("f  " + str(index) + "\n")
            faceNum += 1
        stripFound = False
print("0x50 finished extracting.")
print(str(vertexNum) + " vertices created.")
print(str(normalNum) + " normals created.")
print(str(faceNum) + " faces created.")
print(str(repeatNum) + " repeat faces found.")
