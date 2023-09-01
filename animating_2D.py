import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import imageio

anim = True


def update(num, plotArray, lines): # what if we make lines an array of line?
	j = 2
	print(num)
	for line in lines:
		if num==0:
			num = 1
		line.set_data(plotArray.iloc[:,j][:num], plotArray.iloc[:,j+1][:num])
		line.set_3d_properties(plotArray.iloc[:,j+2][:num])
		j = j + 5


# df = pd.read_csv("1677609655.6149752.csv",converters={"target": lambda x: x.strip("[]").replace("'","").split(", ")})
df = pd.read_csv("1679599744.9839976tre65.csv",converters={"target": lambda x: x.strip("[]").replace("'","").split(", ")})
df = pd.concat([df, df.pop("target").apply(pd.Series).add_prefix("target_")], axis=1)
df = df.loc[:, [x for x in df.columns if x.startswith(('target_', 'timestamp'))]]

# Convert timestamp into a delta timestamp
time_start = df['timestamp'][0]
df['timestamp'] = df['timestamp'].subtract(time_start)

i = 2
while (i<df.columns.size):
	df[df.columns[i]] = df[df.columns[i]].str.replace(r"[\[\]]", '').astype(float)
	df[df.columns[i]] = pd.to_numeric(df[df.columns[i]])
	i = i + 1

# The anim will only have a maximum of 3 points that are moving through time, which isn't ideal.
print(df.head)

# # Attaching 3D axis to the figure
fig = plt.figure()
ax = fig.add_subplot(projection="3d")

num_lines = 0 
meanArrX = []
stdDevArrX = []
meanArrY = []
stdDevArrY = []
meanArrZ = []
stdDevArrZ = []

# print()
lines = []

i = 2 # 0 is useless. 1-5 is first, with 1 and 5 being useless, 6-10 is second, 11-15 third
while ((i)<df.columns.size): # 2, 7, 12, 17 -> break.
	# 2 3 4. 6 7 8. 
	if not anim:
		ax.scatter(df[df.columns[i]], df[df.columns[i+1]], df[df.columns[i+2]]) # THIS LINE GIVES YOU A STATIC GRAPH INSTEAD.
	line, = ax.plot(df.iloc[:,i][0:1], df.iloc[:,i+1][0:1], df.iloc[:,i+2][0:1], '*') # REMOVE '*' IF YOU WANT LINES.
	meanArrX.append(df[df.columns[i]].mean())
	stdDevArrX.append(df[df.columns[i]].std())
	meanArrY.append(df[df.columns[i+1]].mean())
	stdDevArrY.append(df[df.columns[i+1]].std())
	meanArrZ.append(df[df.columns[i+2]].mean())
	stdDevArrZ.append(df[df.columns[i+2]].std())
	lines.append(line)
	# filename = f'{i}.png'
	# plt.savefig(filename)
	# plt.close()

	i = i + 5
	num_lines = num_lines + 1
# # Setting the axes properties. 
ax.set(xlim3d=(sum(meanArrX)/len(meanArrX)-3*max(stdDevArrX), sum(meanArrX)/len(meanArrX)+3*max(stdDevArrX)), xlabel='X')
ax.set(ylim3d=(sum(meanArrY)/len(meanArrY)-3*max(stdDevArrY), sum(meanArrY)/len(meanArrY)+3*max(stdDevArrY)), ylabel='Y')
ax.set(zlim3d=(sum(meanArrZ)/len(meanArrZ)-3*max(stdDevArrZ), sum(meanArrZ)/len(meanArrZ)+3*max(stdDevArrZ)), zlabel='Z')

N = len(df)

if anim:
	anim = animation.FuncAnimation(
		fig, update,  frames=N, fargs=(df, lines), interval=100, repeat=False)
	f = r"/Users/lohner/Documents/Walabot/imgs/animation.gif" 
	writergif = animation.PillowWriter(fps=30) 
	anim.save(f, writer=writergif)
	anim.save()

# df = pd.read_csv("1680119234.844575_tresh_20.csv")
# fig = plt.figure()
# ax = fig.add_subplot(projection="3d")
# df = df.explode('target')


# [[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0..]]]
	
# while ((i)<df.columns.size): # 2, 7, 12, 17 -> break.
# 	ax.scatter(df[df.columns[i]], df[df.columns[i+1]], df[df.columns[i+2]]) # THIS LINE GIVES YOU A STATIC GRAPH INSTEAD.


# df['target'] = [[[0,0,0],[0,0,0]],[[0,0,0],[0,0,0]]] # value = z axis. column aka inner = x axis, column# = y axis? That leaves 1 extra axis though.
# 246 arrays, each with 46 length, grouped into 6 subgroups. Is the # value the power then?
# So [[]]# gives us the x coordinate
# [#] gives us the y coordinate
# What does []# do??? Z coordinate?
# 6,46,246 are xpos3d,ypos3d,zpos3d. 
# Phi goes from -45 to 45, with a resolution of 2. 90/2+1 = 46 (y)
# In goes from -25 to 25 with a resolution of 10 (6) 50/10 = 5+1 = 6 (x)
# Z goes from ... 
# 5 to 20 with a resolution of .5 -> 15*2 = 30 = 1 = 31???? Where does 246 come from?
# Keep in mind the R angle might interact with the other 2 angles to give a greater Z distance??



