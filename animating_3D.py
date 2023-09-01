import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from ast import literal_eval
import ast
import time
import imageio

def flatMakerX(arr, dimX, dimY, dimZ):
    xArr = np.arange(0,dimX,1) #baseArr 0, dimX, 1 # [0, 1, 2, 3, 4,... ,maxX] [0,0,0,5][0,0,1,7][0,0,0,12]
    baseArr = np.arange(0,dimX,1)
    for x in range(int(arra.size/dimX)-1): # baseSize/dimX
        xArr = np.append(xArr,baseArr)
    return xArr

def flatMakerY(arr, dimX, dimY, dimZ):
    yArr = np.arange(0,dimY,1) #baseArr 0, dimY, 1
    yArr = np.repeat(yArr, dimX) # dimX
    baseArr = yArr
    for x in range(int(arra.size/(dimX*dimY))-1): # (baseSize/(dimX*dimY))-1
        yArr = np.append(yArr,baseArr)
    # 0,1,2,3,0
    # 0,0,0,0,1
    return yArr

def flatMakerZ(arr, dimX, dimY, dimZ):
    zArr = np.arange(0,dimZ,1) # zArr 0, dimZ, 1
    zArr = np.repeat(zArr, dimX*dimY) # dimX * dimY
    return zArr
    # arr[0,0,0,0]

def flatMakerI(arr):
    arra = np.array(eval(arr))
    # flattening the array would give us the intensity array
    arra = arra.flatten()
    return arra
#arr = np.random.rand(1, 5, 3, 4)
#arr = target_array
#arr


# manually remove " using search and replace. Add " to the ends only.
df = pd.read_csv("1682361999.346003_20_tresh_20phi_15thet_30_noise_openClose_wave)x2.csv") # GREAT
# df = pd.read_csv("1682362241.8210464_30_tresh_20phi_15thet_30.csv") # WORKS
# df = pd.read_csv("1682362499.9322648_40_tresh_20phi_15thet_30.csv") # EMPTY?
# df = pd.read_csv("1682362704.7286098_50_tresh_20phi_15thet_30.csv") #100% EMPTY T>T

anim = True
# df = pd.DataFrame()
# df['timestamp'] = [1,2,3,4,5]
# df['target'] = ["[[[0,1,2,5],[10,2,3,4],[1,20,3,4],[1,2,0,0]],[[0,10,2,3],[1,2,30,4],[1,2,3,40],[10,2,0,0]]]","[[[0,1,20,3],[1,2,30,4],[1,20,3,4],[10,2,0,0]],[[0,10,2,3],[10,2,3,4],[10,2,3,4],[1,20,0,0]]]","[[[0,1,2,3],[1,2,3,4],[1,2,3,4],[1,2,0,0]],[[0,1,2,3],[1,2,3,4],[1,2,3,4],[1,2,0,0]]]","[[[0,1,2,3],[1,2,3,4],[1,2,3,4],[1,2,0,0]],[[0,1,2,3],[1,2,3,4],[1,2,3,4],[1,2,0,0]]]","[[[0,1,2,3],[1,2,3,4],[1,2,3,4],[1,2,0,0]],[[0,1,2,3],[1,2,3,4],[1,2,3,4],[1,2,0,0]]]"]


# Extract the target column as a string
# target_str = df['target'].values[0]
timestamp_column = df['timestamp']
pd.to_numeric(timestamp_column)
time_start = timestamp_column[0]
timestamp_column = timestamp_column.subtract(time_start)
print(timestamp_column)
data_column = df['target']
# pd.to_numeric(data_column)


num_lines = 0 

# print()
lines = []
print("Beginning the lambda things. Will take a while.")
finalDf = pd.DataFrame()
ff = data_column.iloc[0] # TODO: Switch to 0

arra = np.array(eval(ff))
dimX = arra[0][0].size
dimY = arra[0].size/dimX
dimZ = (arra.size/dimY)/dimX


finalDf['xArr'] = data_column.apply(lambda x: flatMakerX(x, dimX, dimY, dimZ))
finalDf['yArr'] = data_column.apply(lambda x: flatMakerY(x, dimX, dimY, dimZ))
finalDf['zArr'] = data_column.apply(lambda x: flatMakerZ(x, dimX, dimY, dimZ))
finalDf['iArr'] = data_column.apply(lambda x: flatMakerI(x))
# eliminate frames where the data didn't get anything.
finalDf = finalDf[finalDf['iArr'].apply(lambda x: True if x.sum() > 0 else False)]
print("Finished the lambda things. rest should be fast. If it isn't it migh")
finalDf['iArr'] = finalDf['iArr']/5000
filenames = []

def update(num): # what if we make lines an array of line?
    frame = finalDf.iloc[num]
    # print(frame)
    x = frame['xArr']
    y = frame['yArr']
    z = frame['zArr']
    i = frame['iArr']
    scatter.set_offsets(np.c_[frame['xArr'], frame['yArr'], frame['zArr']])
    scatter._sizes = i
    o = 0
    # plt.draw()

    # create file name and append it to a list
    print(num)

    # f = r"/Users/lohner/Documents/Walabot/imgs/animation2.gif" 
    # writergif = animation.PillowWriter(fps=30) 
    # anim.save(f, writer=writergif)
    # anim.save()
    return scatter,
   



fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.set_xlim3d(0, 50)
ax.set_ylim3d(0, 50)
ax.set_zlim3d(0, 50)

lines = []
i = 0
ff = finalDf.iloc[0] # TODO: Switch to 0
x=ff['xArr']
y=ff['yArr']
z=ff['zArr']
i=ff['iArr']


N = range(finalDf['xArr'].size)
scatter = ax.scatter(x, y, z, s=i, animated=True)
anim = animation.FuncAnimation(fig, update,  frames=N, interval=300, blit=True)

print(filenames)

with imageio.get_writer('mygif.gif', mode='I') as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)

plt.show()
# plt.close('all')
