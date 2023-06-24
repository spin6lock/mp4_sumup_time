# encoding:utf8
import config
import glob
from progressbar import ProgressBar
import cv2
import dbm


def found_media_on_dir():
    all_result = []
    for path in config.paths:
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

def main():
    media = found_media_on_dir()
    all_seconds = sumup(media)
    hours, remain_minutes, minutes = convert(all_seconds)
    print("视频时长：{}秒".format(all_seconds))
    print("或：{}分".format(minutes))
    print("或：{}时{}分".format(hours, remain_minutes))


if __name__ == "__main__":
    main()
