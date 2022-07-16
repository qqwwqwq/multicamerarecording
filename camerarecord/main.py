import json
import random
import string

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
config2 = Config(color_resolution=ColorResolution.RES_720P,
                   depth_mode=pyk4a.DepthMode.WFOV_UNBINNED,
                   synchronized_images_only=True,
                   camera_fps=pyk4a.FPS.FPS_15,wired_sync_mode=WiredSyncMode.SUBORDINATE)
config = Config(color_resolution=ColorResolution.RES_720P,
                   depth_mode=pyk4a.DepthMode.WFOV_UNBINNED,
                   synchronized_images_only=True,
                   camera_fps=pyk4a.FPS.FPS_15,wired_sync_mode=WiredSyncMode.MASTER)

k4a = PyK4A(config,device_id=1)
#,device_id=274100312,000178500312
#
k4a2=PyK4A(config2,device_id=0)
k4a2.start()
k4a.start()
print(k4a2.serial)
print(k4a.serial)



# k4a.whitebalance = 4500
# assert k4a.whitebalance == 4500
# k4a.whitebalance = 4510
# assert k4a.whitebalance == 4510

# try:
print("Recording... Press CTRL-C to stop recording.")
while True:
    capture = k4a.get_capture()
    cv2.imshow("waiting",cv2.resize(capture.color, (640, 360)))
    if cv2.waitKey(1) & 0xff ==ord("r"):
        cv2.destroyAllWindows()
        print("start record")
        s=''.join(random.sample(string.ascii_letters + string.digits, 8))
        record = PyK4ARecord(device=k4a, config=config, path="/home/hexin/桌面/multicameradata/"+ s +"t.MKV")
        record.create()
        record2 = PyK4ARecord(device=k4a2, config=config2, path="/home/hexin/桌面/multicameradata/"+ s +"t2.MKV")
        record2.create()
        while True:
            capture2 = k4a2.get_capture()
            capture = k4a.get_capture()
            cv2.imshow("camera1", cv2.resize(capture.color, (640, 360)))
            cv2.moveWindow("camera1", 0, 0)
            cv2.imshow("camera2", cv2.resize(capture2.color, (640, 360)))
            cv2.moveWindow("camera2",0,600)
            cv2.imshow("Depth1", colorize(cv2.resize(capture.transformed_depth, (640, 360)), (None, 5000)))
            cv2.moveWindow("Depth1", 750, 0)
            cv2.imshow("Depth2", colorize(cv2.resize(capture2.transformed_depth, (640, 360)), (None, 5000)))
            cv2.moveWindow("Depth2", 750, 600)
        # print(capture.color)
        # imS = cv2.resize(capture.color, (1024, 763))
        # cv2.imshow('k4a', imS)
            record.write_capture(capture)
            record2.write_capture(capture2)
            if cv2.waitKey(1) & 0xff == ord("s"):
                print("end")
                cv2.destroyAllWindows()
                record.flush()
                record2.flush()
                record2.close()
                record.close()
                break


# except KeyboardInterrupt:
#     print("CTRL-C pressed. Exiting.")


