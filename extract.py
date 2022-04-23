from email.mime import base
import time
import os
import sys
import argparse
from datetime import datetime, timedelta
from glob import glob
import random
import numpy as np
import cv2


# Commandline example :
# Launch random extraction from pathIn to pathOut exept "TEST" "Repo_test" and "bug" anime name
# python ./extract.py --it 2 --pathIn "../../Videos/" --pathOut "./output/" --exept "TEST" "Repo_test" "Bug"
# Launch random extraction with customized start time and time between 2 frames
# python ./extract.py --it 20 --pathIn "../../Videos/" --pathOut "./output/" --startTimeParam 0 20 10 --timeBetweenFramesParam 2 10 60 --exept "TEST" "Repo_test" "Bug"


# Convert time from seconds to minutes and seconds


def convert_time(time_sec):
    return (int(time_sec/60), time_sec % 60)

    # start_time : time (in sec) to start record; duration_time : duration (in sec) to record; time_between_frame : time between 2 frames in sec


def extractImages(pathIn, pathOut, video_start_time_seconds, time_between_frame, duration_time=-1, custom_name=""):
    count = 0
    vidcap = cv2.VideoCapture(pathIn)

    # Extract duration
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_total_duration_secs = frame_count/fps

    print("**************************************")
    print("VIDEO PROPERTIES")
    print(f"->fps rate = {fps} [fps]")
    print(f"->Total frame number = {frame_count} [frames]")
    print(f"->Total duration  = {video_total_duration_secs} [seconds]")

    # Convert duration from sec to min:sec
    video_duration_minutes, video_duration_seconds = convert_time(
        video_total_duration_secs)
    print(
        f"->Total duration  = {video_duration_minutes} [minutes] and {video_duration_seconds} [seconds]")
    print("**************************************")
    print("\n\n")

    # Convert duration from sec to min:sec
    video_start_extraction_minutes, video_start_extraction_seconds = convert_time(
        video_start_time_seconds)

    video_end_time_seconds = video_start_time_seconds + duration_time

    print("**************************************")
    print("EXTRACTION PROPERTIES")
    print(
        f"Extract video from time = {video_start_extraction_minutes} [minutes] and {video_start_extraction_seconds} [seconds]")

    if((duration_time == -1) or (video_end_time_seconds >= video_total_duration_secs)):  # All video time
        duration_time = video_total_duration_secs - video_start_time_seconds
        print("Extract video to the end !")
        video_end_time_seconds = video_start_time_seconds + \
            duration_time  # Override end time => To set it to the end

    video_end_extraction_minutes, video_end_extraction_seconds = convert_time(
        video_end_time_seconds)
    print(
        f"Extract video to time = {video_end_extraction_minutes} [minutes] and {video_end_extraction_seconds} [seconds]")
    print(f"Time between 2 frames = {time_between_frame} [secs]")
    print(f"Custom name = {custom_name}")
    print("**************************************")

    count = video_start_time_seconds

    compression_params = [cv2.IMWRITE_PNG_COMPRESSION, 1]

    success = True
    while (success and count <= video_start_time_seconds + duration_time):
        vidcap.set(cv2.CAP_PROP_POS_MSEC, (count*1000))
        success, image = vidcap.read()

        if(success == False):
            break
        if(custom_name == ""):
            filename = pathOut + "/frame_" + \
                str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S__%f")[:-3]) + \
                str(count) + ".png"
        else:
            filename = pathOut + "/" + \
                custom_name.replace(
                    "/", "") + "__" + str(timedelta(seconds=count)).replace(":", "_") + ".png"  # remove /

        if(os.path.exists(filename)):

            # if (cv2.haveImageReader(filename)):
            print("Stop at file " + filename + " which already exist")
            break

        cv2.imwrite(filename,
                    image, compression_params)     # save frame as JPEG file

        count = count + time_between_frame
        print("\tProgress : " + str(count) + "/" +
              str(video_end_time_seconds), end='\r')
        # print(f"Progress : {count}/{video_end_time_seconds}")
    if(not success):
        print("Error to read video")

    vidcap.release()


def chooseRandomEp(base_path="/mnt/my_mount_dir/Anim/", exept=[]):
    anim_dir_list = glob(base_path+"*/")  # list all dir only
    # print("anim_dir_list : " + ' '.join(anim_dir_list))
    print(f"Anime name exeption : {exept}")
    # Remove anime
    str_to_remove = []
    for anime in anim_dir_list:
        for anime_exept in exept:
            if(not anime.lower().find(anime_exept.lower()) == -1):
                str_to_remove.append(anime)
                #print("FIND : " + (anime))
                break
    for str_ in str_to_remove:
        anim_dir_list.remove(str_)

    # print("AFTER REMOVE anim_dir_list : " + ' '.join(anim_dir_list))

    anime_dir_choose = random.choice(anim_dir_list)  # pick a random anim
    season_dir_list = glob(anime_dir_choose + "*/")
    while(season_dir_list is None or len(season_dir_list) == 0):
        print("REDO ! it was : " + anime_dir_choose)
        anime_dir_choose = random.choice(anim_dir_list)  # pick a random anim
        season_dir_list = glob(anime_dir_choose + "*/")

    season_dir_choose = random.choice(season_dir_list)
    ep_list = glob(season_dir_choose + "ep*.mp4")
    ep_choose = random.choice(ep_list)
    print("Ep choosen : " + ep_choose)
    anim_name = anime_dir_choose.split(base_path)[1]
    season = season_dir_choose.split(anime_dir_choose)[1]
    ep = ep_choose.split(season_dir_choose)[1]
    ep = ep.split(".mp4")[0]
    return [anim_name, season, ep, ep_choose]

# return empty if already exist


def createRepoVideoRecorded(repo, name_anim, season, ep):
    path_str = repo + name_anim + season + ep
    if(not os.path.exists(path_str)):
        print("Directory doesn't exist --> We create it")
        # Create multi dir
        os.makedirs(path_str)
    else:
        print("Directory already exist")
        return ""
    # Store path
    path_video = path_str
    print("Create video repo, stored path : " + path_video)
    return path_video


def extractDiaporama():
    a = argparse.ArgumentParser()
    a.add_argument("--it", help="number of iteration", type=int)
    a.add_argument("--pathOut", help="path to images", required=True, type=str)
    a.add_argument("--pathIn", help="path to your videos",
                   required=True, type=str)
    a.add_argument(
        "--exept", help="anime exception name => format tuple \"anime_example\"", nargs='+', type=str)

    a.add_argument("--startTimeParam",
                   help="Tuple : MIN_start_time_minutes MAX_start_time_minutes STEP_start_time_secs", nargs=3, type=int, default=(0, 20*60, 1))

    a.add_argument("--timeBetweenFramesParam",
                   help="Tuple : MIN_time_minutes MAX_time_minutes STEP_time_secs", nargs=3, type=int, default=(1*60, 10*60, 10))
    args = a.parse_args()

    for i in range(0, int(args.it)):
        [anim_name, season, ep, video_path] = chooseRandomEp(
            base_path=args.pathIn, exept=args.exept)
        start_time, end_time, step_time = args.startTimeParam
        start_time_between_frame, end_time_between_frame, step_time_between_frame = args.timeBetweenFramesParam
        extractImages(video_path, args.pathOut,
                      random.randrange(start_time*60, end_time*60, step_time), random.randrange(start_time_between_frame*60, end_time_between_frame*60, step_time_between_frame), -1, (anim_name + "_" + season + "_" + ep))


if __name__ == "__main__":

    extractDiaporama()
