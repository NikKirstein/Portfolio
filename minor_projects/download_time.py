
# Author Nik Kirstein

def main():
    """
    A one shot function script.
    Takes a variety of user inputs pertaining to download speed.
    Normally download speed is in megabit but I prefer kilobyte, megabyte, and gigabyte.
    Also asks for speed of internet and the size of file.
    
    Doesn't return anything just runs and prints
    """

    kind_of_speed = input("What is your download speed in?\nkb, mb, or gb?\n").strip()
    how_fast = int(input("What is your download speed?\n"))
    size_of_file = input("Size of file? Insert speed followed by a space followed by the measurement indicator.\nExample: 30 gb or Example2: 127 mb\n")
    new_file_size = 0
    real_speed = 0
    
    num_size_of_file = float(size_of_file.split(" ")[0])
    indicator_size_of_file = size_of_file.split(" ")[1].strip()
    # print(indicator_size_of_file)
    
    if indicator_size_of_file == "gb":
        new_file_size = (num_size_of_file * 1024 * 1024)
    elif indicator_size_of_file == "mb":
        new_file_size = num_size_of_file * 1024
    else:
        new_file_size = num_size_of_file
        
    # print(kind_of_speed == "kb")
    if kind_of_speed == "gb":
        real_speed = how_fast * 1024 * 1024
    elif kind_of_speed == "mb":
        real_speed = how_fast * 1024

    '''
    print("real_speed:", real_speed)
    print("new_file_size", new_file_size)
    print("how_fast", how_fast)
    '''
    
    if kind_of_speed != "kb":
        time_secs = (new_file_size / real_speed)
        print("It will take: ", round(time_secs, 3), "seconds to download your file")
        print("That's", round((time_secs / 60), 4), "minutes")
        print("Which is", round((time_secs / 60 / 60), 4), "hours")
    else:
        time_secs = (new_file_size / how_fast)
        print("It will take: ", round(time_secs, 3), "seconds to download your file")
        print("That's", round((time_secs / 60), 4), "minutes")
        print("Which is", round((time_secs / 60 / 60), 4), "hours")
        
        
main()