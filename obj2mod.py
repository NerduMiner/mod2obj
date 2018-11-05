#obj2mod time
import struct
import sys
from array import array
#Once we have edited or made a new obj, it's time to import
#This is as simple as creating new sections of a .mod file
#and using ModPacker to put everything together
faceNum = 0
vertexNum = 0
array = []
fooce = []
with open("funy.obj", "r") as obj:
    for line in obj:
        if ('v') in line:
            print(line)
            line = line[1:]
            array.append([float(x) for x in line.split()])
            print(array)
            vertexNum += 1
        if ('f') in line:
            print(line)
            line = line[1:]
            fooce.append([int(x) for x in line.split()])
            print(fooce)
            faceNum += 1
    print(str(vertexNum) + " vertices found.")
    print(str(faceNum) + " faces found.")
with open("out0x10.bin", "wb") as vert:
    #0x10 starts with an identifier for how many vertices there are
    vertDef = struct.pack('>I', vertexNum)
    vert.write(vertDef)
    #0x20 alignment is practiced so we have to add 20 bytes of padding
    for x in range(5):
        padding = 0
        vertDef = struct.pack('>I', padding)
        vert.write(vertDef)
    #Now we can actually put in our data
    for x in range(vertexNum):
        for y in range(3):
            vertex = array[x][y]
            vertDef = struct.pack('>f', float(vertex))
            vert.write(vertDef)
print("Vertex data added successfully")
# with open("out0x11.bin") as normal:
# with open("out0x50", "wb") as face:
    #P S E U D O C O D E
    #create header data
    #face.write(headerData)
    #for x in range(faceNum):
    #   We use 4 because the format is as follows:
    #   face, uv, vertex-color, normals
    #   for y in range(4):
    #       face = fooce[x][y]
    #       faceDef = struct.pack('>H', face)
    #       face.write(faceDef)
