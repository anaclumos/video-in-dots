import cv2
import sys
import os
import pathlib


class termcolor:
    OKGREEN = "\033[92m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"


for file in sys.argv[1:]:
    normalized_path = os.path.abspath(file)
    if not pathlib.Path(normalized_path).exists():
        print(termcolor.FAIL + "× " + termcolor.ENDC + normalized_path)
        continue
    basename = os.path.basename(normalized_path)
    dirname = os.path.dirname(normalized_path)
    cap = cv2.VideoCapture(normalized_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    video_frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print()
    print("----------")
    print(f"{termcolor.OKGREEN}✓{termcolor.ENDC} VID: {normalized_path}")
    print(f"{termcolor.OKGREEN}✓{termcolor.ENDC} FPS: {str(fps)}")
    print(f"{termcolor.OKGREEN}✓{termcolor.ENDC} ALL: {str(video_frame_count)} frames")
    print("----------")
    print()
