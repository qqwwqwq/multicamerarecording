from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib.animation import FuncAnimation
import numpy as np
import csv
# matplotlib.use('Qt5Agg')
data=[]
head=0
filename='/mnt/storage/buildwin/csv_3d_m/3d_A1-(17-08-2022-18-14-53)__c1.csv'
st=filename[29:-4]
print(st)
with open(filename, newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        if head==0:
            head=1
            continue
        # for meter
        data_line = [float(i)*1000  for i in row]
        # for milimeter
        # data_line = [float(i) for i in row]
        if data_line == []:
            # data.append([0] * 128)
            continue
        data.append(data_line)
print(data)



SkeletonConnectionMap = [[1, 0],
                       [2, 1],
                       [3, 2],
                       [4, 2],
                       [5, 4],
                       [6, 5],
                       [7, 6],
                       [8, 7],
                       [11, 2],
                       [12, 11],
                       [13, 12],
                       [14, 13],
                       [15, 14],
                       [18, 0],
                       [19, 18],
                       [20, 19],
                       [22, 0],
                       [23, 22],
                       [24, 23],
                       [26, 3],
                      ]
# print(data)
# print(data2)
data = np.array(data,dtype=int)



frames_number = data.shape[0]

data = data.reshape([frames_number, 32,4])

# [frame,bady,joint,xyz]

# print(np.sum(data, axis=0))
# print(np.sum(data, axis=1))

# mean = np.mean(data, axis=2)
# mean = mean[:, :, np.newaxis, :]
# # print(mean)
# # print(mean.shape)
# data = data - mean
# val = np.mean(data, axis=2)
# print(val)








fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.view_init(-90,-90)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_xlim(-1500, 1500)
ax.set_ylim(-1000, 1000)
ax.set_zlim(-1000, 1000)
# print(type(ax))


print(len(SkeletonConnectionMap))


def update(index):
    ax.lines = []
    for joint_connection in SkeletonConnectionMap:
        endpoint_x = [data[index][joint_connection[0]][0],  data[index][joint_connection[1]][0]]
        endpoint_y = [data[index][joint_connection[0]][1],  data[index][joint_connection[1]][1]]
        endpoint_z = [data[index][joint_connection[0]][2],  data[index][joint_connection[1]][2]]

        ax.plot(endpoint_x,endpoint_y, endpoint_z, c='r')

    # ax.scatter(data[index, :, 0], data[index, :, 1], data[index, :, 2], c='b', marker='^')


print(data.shape[0])
ani = FuncAnimation(fig, update, frames=frames_number, interval=1000/15, repeat=False)
plt.show()
print("start recording")
ani.save("/home/hexin/桌面/demoskeleton/"+st+".gif",writer="pillow")
print("done")