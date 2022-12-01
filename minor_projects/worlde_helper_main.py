
# Author Nik Kirstein

def read_answers():
    """
    Reads the answers.txt file into python.
    Just as a list of unparsed answers since the file itself has dates in it, and days as an answer.
    The list itself is no longer accurate as to which day is which answer, but I never used that anyway.
    Just as a list of all possible word solutions
    Returns the file of lines unparsed.
    """
    answers_unparsed = []
    with open("answers.txt", "r") as file_open:
        for line in file_open:
            answers_unparsed.append(line)
    return answers_unparsed


def parse_answsers(unparsed_answers_lines):
    """
    Takes the raw list of answers with dates and days, and 
    just appends just the word solutions to a new list.
    Returns the new list of wordle solutions.
    """
    answer_list = []
    for line_item in unparsed_answers_lines:
        line_item = line_item.split(' ')[5].strip()
        answer_list.append(line_item)
    return answer_list


def handle_letter_position(user_input, answer_list_parsed):
    """
    :param user_input: a list of guesses in the format of "letter position", can be a singular guess.
    :param answer_list_parsed: just a list of answers to parse through
    :return: a list of possible answers that only contains answers where the user input is taken into account
    """
    new_parsed = []
    for letter_position_guess in user_input:
        # print(letter_position_guess)
        if '-' in letter_position_guess or "+" in letter_position_guess:
            pass
        elif "_" in letter_position_guess:
            split_list = letter_position_guess.split('_')
            letter = split_list[0].upper()
            position = int(split_list[1]) - 1
            for answer in answer_list_parsed:
                answer_list_rep = list(answer)
                # print(answer_list_rep)
                if not answer_list_rep[position] == letter:
                    # print("Found", answer)
                    new_parsed.append(answer)
        else:
            split_list = letter_position_guess.split(' ')
            # print(split_list)
            letter = split_list[0].upper()
            position = int(split_list[1]) - 1
            for answer in answer_list_parsed:
                answer_list_rep = list(answer)
                # print(answer_list_rep)
                if answer_list_rep[position] == letter:
                    # print("Found", answer)
                    new_parsed.append(answer)
    return new_parsed


def handle_removing_letters(user_input, answer_list_parsed):
    """
    If a letter isn't a letter in the solution, this is how we handle parsing the list of solutions
    and removing all solutions that contain that letter.
    Returns a new list of solutions with those that fit this condition removed.
    """
    new_parsed = []
    for guess in user_input:
        # print(guess)
        # print(guess.split(' '[0]))
        if guess.split(' ')[1].isnumeric() or guess.split(' ')[0] == "+" or "_" in guess:
            pass
        else:
            letter_to_remove = guess.split(' ')[0].upper()
            # print("executing")
            for answer in answer_list_parsed:
                # print(answer)
                # print(letter_to_remove)
                if letter_to_remove not in answer:
                    new_parsed.append(answer)
    return new_parsed


def handle_possible_letters(user_input, answer_list_parsed):
    """
    If a letter is in the solution but not in the correct position, we parse are list of solutions and only take
    solutions that have this letter in them.
    Returns a new list of solutions with those that fit this condition removed.
    """
    new_parsed = []
    for guess in user_input:
        if guess.split(' ')[1].isnumeric() or guess.split(' ')[0] == "-" or "_" in guess:
            pass
        else:
            letter_to_keep = guess.split(' ')[0].upper()
            for answer in answer_list_parsed:
                if letter_to_keep in answer:
                    new_parsed.append(answer)
    return new_parsed


def main():
    answers_unparsed_lines = read_answers()
    answers_only = parse_answsers(answers_unparsed_lines)
    guesses = []
    print("Type DONE at anytime into userinput to end the program")
    print("Options:\n"
          "\ta + = Only answers with a in it\n" +
          "\th - = Only answers without h in it\n" +
          "\tv 3 = Only Answers with v in the third position\n" +
          "\tt_4 = Only Answers where t is not the fourth position")
    user_input = input("Insert an option:")
    if user_input == "DONE":
        print("Did you get it?")
        return
    if "-" in user_input:
        # print("Executing first -")
        guesses.append(user_input)
        new_answer_list = handle_removing_letters(guesses, answers_only)
        print(new_answer_list)
    elif "+" in user_input:
        # print("Executing first +")
        guesses.append(user_input)
        new_answer_list = handle_possible_letters(guesses, answers_only)
        print(new_answer_list)
    else:
        # print("Executing first position")
        guesses.append(user_input)
        new_answer_list = handle_letter_position(guesses, answers_only)
        print(new_answer_list)
    while True:
        guesses = []
        user_input = input("Insert an option:")
        if user_input == "DONE":
            break
        if '-' in user_input:
            # print("Executing loop -")
            guesses.append(user_input)
            new_answer_list = handle_removing_letters(guesses, new_answer_list)
            print(new_answer_list)
        elif "+" in user_input:
            # print("Executing loop +")
            guesses.append(user_input)
            new_answer_list = handle_possible_letters(guesses, new_answer_list)
            print(new_answer_list)
        else:
            # print("Executing loop position")
            guesses.append(user_input)
            new_answer_list = handle_letter_position(guesses, new_answer_list)
            print(new_answer_list)
    print("Did you get it?")


main()

