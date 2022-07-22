from argparse import ArgumentParser

import cv2

from helpers import colorize, convert_to_bgra_if_required
from pyk4a import PyK4APlayback


def info(playback: PyK4APlayback):
    print(f"Record length: {playback.length / 1000000: 0.2f} sec")


def play(playback: PyK4APlayback):
    while True:
        try:
            capture = playback.get_next_capture()
            if capture.color is not None:

                cv2.imshow("Color", convert_to_bgra_if_required(playback.configuration["color_format"], cv2.resize(capture.color, (1024, 763))))
            if capture.transformed_depth is not None:
                cv2.imshow("Depth", colorize(cv2.resize(capture.transformed_depth, (1024, 763)), (None, 5000)))
            key = cv2.waitKey(10)
            if key != -1:
                break
        except EOFError:
            break
    cv2.destroyAllWindows()


def main() -> None:


    filename: str = "/mnt/storage/buildwin/multicameradata/A5-(22-07-2022-20-26-06)__c1.MKV"


    offset: float = 0

    playback = PyK4APlayback(filename)
    playback.open()

    info(playback)

    if offset != 0.0:
        playback.seek(int(offset * 1000000))
    play(playback)

    playback.close()


if __name__ == "__main__":
    main()