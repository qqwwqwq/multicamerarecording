import numpy as np
import csv
import os
from scipy.signal import savgol_filter
# matplotlib.use('Qt5Agg')

def spike_noise_filter(initial_path,target_path,window_lenth,polyorder,joint_number):
    #window_lenth   larger value -> stronger smooth
    #polyorder      smaller value -> stronger smooth
    filenames=os.listdir(initial_path)
    for name in filenames:
        data = []
        head = 0
        filename = initial_path + "/" + name
        print(filename)
        headline = []
        znumber = 0
        with open(filename, newline='') as csvfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                if head == 0:
                    head = 1
                    headline = row
                    if headline == []:
                        headline = ['x0', 'y0', 'z0', 'p0', 'x1', 'y1', 'z1', 'p1', 'x2', 'y2', 'z2', 'p2', 'x3', 'y3',
                                    'z3', 'p3', 'x4', 'y4', 'z4', 'p4', 'x5', 'y5', 'z5', 'p5', 'x6', 'y6', 'z6', 'p6',
                                    'x7', 'y7', 'z7', 'p7', 'x8', 'y8', 'z8', 'p8', 'x9', 'y9', 'z9', 'p9', 'x10',
                                    'y10', 'z10', 'p10', 'x11', 'y11', 'z11', 'p11', 'x12', 'y12', 'z12', 'p12', 'x13',
                                    'y13', 'z13', 'p13', 'x14', 'y14', 'z14', 'p14', 'x15', 'y15', 'z15', 'p15', 'x16',
                                    'y16', 'z16', 'p16', 'x17', 'y17', 'z17', 'p17', 'x18', 'y18', 'z18', 'p18', 'x19',
                                    'y19', 'z19', 'p19', 'x20', 'y20', 'z20', 'p20', 'x21', 'y21', 'z21', 'p21', 'x22',
                                    'y22', 'z22', 'p22', 'x23', 'y23', 'z23', 'p23', 'x24', 'y24', 'z24', 'p24', 'x25',
                                    'y25', 'z25', 'p25', 'x26', 'y26', 'z26', 'p26', 'x27', 'y27', 'z27', 'p27', 'x28',
                                    'y28', 'z28', 'p28', 'x29', 'y29', 'z29', 'p29', 'x30', 'y30', 'z30', 'p30', 'x31',
                                    'y31', 'z31', 'p31']
                    continue
                data_line = [float(i) for i in row]
                if data_line == []:
                    data.append([0] * (joint_number*4))
                    znumber += 1
                    continue
                data.append(data_line)
        data = np.array(data, dtype=float)
        frames_number = data.shape[0]
        data = data.reshape([frames_number, joint_number, 4])
        for t in range(joint_number):
            for j in range(2):
                data[znumber:, t, j] = savgol_filter(data[znumber:, t, j], 4 * window_lenth + 1, polyorder=3 * polyorder, deriv=0)
        for i in range(data.shape[0]):
            data[i][:, :3] -= data[i][1][:3]
        with open(target_path + "/" + name, 'w', encoding='UTF8',
                  newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headline)
            for i in data:
                writer.writerow(i.flatten())
        print("done")

if __name__=="__main__":
    initial_path = r'/mnt/storage/buildwin/process_newfive_csv_3d_m'
    target_path = '/mnt/storage/buildwin/spike_test'
    spike_noise_filter(initial_path, target_path, 20, 9, 32)
