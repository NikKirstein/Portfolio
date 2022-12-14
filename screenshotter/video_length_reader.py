import os
import zipfile
from moviepy.editor import VideoFileClip
from datetime import timedelta


def pre_setup():
    """
    """
    video_file_path = ""
    f = []
    for (dirpath, dirnames, filenames) in os.walk(video_file_path):
        f.extend(filenames)
        break

    return video_file_path, f


def rename_to_zips(video_file_path, file_list):
    """

    :param video_file_path:
    :param file_list:
    :return:
    """

    for name in file_list:
        if ".rdg" in name:
            no_file_extension = name.split('.')[0]
            path_old_rdg = video_file_path + name
            new_zip = no_file_extension + '.zip'
            path_new_zip = video_file_path + new_zip
            # print(path_new_zip)
            os.rename(path_old_rdg, path_new_zip)

    return None


def unzip_zips(top_dir):
    for item in os.listdir(top_dir):
        if ".zip" in item:
            print(item)
            zip_ref = zipfile.ZipFile(top_dir + item)
            zip_ref.extractall(top_dir + item.split('.')[0])
            zip_ref.close()


def get_length(filename):
    result = VideoFileClip(filename)
    duration = result.duration
    result.close()
    return duration


def get_length_of_all_videos(top_dir):
    video_length_list_seconds = []
    for item in os.listdir(top_dir):
        # print(item)
        if ".zip" not in item:
            # print("in", item)
            for files in sorted(os.listdir(top_dir + item)):
                if ".asf" in files:
                    print(files)
                    video_length_list_seconds.append(get_length(top_dir + item + "\\" + files))
    return video_length_list_seconds


def main():

    dir_path, all_files = pre_setup()
    # rename_to_zips(dir_path, all_files)
    # unzip_zips(dir_path)
    all_video_seconds_list = get_length_of_all_videos(dir_path)
    total_video_seconds = sum(all_video_seconds_list)
    print("Total Hours, Minutes, Seconds of all Videos:", timedelta(seconds=total_video_seconds))


main()
