import json
import sys
import cv2
import csv

import numpy as np

from pykinect_azure import k4abt_skeleton_t

sys.path.insert(1, '../')
import pykinect_azure as pykinect
from pykinect_azure.k4a._k4atypes import K4A_CALIBRATION_TYPE_DEPTH,K4A_CALIBRATION_TYPE_COLOR
import pandas as pd
#pdObj = pd.read_json('/home/hexin/桌面/mydata.json')
# Iterating through the json
import os
# pdObj.to_csv('/home/hexin/桌面/streaming.csv', index=False)
if __name__ == "__main__":
	path=r'/mnt/storage/buildwin/test'
	filenames=os.listdir(path)
	fname2=os.listdir(r'/mnt/storage/buildwin/newfive_csv_3d')
	for j in range(len(fname2)):
		fname2[j]=fname2[j][3:-7]
	print(fname2)
	filenames=sorted(filenames)
	print(filenames)
	for name in filenames:
		print(name[:-4],00000)
		if name[:-4] in fname2:
			continue
		video_filename = '/mnt/storage/buildwin/test/'+name
		print(video_filename)
		st = video_filename[31:-4]
		print(st)
		# Initialize the library, if the library is not found, add the library path as argument
		pykinect.initialize_libraries(track_body=True)
		# Start playback
		playback = pykinect.start_playback(video_filename)

		playback_config = playback.get_record_configuration()
		print(playback_config)

		playback_calibration = playback.get_calibration()
		# Start body tracker
		bodyTracker = pykinect.start_body_tracker(calibration=playback_calibration)

		header = []
		header_m = []
		header_2d = []
		datas = []
		datas_m = []
		datas_2d = []

		tag = 0
		cv2.namedWindow('Depth image with skeleton', cv2.WINDOW_NORMAL)
		center1 = []
		current1 = []



		def cenp(body_handle):
			if body_handle == []:
				return []
			for jointID, joint in enumerate(body_handle.skeleton.joints):
				if jointID == 1:
					return [joint.position.xyz.x, joint.position.xyz.y, joint.position.xyz.z]


		def dis(a, b):
			return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


		while playback.isOpened():
			# Get camera capture
			capture = playback.update()
			# Get body tracker frame
			body_frame = bodyTracker.update(capture=capture)
			num_bodies = body_frame.get_num_bodies()
			dataone = []
			dataone_m = []
			dataone_2d = []
			headone = []
			headone_m = []
			headone_2d = []
			dataone_B = []
			dataone_m_B = []
			dataone_2d_B = []
			headone_B = []
			headone_m_B = []
			headone_2d_B = []
			ref_x = 0
			ref_y = 0
			ref_z = 0
			ref_x_B = 0
			ref_y_B = 0
			ref_z_B = 0
			
			current1 = body_frame.get_body(0).handle()
				

			for body_id in range(num_bodies):
				skeleton_handle = k4abt_skeleton_t()
				# if num_bodies == 2:
					# print(center1, current1, current2)
				if body_id == 0:
					for jointID, joint in enumerate(current1.skeleton.joints):
						if jointID == 1:
							ref_x = joint.position.xyz.x
							ref_y = joint.position.xyz.y
							ref_z = joint.position.xyz.z
					for jointID, joint in enumerate(current1.skeleton.joints):
						# print([joint.position.xyz.x,joint.position.xyz.y,joint.position.xyz.z],jointID)
						joint_2d = playback_calibration.convert_3d_to_2d(joint.position, K4A_CALIBRATION_TYPE_DEPTH,
																		 K4A_CALIBRATION_TYPE_COLOR)
						# print(joint_2d.xy.x,joint_2d.xy.y)
						headone.append("x" + str(jointID))
						headone.append("y" + str(jointID))
						headone.append("z" + str(jointID))
						headone.append("p" + str(jointID))
						headone_m.append("x" + str(jointID))
						headone_m.append("y" + str(jointID))
						headone_m.append("z" + str(jointID))
						headone_m.append("p" + str(jointID))
						headone_2d.append("x" + str(jointID))
						headone_2d.append("y" + str(jointID))
						headone_2d.append("p" + str(jointID))
						dataone.append(joint.position.xyz.x)
						dataone.append(joint.position.xyz.y)
						dataone.append(joint.position.xyz.z)
						dataone.append(joint.confidence_level)
						dataone_m.append((joint.position.xyz.x) / 1000)
						dataone_m.append((joint.position.xyz.y) / 1000)
						dataone_m.append((joint.position.xyz.z) / 1000)
						dataone_m.append(joint.confidence_level)
						dataone_2d.append(joint_2d.xy.x)
						dataone_2d.append(joint_2d.xy.y)
						dataone_2d.append(joint.confidence_level)

			center1 = current1


			if tag == 0:
				header = headone
				header_m = headone_m
				header_2d = headone_2d
				tag = 1

			datas.append(dataone)
			datas_m.append(dataone_m)
			datas_2d.append(dataone_2d)

			# print(datas)
			# Get the colored depth
			ret, depth_color_image = capture.get_transformed_colored_depth_image()
			# Get the colored body segmentation
			ret, color = capture.get_color_image()
			ret, body_image_color = body_frame.get_segmentation_image()
			if not ret:
				continue
			# Combine both images
			# combined_image = cv2.addWeighted(depth_color_image, 0.6, body_image_color, 0.4, 0)
			# Draw the skeletons
			combined_image = body_frame.draw_bodies(color, dest_camera=K4A_CALIBRATION_TYPE_COLOR)
			c2 = body_frame.draw_bodies(depth_color_image, dest_camera=K4A_CALIBRATION_TYPE_COLOR)

			cv2.imshow("camera1", cv2.resize(combined_image, (640, 360)))
			cv2.moveWindow("camera1", 0, 0)
			cv2.imshow("camera2", cv2.resize(c2, (640, 360)))
			cv2.moveWindow("camera2", 0, 600)
			# Overlay body segmentation on depth image
			# cv2.imshow('Depth image with skeleton',c2)
			# Press q key to stop
			if cv2.waitKey(1) == ord('q'):
				break
		with open("/mnt/storage/buildwin/newfive_csv_3d/" + "3d_" + st + "_B1.csv", 'w', encoding='UTF8', newline='') as f:
			writer = csv.writer(f)

			# 写入头
			writer.writerow(header)

			# 写入数据
			writer.writerows(datas)

		with open("/mnt/storage/buildwin/newfive_csv_3d_m/" + "3d_" + st + "_B1.csv", 'w', encoding='UTF8', newline='') as f:
			writer = csv.writer(f)

			# 写入头
			writer.writerow(header_m)

			# 写入数据
			writer.writerows(datas_m)

		with open("/mnt/storage/buildwin/newfive_csv_2d/" + "2d_" + st + "_B1.csv", 'w', encoding='UTF8', newline='') as f:
			writer = csv.writer(f)

			# 写入头
			writer.writerow(header_2d)

			# 写入数据
			writer.writerows(datas_2d)
		playback.close()
