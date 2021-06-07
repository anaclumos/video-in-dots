import cv2
import os
import pathlib

video = "/Users/sunghyuncho/video.mp4"


class termcolor:
    FAIL = "\033[91m"
    OKGREEN = "\033[92m"
    ENDC = "\033[0m"


normalized_path = os.path.abspath(video)
if not pathlib.Path(normalized_path).exists():
    print(termcolor.FAIL + "× " + termcolor.ENDC + normalized_path)
    exit()
basename = os.path.basename(normalized_path)
dirname = os.path.dirname(normalized_path)
filename = basename.rsplit(".", 1)[0]

cap = cv2.VideoCapture(video)
try:
    os.makedirs(os.getcwd() + "/frames/" + filename)
    print(
        termcolor.OKGREEN
        + "✓ "
        + termcolor.ENDC
        + os.getcwd()
        + "/frames/"
        + termcolor.OKGREEN
        + f"{filename}"
        + termcolor.ENDC
    )
except FileExistsError as e:
    pass

count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if frame is None:
        break
    if ret == True:
        cv2.imshow(f"{filename}", frame)
        cv2.imwrite(f"{os.getcwd()}/frames/{filename}/f{count}.jpg", frame)
        print(
            termcolor.OKGREEN
            + "✓ "
            + termcolor.ENDC
            + os.getcwd()
            + "/frames/"
            + termcolor.OKGREEN
            + f"{filename}"
            + termcolor.ENDC
            + "/"
            + termcolor.OKGREEN
            + f"f{count}.jpg"
            + termcolor.ENDC
        )
        count += 1
        if cv2.waitKey(10) & 0xFF == ord("q"):
            break
fps = cap.get(cv2.CAP_PROP_FPS)
video_frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
cap.release()
cv2.destroyAllWindows()

print("\nValidating...\n")

number_of_saved_frames = len(
    [
        name
        for name in os.listdir(os.getcwd() + "/frames/" + filename)
        if os.path.isfile(os.path.join(os.getcwd() + "/frames/" + filename, name))
    ]
)

if video_frame_count == number_of_saved_frames:
    print(
        termcolor.OKGREEN
        + "✓ "
        + termcolor.ENDC
        + f"All "
        + termcolor.OKGREEN
        + str(number_of_saved_frames)
        + termcolor.ENDC
        + " frames saved to "
        + os.getcwd()
        + "/"
        + termcolor.OKGREEN
        + f"{filename}"
        + termcolor.ENDC
    )
else:
    print(
        termcolor.FAIL
        + "× "
        + termcolor.ENDC
        + f"The folder {filename} has {number_of_saved_frames} frames, but the video has {video_frame_count} frames."
    )

print(f"FPS: {termcolor.OKGREEN + str(fps) + termcolor.ENDC}")
