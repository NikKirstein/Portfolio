import jsonlines
import spacy
from spacy.matcher import Matcher
import time
import csv
import os
import re
# from spacy import displacy


"""
┌─┐┌─┐┌┬┐┌─┐┬  
├─┘├┤  ││├─┤│  
┴  └─┘─┴┘┴ ┴┴─┘
A siri like "AI" which really is just a question answering bot.
Uses a subset of Google's Natural Questions corpus.
Also allows users to ask their own questions. Answers my vary in correctness

Written by Nik Kirstein
Started writing: 04/17/19
"""

"""
jsonl scheme
------------
annotations
document_html
document_title
document_tokens
document_url
example_id
long_answer_candidates
question_text
question_tokens
"""


def get_question_answer_tuple_list(filename, main_q_list):
    """
    Processes jsonlines files and creates a tuple of questions and answers
    :param filename: a filename, should be a jsonline file.
    :param main_q_list: a list, this is an empty list fed to the function
    :return: main_q_list: Modified in place list of question answer tuples
    """
    print("Processing:", filename, "... Adding to QA list. We skip questions without answers")
    with open(filename, 'r') as f:  # opening file in binary(rb) mode
        for item in jsonlines.Reader(f):
            try:
                # print("question:", item['question_text'])
                long_ans_start_index = item['annotations'][0]['long_answer']['start_token']
                long_ans_end_index = item['annotations'][0]['long_answer']['end_token']
                # print("annotations:", item['annotations'][0]['long_answer'])
                answer = item['document_tokens'][long_ans_start_index:long_ans_end_index]
                # print(answer)
                text_ans = ""
                for ans_dict in answer:
                    text_ans += ans_dict['token'] + " "
                # print(text_ans)

                # print((item['question_text'], text_ans))
                if text_ans != '':  # skip questions with no annotated answers
                    main_q_list.append((item['question_text'], text_ans))

            except jsonlines.jsonlines.InvalidLineError:
                # Horrible practice but w/e
                pass

    return main_q_list


def write_to_tsv(main_qs, main_as, out_file):
    """
    Writes to a tsv files.  Questions and answers.
    :param main_qs: list of questions
    :param main_as: list of answers
    :param out_file: filename of outfile.
    :return: None, filewriting function
    """
    with open(out_file, 'w', newline='') as tsvfile:
        for i in range(len(main_qs)):
            tsvwriter = csv.writer(tsvfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
            tsvwriter.writerow([main_qs[i], main_as[i]])
    return None


def compare_vectors(triple1, triple2):
    """
    Compares two vectors.  Compares specific parts since vectors are usually in the format
    of.  (question word, nounphrase, verb) and (nounphrase, verb, answer)
    :param triple1: first triple to compare
    :param triple2: second triple to compare
    :return: triple_score: Addition of both similarities into a score
    """
    noun_comparison = triple1[1].similarity(triple2[0])
    verb_comparison = triple1[2].similarity(triple2[1])
    triple_score = noun_comparison + verb_comparison
    return triple_score


def generate_score_list(vector1, t_list2):
    """
    Using one vector comparing its similarities to all other vectors in a list, generates a score list
    :param vector1: vector to compare against all other vectors
    :param t_list2: list of triple vectors
    :return: score_list: list of similarity scores
    """
    score_list = []
    for i in range(len(t_list2)):
        if vector1 is None or t_list2[i] is None:
            score_list.append(0)
        else:
            score_list.append(compare_vectors(vector1, t_list2[i]))
    return score_list


def vectorize_words_in_tuple(tuple_list):
    """
    Goes through a list of triples and uses spacy to make them vectors.  Looks the same but different objects entirely
    :param tuple_list: list of triple tuples
    :return: vectorized_tuple_list, almost identical to the input but spacy token objects of vectors
    """
    vectorized_tuple_list = []
    nlp = spacy.load('en_core_web_lg')
    for triple in tuple_list:
        vectored0 = nlp(triple[0])
        vectored1 = nlp(triple[1])
        vectored2 = nlp(triple[2])
        vectorized_tuple_list.append((vectored0, vectored1, vectored2))
    return vectorized_tuple_list


def load_predefined_tuples(filename):
    """
    Loads triple tuples from reverb
    :param filename: name of the file
    :return: a list of the reverb triples
    """
    list_of_predefined_tuples = []
    with open(filename, 'r', encoding="utf-8") as f:
        for row in f:
            split_row = row.split('\t')
            list_of_predefined_tuples.append((split_row[1].lower(), split_row[2].lower(), split_row[3].lower()))

    return list_of_predefined_tuples


def load_parsed_tuples(filename):
    """
    loads triples from tsv files made by hand.
    :param filename: name of the file
    :return: a list of parsed_tuples. Function is almost identical to the one above but I'm reading files I already
    wrote myself so the format is nicer and cleaner but in slightly different form so new function.
    """
    list_of_parsed_tuples = []
    with open(filename, 'r', encoding='utf-8') as f:
        for row in f:
            split_row = row.split('\t')
            list_of_parsed_tuples.append((split_row[0], split_row[1], split_row[2]))
    return list_of_parsed_tuples


def read_from_tsv(filename):
    """
    reads from a tsv file.  This is the annotated file that I annotated by hand.
    :param filename: name of the file
    :return: parsed_qa_tuples_list is the main question answer tuple we use everywhere else.
            gold_tuples is obviously a list of triples of the gold standard triples
    """
    parsed_qa_tuples_list = []
    gold_tuples = []
    with open(filename, 'r', newline='', encoding='utf-8') as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter='\t')
        for row in tsvreader:
            # print(row)
            parsed_qa_tuples_list.append((row[0], row[1]))
            gold_tuples.append((row[2], row[3], row[4]))
    return parsed_qa_tuples_list, gold_tuples


def parse_main_reverb_tuples(reverb_tuples, gold_list):
    """
    Parses the 15 million reverb triples using verbs and nouns in our own triples.  It's all I could think to do
    to make it so I don't search through 15 million triples
    :param reverb_tuples: all 15 million reverb triples
    :param gold_list: annotated list of gold_standard triples to parse the list.  One day this will change to triples
    I extracted using the grammar parser
    :return: parsed_reverb_list
    """
    parsed_reverb_list = []
    for triple in gold_list:
        noun = triple[0]
        verb = triple[1]
        for long_triple in reverb_tuples:
            if verb in long_triple or noun in long_triple:
                parsed_reverb_list.append(long_triple)

    # print(len(parsed_reverb_list))
    return parsed_reverb_list


def write_parsed_reverb_to_file(parsed_reverb_list, filename):
    """
    Writes the parsed reverb list to a file because not doing so makes the program super slow.
    :param parsed_reverb_list: a parsed triple list of reverb triples
    :param filename: name of the file
    :return: None, file writing function

    """
    with open(filename, 'w') as f:
        for triple in parsed_reverb_list:
            f.write(str(triple[0]) + "\t" + str(triple[1]) + "\t" + str(triple[2]) + "\n")

    return None


def parse_where_questions(main_q_list):
    """
    goes through the jsonlines questions in a list and parses down questions that I can deal with.
    :param main_q_list: list of jsonlines questions from googles natural questions dataset
    :return: where_questions, list of questions and where_answers, a list of answers
    """
    # Print trees for all questions.
    # Print high level trees and see how much I see of what (frequency)
    # narrow it down based on entities/grammar/tree structure?
    # Otherwise, questions are too widespread and hard to query

    where_questions = []
    where_answers = []
    nlp = spacy.load("en_core_web_sm")

    for qa_tuple in main_q_list:
        if "where" in qa_tuple[0]:
            question = nlp(qa_tuple[0])
            # print(question[0].pos_)
            answer = qa_tuple[1]

            if (
                    question[0].pos_ == "ADV" and
                    question[1].pos_ == "VERB" and
                    question[(len(question) - 1)].pos_ == "VERB"
            ):
                # print("FOUND", question)
                where_questions.append(question)
                where_answers.append(answer)
    return where_questions, where_answers


def pre_process_files():
    """
    Function to handle a bunch of preprocessing junk if you haven't done it already.
    Big files so this function will likely fail without the included files below but you shouldn't need them to run the
    program if you have the other parsed versions of the files.
    :return: None
    """
    print("Parsed TSV files not found, creating questions from .jsonl files")
    print("Please make sure you have the jsonl files available if this is appearing")
    main_question_list = []

    # Parse and populate our question list and toss questions without answers
    get_question_answer_tuple_list('nq-dev-00.jsonl', main_question_list)  # Populate list with data from jsonl
    get_question_answer_tuple_list('nq-dev-01.jsonl', main_question_list)  # Append to existing list with more data
    get_question_answer_tuple_list('nq-dev-02.jsonl', main_question_list)  # Append to existing list with more data
    get_question_answer_tuple_list('nq-dev-03.jsonl', main_question_list)  # Append to existing list with more data
    get_question_answer_tuple_list('nq-dev-04.jsonl', main_question_list)  # Append to existing list with more data

    # Further parse questions based on criteria to get similar questions
    main_where_questions, main_where_answers = parse_where_questions(main_question_list)

    # Total questions: 126 questions
    # how many questions we have right now.
    # print("Length of questions and answers", len(main_where_questions))
    dev_questions = main_where_questions[0:49]
    dev_answers = main_where_answers[0:49]
    training_questions = main_where_questions[50:100]
    training_answers = main_where_answers[50:100]
    test_questions = main_where_questions[101:]
    test_answers = main_where_answers[101:]
    print("Writing TSV files for easier retrieval")
    write_to_tsv(dev_questions, dev_answers, 'DevSet.tsv')
    write_to_tsv(training_questions, training_answers, 'TrainingSet.tsv')
    write_to_tsv(test_questions, test_answers, 'TestSet.tsv')

    return None


def toss_stop_words(qa_tuple_list):
    """
    UNUSED. Takes stop words out of question answer tuples
    :param qa_tuple_list: a list of question answer tuples
    :return: a list of the same above but questions and answers have no stop words
    """
    qa_tuple_list_stopped_remove = []
    nlp = spacy.load("en_core_web_sm")
    for qa in qa_tuple_list:
        question = nlp(qa[0])
        # print(question)
        answer = nlp(qa[1])
        new_question = ""
        new_answer = ""
        for qs_token in question:
            if not qs_token.is_stop:
                new_question += str(qs_token) + " "
        for ans_token in answer:
            if not ans_token.is_stop:
                new_answer += str(ans_token) + " "
        qa_tuple_list_stopped_remove.append((new_question, new_answer))
        # print(token)
        # print(token.is_stop)
    return qa_tuple_list_stopped_remove


def grammar_parser2(subset_questions):
    """
    An attempt that never made it to light.  Not used but kept for history.
    :param subset_questions:
    :return: None
    """
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)
    pattern = [{'TAG': 'DT', 'OP': '?'},
               {'TAG': 'PP', 'OP': '?'},
               {'TAG': 'JJ', 'OP': '*'},
               {'TAG': 'NN', 'OP': '+'},
               {'TAG': 'IN', 'OP': '?'},
               {'TAG': 'NNS', 'OP': '?'},
               {'TAG': 'NNP', 'OP': '?'}]
    matcher.add("NP", None, pattern)

    for qa_tuple in subset_questions:
        question = nlp(qa_tuple[0])
        print(question)
        tagged_question = ""
        for token in question:
            tagged_question += str(token) + " " + str(token.tag_) + " "
        print(tagged_question)
        matches = matcher(question)
        print(matches)


def strip_noun(phrase_list):
    """
    Strips part of speech tags from noun_phrases
    :param phrase_list: strings of noun_phrases with part of speech tags
    :return: new_phrase, same as input without part of speech tags
    """
    part_of_speech_tags = ['AFX', 'BES', 'CC', 'CD', 'DT', 'CCONJ', 'DET',
                           'EX', 'FW', 'HVS', 'HYPH', 'IN', 'JJ', 'JJR', 'JJS',
                           'MD', 'NFP', 'NN', 'NNP', 'NNS', 'PDT', 'POS', 'PRP',
                           'RB', 'RBR', 'RBS', 'UH', 'VB', 'VBD', 'VBG', 'VBN',
                           'VBP', 'VBZ', 'WDT', 'WP', 'WRB']
    new_phrase = []
    for word_pos in phrase_list:
        split_words = word_pos.split(" ")
        for non_pos in split_words:
            if non_pos not in part_of_speech_tags:
                new_phrase.append(non_pos)
    return " ".join(new_phrase)


def strip_verb(phrase_list):
    """
    This is really disgusting but I'm going crazy at this point.
    I am so sorry for this function.
    :param phrase_list: a verb phrase input with part of speech tags
    :return: same phrase without part of speech tags.
    """
    part_of_speech_tags = ['AFX', 'BES', 'CC', 'CD', 'DT', 'CCONJ', 'DET',
                           'EX', 'FW', 'HVS', 'HYPH', 'IN', 'JJ', 'JJR', 'JJS',
                           'MD', 'NFP', 'NN', 'NNP', 'NNS', 'PDT', 'POS', 'PRP',
                           'RB', 'RBR', 'RBS', 'UH', 'VB', 'VBD', 'VBG', 'VBN',
                           'VBP', 'VBZ', 'WDT', 'WP', 'WRB']
    new_phrase = []
    if len(phrase_list) > 1:
        phrase_list.pop(0)
    for word_tuple in phrase_list:
        for item in word_tuple:
            split_item = item.split(" ")
            for mini_item in split_item:
                if mini_item not in part_of_speech_tags:
                    new_phrase.append(mini_item)
    return " ".join(new_phrase)


def grammar_parser(subset_questions):
    """
    Goes through a list of questions and builds triples from them.
    :param subset_questions: a list of questions
    :return: a tuple list of triples
    """
    nlp = spacy.load("en_core_web_sm")
    noun_regex = r"(?:(?:\w+ DT )?(?:\w+ JJ )*)?\w+ (?:N[NP]|PRN)"
    verb_regex = r"(?:(NN|VBG|JJ|NNP|CD|VB|NNS|RB))+ (\w+ (VBN|VBD|VBP))"
    my_tuple_list = []
    for qa_tuple in subset_questions:
        string_tagged_question = ""
        question = nlp(qa_tuple[0])
        for string_tagged_token in question:
            string_tagged_question += str(string_tagged_token) + " "
            string_tagged_question += str(string_tagged_token.tag_) + " "
        # print(string_tagged_question)
        noun_phrase = re.findall(noun_regex, string_tagged_question)
        verb_phrase = re.findall(verb_regex, string_tagged_question)
        # print(noun_phrase)
        # print(verb_phrase)
        new_noun_phrase = strip_noun(noun_phrase)
        new_verb_phrase = strip_verb(verb_phrase)
        # print(new_noun_phrase)
        # print(new_verb_phrase)
        my_tuple_list.append(("where", new_noun_phrase, new_verb_phrase))

    return my_tuple_list


def run_dev_set(question_to_ask):
    """
    Runs dev main basically.  Just functionalized to be clean.
    :param question_to_ask: which question from the dev set to test.
    :return: None
    """
    parsed_dev_qas, dev_gold_tuples = read_from_tsv('DevSetAnnotated.tsv')
    my_tuples = grammar_parser(parsed_dev_qas)
    my_vectored = vectorize_words_in_tuple(my_tuples)

    exists = os.path.isfile('DevParsedComparisonTuples.txt')
    if not exists:
        predefined_tuple_list = load_predefined_tuples('reverb_clueweb_tuples-1.1.txt')
        parsed_reverb_tuples = parse_main_reverb_tuples(predefined_tuple_list, dev_gold_tuples)
        write_parsed_reverb_to_file(parsed_reverb_tuples, 'DevParsedComparisonTuples.txt')
    else:
        loaded_from_list_tuples = load_parsed_tuples('DevParsedComparisonTuples.txt')
        # we don't use this and compare to the gold standard instead because it took 900 seconds to run against this.
        # Ideally we would then use this list: loaded_from_list_tuples which is 28000 long or so and vectorize it.
        # After vectorizing, we generate the score list, making it insanely long.  Once we get a score of 28000
        # similarities, we get the max, get its index and grab the third value from the tuple at that index, that
        # should be our correct answer.
    pre_vectored = vectorize_words_in_tuple(dev_gold_tuples)
    question_we_ask = generate_score_list(my_vectored[question_to_ask], pre_vectored)
    likely_answer = max(question_we_ask)
    # The real gold here.  We get the highest similarity and we assign it to a variable
    # print(likely_answer)
    location = question_we_ask.index(likely_answer)
    # Then we just look for where that value sits in the index of a list and that position should give us the triple
    # That we want, then just put that index into the gold standards (or in the future, we have to do another similarity
    # Check, and that gives us our output. Basically, my system of cosine similarity is in fact giving me the right
    # index most of the time so that's a good sign.
    # print(location)
    print("Question:", my_vectored[question_to_ask])
    print("Output answer:", pre_vectored[location][2])
    print("Expected answer:", pre_vectored[question_to_ask][2])
    return None


def run_training_set(question_to_ask):
    """
    Runs training main basically.  Just functionalized to be clean.
    :param question_to_ask: which question from the training set to test.
    :return: None
    """
    parsed_training_qas, training_gold_tuples = read_from_tsv('TrainingSetAnnotated.tsv')
    my_tuples = grammar_parser(parsed_training_qas)
    my_vectored = vectorize_words_in_tuple(my_tuples)

    exists = os.path.isfile('TrainingParsedComparisonTuples.txt')
    if not exists:
        predefined_tuple_list = load_predefined_tuples('reverb_clueweb_tuples-1.1.txt')
        parsed_reverb_tuples = parse_main_reverb_tuples(predefined_tuple_list,  training_gold_tuples)
        write_parsed_reverb_to_file(parsed_reverb_tuples, 'TrainingParsedComparisonTuples.txt')
    else:
        loaded_from_list_tuples = load_parsed_tuples('TrainingParsedComparisonTuples.txt')
        # we don't use this and compare to the gold standard instead because it took 900 seconds to run against this.
    pre_vectored = vectorize_words_in_tuple(training_gold_tuples)
    question_we_ask = generate_score_list(my_vectored[question_to_ask], pre_vectored)
    likely_answer = max(question_we_ask)
    # print(likely_answer)
    location = question_we_ask.index(likely_answer)
    # print(location)
    print("Question:", my_vectored[question_to_ask])
    print("Output answer:", pre_vectored[location][2])
    print("Expected answer:", pre_vectored[question_to_ask][2])
    return None


def run_test_set(question_to_ask):
    """
    Runs test main basically.  Just functionalized to be clean.
    :param question_to_ask: which question from the test set to test.
    :return: None
    """
    parsed_test_qas, test_gold_tuples = read_from_tsv('TestSetAnnotated.tsv')
    my_tuples = grammar_parser(parsed_test_qas)
    my_vectored = vectorize_words_in_tuple(my_tuples)

    exists = os.path.isfile('TestParsedComparisonTuples.txt')
    if not exists:
        predefined_tuple_list = load_predefined_tuples('reverb_clueweb_tuples-1.1.txt')
        parsed_reverb_tuples = parse_main_reverb_tuples(predefined_tuple_list, test_gold_tuples)
        write_parsed_reverb_to_file(parsed_reverb_tuples, 'TestParsedComparisonTuples.txt')
    else:
        loaded_from_list_tuples = load_parsed_tuples('TestParsedComparisonTuples.txt')
        # we don't use this and compare to the gold standard instead because it took 900 seconds to run against this.
    pre_vectored = vectorize_words_in_tuple(test_gold_tuples)
    question_we_ask = generate_score_list(my_vectored[question_to_ask], pre_vectored)
    likely_answer = max(question_we_ask)
    # print(likely_answer)
    location = question_we_ask.index(likely_answer)
    # print(location)
    print("Question:", my_vectored[question_to_ask])
    print("Output answer:", pre_vectored[location][2])
    print("Expected answer:", pre_vectored[question_to_ask][2])
    return None


def main():
    """
    Main function
    :return: None
    """
    start_run = time.time()

    exists = os.path.isfile('DevSetAnnotated.tsv')
    if not exists:
        pre_process_files()
    else:
        menu_choice = input("insert number 1-3 or q to quit. 1:Dev, 2:training, 3:test\n")
        if menu_choice == "1":
            question_to_try = input("Test questions 1-48, insert a number\n")
            run_dev_set(int(question_to_try))
        elif menu_choice == "2":
            question_to_try = input("Test questions 1-49, insert a number\n")
            run_training_set(int(question_to_try))
        elif menu_choice == "3":
            question_to_try = input("Test questions 1-24, insert a number\n")
            run_test_set(int(question_to_try))
        elif menu_choice == "q":
            print("quitting")

    end_run = time.time()
    print("script ran in:", str(round(end_run - start_run, 4)), "seconds")


if __name__ == '__main__':
    main()
