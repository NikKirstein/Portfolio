import cv2  # also requires numpy to be installed
import os


def pre_setup():
    """
    This function exists to specify the path of the screenshots directory to read,
    as well as the new directory where new screenshots will be saved with an added _cropped.
    It creates the new screenshots directory where all cropped images will be placed.

    returns screenshots_file_path: directory of screenshots to be read
    returns new_screenshots_folder_path: directory created for cropped screenshots to be saved.
    """
    screenshots_file_path = ""  # individual screenshots folder here

    new_screenshots_folder_name = '_'.join(screenshots_file_path.split('\\')[-2].split('_')[0:2]) + "_cropped"
    # print(new_screenshots_folder_name)
    new_screenshots_folder_path = screenshots_file_path.split('\\')[0] \
                                  + '\\'.join(screenshots_file_path.split('\\')[1:4]) \
                                  + '\\' + new_screenshots_folder_name + '\\'
    print(new_screenshots_folder_path)

    try:
        if not os.path.exists(new_screenshots_folder_path):
            os.makedirs(new_screenshots_folder_path)
    except OSError:
        print("Error while Creating Directory")

    return screenshots_file_path, new_screenshots_folder_path


def traverse_and_crop(screenshots_directory_path, new_screenshot_directory_path):
    """
    Traverses the screenshots_directory path and crops all screenshots inside and saves them
    to the new_screenshot_directory_path
    :param screenshots_directory_path: Screenshot directory to read images from
    :param new_screenshot_directory_path: New directory to save images.
    :return: None, saves images.
    """
    current_screenshot_dir = os.listdir(screenshots_directory_path)
    for screenshot_file_name in current_screenshot_dir:
        print(screenshot_file_name)
        screenshot_file = screenshots_directory_path + screenshot_file_name
        print(screenshot_file)
        img = cv2.imread(screenshot_file)
        cropped_img = img[0:1080, 0:1920]
        cv2.imwrite((new_screenshot_directory_path + screenshot_file_name), cropped_img)
    return None


def main():
    """
    Runs two functions. One to get the directory to read and save.
    Creates the directory to save.
    Traverses the directory and crops images inside of it and saves it to the new directory.
    :return: None
    """
    current_screenshots_directory, new_screenshots_directory_path = pre_setup()
    traverse_and_crop(current_screenshots_directory, new_screenshots_directory_path)


main()
