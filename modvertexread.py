import sys
import struct

def find0x98(data, stripFound, fix, EOF):
    while True:
        if not stripFound:
            data = e.read(1)
            try:
                start = struct.unpack('>B',data)
                if start[0] == 152:
                    stripFound = True
                    continue
                else:
                    continue
            except struct.error as err:
                print("EOF")#trolled
                EOF = True
                return EOF
            #Have we found a new triangle strip?
        if stripFound:
            #Find how many vertices are in the strip
            data = e.read(fix)
            if fix == 2:
                try:
                    vertices = struct.unpack('>1H',data)
                except struct.error as err:
                    return False
            elif fix == 1:
                try:
                    vertices = struct.unpack('>B', data)
                except struct.error as err:
                    print("oops")
                    data = 69
                    break
            print(str(vertices[0]) + " vertices found in strip")
            return vertices
        if data == 69:
            return data
        
def checkInvalid(array, length):
    #Prevent any straggling data from being written
    if len(array) < length:
        array = []
        return array
    #Prevent any repeat reference from being written
    rang = length-1
    for x in range(rang):
        elemntA = array[x]
        elemntB = array[x+1]
        if elemntA == elemntB:
            array = []
            return array
        elif array[x] == array[rang]:
            array = []
            return array

def extract8bitface(data, length, faceData, vertexNum):
    #We will go through the "short" to find >00 if there is one, other
    #wise we will just use a zero
    #We might also get to the next strip with out enough data so we will
    #skip outputting the face
    while len(faceData) < 3:
        data = e.read(2)
        try:
            #Convert the data into chars
            array = struct.unpack('>2B',data)
            print(array)
        except struct.error as err:
            break #eof
        #Essentially we are looking for any hex > 00
        #Otherwise we just use 0
        #Check if we caught a new strip identifier
        if array[0] == 152:
            print("New Strip Found")
            array = ['e']
            return array
        elif array[1] == 152:
            faceData.append(array[0])
            print("New Strip Found in 2nd byte")
            array = []
            return array
        if array[0] > array[1]:
            faceData.append(array[0])
            print(face8bit)
            continue
        elif array[0] < array[1]:
            faceData.append(array[1])
            print(face8bit)
            continue
        else:
            #00 more like belongs in the trash
            continue
    return faceData

def read8face(face8bit, e):
    readVert = False
    print("Reading indicies in 8-bit mode")
    for x in range(int(vertices[0])):
        #Did we encounter a new strip?
        if readVert:
            break
        #8-BIT READ MODE
        #Read 2 bytes in the form of a "short" of face data
        face8bit = []
        data = e.read(2)
        try:
            #Convert the data into chars
            face = struct.unpack('>2B',data)
        except struct.error as err:
            break #eof       
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
            print("Either no data or ran out of data.")
            break #eof
        #HARDCODE: All 0.0 must go away
        if round(normal[0],4) + round(normal[1],4) + round(normal[2],4) == 0.0:
            continue
        index = str(round(normal[0],4)) + " " + str(round(normal[1],4)) + " " + str(round(normal[2],4))
        print(struct.unpack('>3f',data))
        obj.write("vn  " + str(index) + "\n")
        normalNum += 1
print("0x11 finished extracting.")
paddingDone = False
stripFound = False
#Because I am not sure what descriptor dictates whether faces are in 8-bit or
#16-bit, turn this variable to true if you are getting strange references
read8bit = True
face8bit = []
skip = 0
vertices = 0
EOF = False
with open('0x50.bin', 'br') as e:
    find0x98(e, stripFound, 2, EOF)
    #D A N G E R T I M E
    while e:
        if EOF:
            break
        #The .mod starts a triangle strip primitive with 0x98, the next 2 bytes
        #describe how many vertices are in the strip
        #There is some padding at the start so we have to skip reading that
        if read8bit == True:
            if normalNum == 0:
                length = 3
            else:
                length = 9
            face8bit = extract8bitface(e, length, face8bit, vertices)
            if not face8bit:
                break
            #Did we encounter a new strip?
            if len(face8bit) == 0:
                find0x98(e, True, 2, EOF)
                if data == 69:
                    break
                face8bit = []
                continue
            elif face8bit[0] == 'e':
                find0x98(e, True, 1, EOF)
                if data == 69:
                    break
                face8bit = []
                continue
            if data == 69:
                print("EOF found.")
                break
            checkInvalid(face8bit, length)
            #Did we break with an unfinished face?
            x = int(len(face8bit))
            if x < length:
                face8bit = []
            #We don't support textures yet so we only add vertices and normals to the face
            if normalNum > 0:
                index = str(face8bit[0]) + "//" + str(face8bit[1]) + " " + str(face8bit[3]) + "//" + str(face8bit[4]) + " " + str(face8bit[6]) + "//" + str(face8bit[7])
            else:
                if len(face8bit) == 0:
                    continue
                print("Length: " + str(len(face8bit)))
                index = str(face8bit[0]) + " " + str(face8bit[1]) + " " + str(face8bit[2])
            face8bit = []
            obj.write("f  " + str(index) + "\n")
            faceNum += 1
            stripFound = False
        else:
            for x in range(int(vertices[0]/3)):
                #16-BIT READ MODE
                #Read 18 bytes of face data
                data = e.read(18)
                print
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
