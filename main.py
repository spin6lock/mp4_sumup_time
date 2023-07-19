# encoding:utf8
import config
import glob
from progressbar import ProgressBar
import cv2
import dbm


def found_media_on_dir(path):
    all_result = []
    result = glob.glob(path + "*.MP4", recursive = True)
    all_result.extend(result)
    return all_result


def sumup(all_video):
    total = 0
    progress = ProgressBar()
    with dbm.open("filename_period", "c") as db:
        for video in progress(all_video):
            time = db.get(video, None)
            if time:
                total = total + int(time)
                continue
            data = cv2.VideoCapture(video)
            frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = data.get(cv2.CAP_PROP_FPS)
            if fps == 0:
                print(f"fps is zero:{video}")
                fps = 30
            duration = round(frames / fps)
            db[video] = str(duration)
            total = total + duration
    return total


def convert(seconds):
    minutes = seconds // 60
    remain_seconds = seconds % 60
    hours = minutes // 60
    remain_minutes = minutes % 60
    return hours, remain_minutes, minutes

def sumup_one_dir(path):
    media = found_media_on_dir(path)
    all_seconds = sumup(media)
    hours, remain_minutes, minutes = convert(all_seconds)
    print(f"{path} 视频时长：{all_seconds}秒")
    print(f"或：{minutes}分")
    print(f"或：{hours}时{remain_minutes}分")


def main():
    for path in config.paths:
        sumup_one_dir(path)


if __name__ == "__main__":
    main()
