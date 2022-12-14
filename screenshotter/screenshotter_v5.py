import cv2  # also requires numpy to be installed
import os
from datetime import datetime, timedelta
import csv
import codecs

"""
Script written by Nik Kirstein

Edit lines: 
    51: directory path of Morae videos. Usually asf files.  Unzipped from Morae .rdg files
    52: video file name. Exact video to take screenshots from
    53: directory path of exported csv files of Morae Manager markers.
    54: csv file name. Exact csv file to parse and get times to take screenshots at from markers and save as filenames.
    55: output_directory: the directory where a screenshot directory will be made once the script is run.  
                          Each video creates a new screenshot directory called hostname-recording#_screenshots_raw
    
General pipeline of script:
    1. Script opens the csv file and parses it for times and filenames.
    2. Script converts human times to milliseconds for use in script.
    3. Script handles filenames since some markers have the same name but screenshots must be saved as 
       different filenames. Naming convention is adding -2, -3, -4, etc to end of original filename.
    4. Script opens a video and goes through it frame by frame, looking at each time in milliseconds
       that a frame occurs at.
    5. The script estimates the time to take a screenshot within 300 milliseconds.
    Morae Manager allows users to create markers at any time despite this time not actually existing 
    within the video, so we must estimate when to take a screenshot.  This is usually not a problem since
    humans do not move fast enough for 300 milliseconds to usually make a difference when taking a picture of a screen.
    This estimation is tune-able, simply edit line: 260 for a different time range if really needed.
    6. If the script sees a time close enough to a marker, it will take a screenshot at that time and frame and save
    it in the same location as the directory specified for output_directory
    7. Script will output how long it took to run.  Printing out the milliseconds as it runs through the script,
    does NOT change how fast the script will run, the video is always read frame by frame regardless of print output.
"""


def pre_setup():
    """
    This function exists to specify paths and files for the script.
    video_file_path is the directory where video files exist.
    video_file_name is the specific video to load and take screenshots from.
    csv_file_path is the directory where exported csv files from Morae exist.
    csv_file_name is the specific csv file to load Morae marker data from to ingest.

    This function returns many things used in the script.
    video_read is an openCV video read object for use in main()
    no_extension_video_file_name is the name of the video read without a file extension, usually a computer name.
    video_file_path is the directory of where videos are read from.
    full_csv_file_path is both the path and directory of exported Morae CSV files.
    """
    video_file_path = ""
    video_file_name = ""
    csv_file_path = ""
    csv_file_name = ""
    output_directory = ""

    ####################################
    # Edit the above to run the script. Don't change code below this line. #
    ####################################

    full_csv_file_path = csv_file_path + csv_file_name

    no_extension_video_file_name = video_file_name.split('.')[0]
    video_full_name_and_path = video_file_path + video_file_name
    video_read = cv2.VideoCapture(video_full_name_and_path)

    try:
        if not os.path.exists((output_directory + "\\" + no_extension_video_file_name + '_screenshots_raw')):
            os.makedirs((output_directory + "\\" + no_extension_video_file_name + '_screenshots_raw'))
    except OSError:
        print("Error while Creating Directory")

    return video_read, no_extension_video_file_name, video_file_path, full_csv_file_path, output_directory


def human_time_to_milliseconds(input_time):
    """
    Takes an input string in the format "0:00:00.00", human readable time.
    Hours:Minutes:Seconds.Milliseconds
    It then converts to milliseconds and returns that.
    :return: milliseconds: a time in milliseconds formatted as 000000.0
    """
    milliseconds = (datetime.strptime(input_time + '000', '%H:%M:%S.%f')
                    - datetime.strptime('00', '%H')).total_seconds() * 1000
    # print(milliseconds)
    return milliseconds


def milliseconds_to_human_time(input_time):
    """
    Takes an input number of milliseconds: 54321.0
    It then converts to human time in the format: "0:00:00.00"
    :return: human_time: a time in human readable format. Hours, minutes, seconds, milliseconds
    """
    human_time = timedelta(milliseconds=input_time)
    return human_time


def convert_filename_times_to_milliseconds(input_tuple_list):
    """
    Takes a list of tuples in the format [(humantime, "filename")]
    It converts all the human times in these tuples to milliseconds for the entire list.
    :param input_tuple_list: a list of tuples [("0:01:23.15", "D (AHLTA - Allergies)")]
    :return: same tuple list but the human time strings are now millisecond numbers (ints)
    """
    millisecond_tuple_list = []
    for time_filename_tuple in input_tuple_list:
        millisecond_tuple_list.append((human_time_to_milliseconds(time_filename_tuple[0]), time_filename_tuple[1]))

    return millisecond_tuple_list


def ingest_morae_marker_data(csv_path_and_filename):
    """
    Takes a full path and filename of a csv file of Morae Markers.
    This csv file is exported from Morae Manager under the analyze option.
    It then ingests it and parses it and turns it into a list of tuples where each tuple is
    a human readable time string and a corresponding filename for that time.
    [("0:00:43.25", "D (MHS - Allergies)"), ("0:01:21.75", "L (MHS-Problems)")]
    :param csv_path_and_filename: full path and filename of a csv file of Morae Markers.
    :return: time_filename_tuple_list: a list of tuples described above.
    """
    time_filename_tuple_list = []
    csv_reader = csv.reader(codecs.open(csv_path_and_filename, 'r', 'utf-16'))
    print(csv_reader)
    for row in csv_reader:
        # print(row)
        split_row = row[0].split('\t')  # tab separated values
        # print(split_row)
        marker_time = split_row[0]
        marker_file_name = split_row[4]
        # print(marker_time, marker_file_name)
        time_filename_tuple_list.append((marker_time, marker_file_name))

    # Toss first tuple as this is the header row in the csv file, not actual data.
    time_filename_tuple_list.pop(0)

    return time_filename_tuple_list


def generate_multiple_filenames(input_tuple_list):
    """
    Probably the most annoying/complicated function in this script.
    This function traverses a list of tuples containing times and filenames.
    If it has never seen a filename, it adds it to a new tuple list.
    If it has seen a filename before, it adds it to the new tuple list with an added -(counter) depending
    on how many times it saw that filename before.  This is to save screenshots under new names with
    incrementing numbers.  D (MHS - Data Reconciliation)-2, D (MHS - Data Reconciliation)-3, etc.
    :param input_tuple_list: a list of tuples, first value being times (string or number),
                             second value being a filename.
    :return: new_input_tuple_list: the same tuple list as before but instead of repeated filenames, each
                                   filename has a new -2, -3, -4 depending how on many times the filename exists.
    """
    filename_tracker = []
    filename_count_tracker = {}
    new_input_tuple_list = []

    for i in range(len(input_tuple_list)):
        filename = input_tuple_list[i][1]
        marker_time = input_tuple_list[i][0]
        # print(filename)
        if i == 0:
            filename_tracker.append(filename)
            filename_count_tracker[filename] = 1
            new_input_tuple_list.append((marker_time, filename))
        else:
            if filename in filename_tracker:
                filename_count_tracker[filename] += 1
                new_name = input_tuple_list[i][1] + '-' + str(filename_count_tracker[filename])
                filename_tracker.append(new_name)
                new_input_tuple_list.append((marker_time, new_name))
            else:
                filename_tracker.append(filename)
                filename_count_tracker[filename] = 1
                new_input_tuple_list.append((marker_time, filename))
    return new_input_tuple_list


def add_png_to_filenames(input_list_tuple):
    """
    Takes a list of tuples containing times and filenames and
    simply appends .png to each filename so that openCV can understand the filename to save it.
    :param input_list_tuple: list of tuples:
                            [(21690.0, "D (MHS - Allergies)"), (39980.0, "L (MHS-Problems)")]
    :return: png_tuple_list, same tuple list but with .png appended.
            [(21690.0, "D (MHS - Allergies).png"), (39980.0, "L (MHS-Problems).png")]
    """
    png_tuple_list = []
    for time_tuple in input_list_tuple:
        png_tuple_list.append((time_tuple[0], time_tuple[1] + ".png"))
    return png_tuple_list


def convert_time_tuple_list_to_dict(input_tuple_list):
    """
    Converts a list of tuples into a dictionary where the
    first value in the tuple is the dictionary key
    and the second value in the tuple is the dictionary value.

    :param input_tuple_list: a list of tuples
    :return: output_dict: a python dictionary
    """
    output_dict = {}
    for time_tuple in input_tuple_list:
        output_dict[time_tuple[0]] = time_tuple[1]
    return output_dict


def clean_and_parse_morae_data(starting_tuple_list):
    """
    Takes a tuple list generated from the ingest_morae function.
    Converts human time to millisecond time, handles multiple filenames, and adds .png to all filenames.
    Finally, converts it to a dictionary for use in main()
    :param starting_tuple_list: list of tuples
                                [("0:00:43.25", "D (MHS - Allergies)"), ("0:01:21.75", "L (MHS-Problems)")]
    :return: ending_dictionary: a dictionary of time values mapped to filenames.
    """

    millisecondtime_marker_file_list = convert_filename_times_to_milliseconds(starting_tuple_list)
    # convert human time strings to int milliseconds
    multinames_millisecondtime_marker_file_list = generate_multiple_filenames(millisecondtime_marker_file_list)
    # Handle multiple filenames
    multinames_millisecondtime_marker_file_list_png = add_png_to_filenames(multinames_millisecondtime_marker_file_list)
    # add .png to all filenames
    millisecond_time_filename_dict = convert_time_tuple_list_to_dict(multinames_millisecondtime_marker_file_list_png)

    return millisecond_time_filename_dict


def main():
    """
    loads a video to read and the dictionary of times and screenshot filenames
    in order to go through that video and every time it finds a time where a screenshot should be taken
    it will take a screenshot and save it as the proper screenshot name.
    :return: None
    """
    start_time = datetime.now()
    print("Video Start")

    video_to_read, host_name, video_file_path_reference, csv_full_path_and_file, current_output_directory = pre_setup()
    humantime_marker_file_list = ingest_morae_marker_data(csv_full_path_and_file)
    # Morae has times in human time by default
    millisecond_final_filename_dict = clean_and_parse_morae_data(humantime_marker_file_list)
    # parse and process data using clean and parsing function
    print("Total number of screenshots to take: " + str(len(millisecond_final_filename_dict)))
    # len should match up with number of screenshots to take. This is the number of Morae Markers.
    print(millisecond_final_filename_dict)

    while video_to_read.isOpened():
        current_frame = video_to_read.read()
        # print(current_frame)
        current_mili = round(video_to_read.get(cv2.CAP_PROP_POS_MSEC), 0)
        print(current_mili)

        if current_frame[0] is False:
            print("End of Video, last frame false")
            break

        for key in millisecond_final_filename_dict.keys():
            if 300 > key - current_mili >= 0:
                screenshots_save_file_path = (current_output_directory +
                                              host_name + "_screenshots_raw\\")
                file_name = millisecond_final_filename_dict[key]
                full_name_and_path = screenshots_save_file_path + file_name
                print("Time Found: Saving Screenshot")
                print(full_name_and_path)
                # print("FILE: ", file_name)
                cv2.imwrite(full_name_and_path, current_frame[1], [cv2.IMWRITE_JPEG_QUALITY, 100])

    video_to_read.release()
    cv2.destroyAllWindows()

    print("Script ran in", (datetime.now() - start_time).seconds, "seconds")


main()
