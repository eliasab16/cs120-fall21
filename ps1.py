#arr is array of (val, key) pairs
import math
import time
from random import seed, randint
import timeit
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axisartist import SubplotZero
import pandas as pd
import seaborn as sns
from IPython.display import display


class Axes():
    
    def __init__(self, xlim=(-5,5), ylim=(-5,5), figsize=(12,5)):
        self.xlim = xlim
        self.ylim = ylim
        self.figsize  = figsize
        self.points   = []
        self.segments = []
        self.vectors  = []
        self.lines    = []
        self.scale_arrows()
    def __arrow__(self, x, y, dx, dy, width, length):
        plt.arrow(
            x, y, dx, dy, 
            color       = 'k',
            clip_on     = False, 
            head_width  = self.head_width, 
            head_length = self.head_length
        ) 
        
    def __drawAxis__(self):
        """
        Draws the 2D cartesian axis
        """
        # A subplot with two additional axis, "xzero" and "yzero"
        # corresponding to the cartesian axis
        ax = SubplotZero(self.fig, 1, 1, 1)
        self.fig.add_subplot(ax)
        
        # make xzero axis (horizontal axis line through y=0) visible.
        for axis in ["xzero","yzero"]:
            ax.axis[axis].set_visible(True)
        # make the other axis (left, bottom, top, right) invisible
        for n in ["left", "right", "bottom", "top"]:
            ax.axis[n].set_visible(False)
            
        # Plot limits
        plt.xlim(self.xlim)
        plt.ylim(self.ylim)
        # Draw the arrows
        self.__arrow__(self.xlim[1], 0, 0.01, 0, 0.3, 0.2) # x-axis arrow
        self.__arrow__(0, self.ylim[1], 0, 0.01, 0.2, 0.3) # y-axis arrow
        
        
    def scale_arrows(self):
        """ Make the arrows look good regardless of the axis limits """
        xrange = self.xlim[1] - self.xlim[0]
        yrange = self.ylim[1] - self.ylim[0]
        
        self.head_width  = min(xrange/30, 0.25)
        self.head_length = min(yrange/30, 0.3)
        
        
    def draw(self, image=None):
        self.scale_arrows()
        self.fig = plt.figure(figsize=self.figsize)
        # First draw the axis
        self.__drawAxis__()
        # Plot each point
        for point in self.points:
            point.draw()
        # Save the image?
        if image:
            plt.savefig(image)
        plt.show()
        
    def addPoints(self, points):
        for p in points:
            self.addPoint(p)
            
    def addPoint(self, p):
        self.points.append(p)
class Point():
    
    def __init__(self, x, y, color='#4ca3dd', size=50, add_coordinates=True):
        self.x = x
        self.y = y
        self.color = color
        self.size  = size
        self.add_coordinates = add_coordinates
        self.y_offset = 0.2
        self.items = np.array([x,y])
        self.len = 2
        
    def __getitem__(self, index):
        return self.items[index]
    
    # def __str__(self):
    #     return "Point(%.2f,%.2f)" % (self.x, self.y)
    
    # def __repr__(self):
    #     return "Point(%.2f,%.2f)" % (self.x, self.y)
    
    def __len__(self):
        return self.len
    
    def draw(self):
        plt.scatter([self.x], [self.y], color=self.color, s=self.size)
        
        # Add the coordinates if asked by user
        # if self.add_coordinates:
        #     plt.text(
        #         self.x, self.y + self.y_offset,
        #         "(%.1f,%.1f)"%(self.x,self.y),
        #         horizontalalignment='center',
        #         verticalalignment='bottom',
        #         fontsize=12
        #     )


def merge(arr1, arr2):
    sortedArr = []

    i = 0
    j = 0
    while i < len(arr1) or j < len(arr2):
        if i >= len(arr1):
            sortedArr.append(arr2[j])
            j += 1
        elif j >= len(arr2):
            sortedArr.append(arr1[i])
            i += 1
        elif arr1[i][0] <= arr2[j][0]:
            sortedArr.append(arr1[i])
            i += 1
        else:
            sortedArr.append(arr2[j])
            j += 1

    return sortedArr

def mergeSort(arr):
    if len(arr) < 2:
        return arr

    midpt = int(math.ceil(len(arr)/2))

    half1 = mergeSort(arr[0:midpt])
    half2 = mergeSort(arr[midpt:])

    return merge(half1, half2)

def countSort(arr, univsize):
    universe = []
    for i in range(univsize):
        universe.append([])

    for elt in arr:
        universe[elt[0]].append(elt)

    sortedArr = []
    for lst in universe:
        for elt in lst:
            sortedArr.append(elt)

    return sortedArr

def convertBase(n, b, max):
    digits = []

    for i in range(max):
        if (n):
            digits.append(int(n % b))
            n //= b
        else:
            digits.append(0)

    return digits

conv_time = 0

def radixSort(arr, univsize, b):
    maxlen = math.ceil(math.log(univsize, b))

    # stop = timeit.default_timer()
    # conv_time = stop-start
    # print("convert: " + str(stop - start))

    for i in range(0, maxlen):
        for a in range(len(arr)):
            if (i == 0):
                newNum = convertBase(arr[a][0], b, maxlen)
                arr[a] = [newNum[0], [newNum, arr[a][0], arr[a][1]]]
            if (i > 0):
                arr[a][0] = arr[a][1][0][i]

        arr = countSort(arr, univsize)

    for i in range(len(arr)):
        arr[i] = [arr[i][1][1], arr[i][1][2]]

    return arr

seed(20)

def rand_list_gen(u,n):
    rand_list = []
    for i in range(0,n):
        rand_list.append([randint(1,u), "a"])

    return rand_list

coords = []
timef = 0
alg = ""


for u in range(1,20):
    random_list = []
    unum = pow(2,u)
    for n in range(1,20):
        nnum = pow(2,n)
        array = rand_list_gen(unum, nnum)


        start = timeit.default_timer()
        mergeSort(array)
        stop = timeit.default_timer()
        ms = stop - start
        
        timef = ms
        alg = "merge"

        start = timeit.default_timer()
        countSort(array, unum + 1)
        stop = timeit.default_timer()
        cs = stop - start
        
        if (cs < timef):
            timef = cs
            alg = "count"

        start = timeit.default_timer()
        radixSort(array, unum + 1, nnum)
        stop = timeit.default_timer()
        rs = stop - start
        # print("radix: " + str(rs))
        # print("prc: " + str(conv_time))
        # print("______________")
        if (rs < timef):
            timef = rs
            alg = "radix"

        coords.append([alg, nnum, unum])

        # print("merge: " + str(ms))
        # print("count: " + str(cs))
        # print("radix: " + str(rs))
        # print("_______")



d = {"n": [], "u": [], "alg": []}

colors = {"merge": '#ffa500', "count": '#0000ff', "radix": '#a0f0ff'}

# Create the cartesian axis
axes = Axes(xlim=(1,pow(2,23)), ylim=(1,pow(2,23)), figsize=(9,7))
# Create two points
for p in coords:
    # x = n, y = u
    d['n'].append(p[1])
    d['u'].append(p[2])
    d['alg'].append(p[0])

df = pd.DataFrame(data=d)

# display(df.to_string())

sns.scatterplot(x="n",
                y="u",
                hue="alg",
                data=df)

plt.savefig("Color_scatterplot_by_variable_with_hue_Seaborn_scatterplot.png", format='png',dpi=150)
plt.xscale("log", basex=2)
plt.yscale("log", basey=2)

plt.show()
    # axes.addPoints([Point(p[1], p[2], color=colors[p[0]])])
# p1 = Point(2,  5, color='#ffa500')
# p2 = Point(7, 17, color='#0000ff')
# axes.addPoints([p1])
# axes.addPoints([p2])
# axes.draw()