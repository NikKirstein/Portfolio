import os

"""
Give it a directory and it will rename your image files with _Final attached.
"""


def pre_setup():
    """
    A directory path full of images.  Specified in this function and also returns it for later use.
    :return :screenshots_file_path: A directory with images inside of it.
    """
    screenshots_file_path = ""
    return screenshots_file_path


def traverse_and_crop(screenshots_directory_path):
    """
    Traverses the directory specified in pre_setup()
    Renames every file as the same filename but with _Final attached.
    THIS CHANGES THE NAME OF EXISTING FILES, IT DOES NOT CREATE NEW FILES.
    MAKE SURE YOU WANT YOUR FILES RENAMED.

    :return: None
    """
    current_screenshot_dir = os.listdir(screenshots_directory_path)
    for screenshot_file_name in current_screenshot_dir:
        print("Processed:", screenshot_file_name)
        stripped_extension = screenshot_file_name.split('.')[0]
        os.rename((screenshots_directory_path + screenshot_file_name),
                  (screenshots_directory_path + stripped_extension + "_Final.png"))

    return None


def main():
    """
    Executes two functions to read a directory and rename the image files in it.
    :return:
    """
    screenshot_directory_path = pre_setup()
    traverse_and_crop(screenshot_directory_path)


main()
