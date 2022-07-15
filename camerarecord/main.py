import json
import random
from pyk4a import Config, ImageFormat, PyK4A, PyK4ARecord
import pyk4a
from helpers import colorize, convert_to_bgra_if_required
from pyk4a import Config, PyK4A, ColorResolution, Calibration, CalibrationType,WiredSyncMode,PyK4APlayback
import numpy as np
np.set_printoptions(suppress=True)
import cv2

def bgr_rgb(img):
    (r, g, b) = cv2.split(img)
    return cv2.merge([b, g, r])
config2 = Config(color_resolution=ColorResolution.RES_1080P,
                   depth_mode=pyk4a.DepthMode.WFOV_UNBINNED,
                   synchronized_images_only=True,
                   camera_fps=pyk4a.FPS.FPS_15, wired_sync_mode=WiredSyncMode.SUBORDINATE)
config = Config(color_resolution=ColorResolution.RES_1080P,
                   depth_mode=pyk4a.DepthMode.WFOV_UNBINNED,
                   synchronized_images_only=True,
                   camera_fps=pyk4a.FPS.FPS_15, wired_sync_mode=WiredSyncMode.MASTER)

k4a = PyK4A(config,device_id=1)
k4a2=PyK4A(config2,device_id=0)
k4a2.start()
k4a.start()

# k4a.whitebalance = 4500
# assert k4a.whitebalance == 4500
# k4a.whitebalance = 4510
# assert k4a.whitebalance == 4510
record = PyK4ARecord(device=k4a, config=config, path="/home/tcy/Desktop/t.MKV")
record.create()
record2 = PyK4ARecord(device=k4a2, config=config2, path="/home/tcy/Desktop/t2.MKV")
record2.create()
try:
    print("Recording... Press CTRL-C to stop recording.")
    while True:
        capture = k4a.get_capture()
        capture2 = k4a2.get_capture()
        # print(capture2.color)
        # print(capture.color)
        # print(capture.color)
        imS2 = cv2.resize(capture2.color, (1024, 763))
        cv2.imshow('k4a', imS2)
        imS = cv2.resize(capture.color, (1024, 763))
        cv2.imshow('k4a', imS)
        record.write_capture(capture)
        record2.write_capture(capture2)

except KeyboardInterrupt:
    print("CTRL-C pressed. Exiting.")

record.flush()
record2.flush()
record2.close()
record.close()
