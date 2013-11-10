__author__ = 'kyedidi'

# import praw
# import nltk
import re
import time
from reddit_database_manager import DatabaseManager
from reddit_submission import Submission

from parse import parse,search

DATABASE_PATH = "reddit_submissions.sqlite"
HITS_stats = {'check_proper_gah': 0, 'gender_finder': 0,
              'height_finder': 0, 'height_inches': 0,
              'height_cm': 0, 'weight_identification': 0}

# check this out for reg ex's:
# https://pythex.org/

class RedditAnalyzer:
  def __init__(self, title):
    self.title = title  # title of the post

    self.height_in = None
    self.age = None
    self.gender_is_female = None

    self.previous_weight = None
    self.current_weight = None

    self.analyze_input()
    # self.is_complete = check_if_complete()

  def get_debug_str(self):
    result = []
    if self.gender_is_female is not None:
      gender_str = "gender: "
      gender_str += "F" if self.gender_is_female else "M"
      result.append(gender_str)
    if self.age is not None:
      result.append("age: " + str(self.age))
    if self.height_in is not None:
      result.append("height(in):" + str(self.height_in))

    if self.previous_weight is not None:
      result.append("previous weight(lbs):" + str(self.previous_weight))
    if self.current_weight is not None:
      result.append("current weight(lbs):" + str(self.current_weight))


    return ', '.join(result)

  @staticmethod
  def __gender_from_string(gender_str):
    # we want to look at only the first character in case it is a male or female string
    if gender_str.lower()[0] == 'f':
      return True
    elif gender_str.lower()[0] == 'm':
      return False
    else:
      return None

  @staticmethod
  def __try_search(queries, string_to_search):
    result = None
    for query in queries:
      try:
        result = search(query, string_to_search)
      except ValueError:
        # This occurs if there's an apostrophe (') in the input string and it can't
        # convert a string and int
        pass
      if result is not None:
        return result
    return None

  @staticmethod
  def __simple_height_finder_inches(string_to_search):
    """Converts a height string to an int (to height in inches)"""
    result = RedditAnalyzer.__try_search(["{feet:d}'{in:d}"], string_to_search)
    if result:
      height = result.named['feet'] * 12 + result.named['in']
      HITS_stats['height_inches'] += 1
      return height
    return None

  @staticmethod
  def __simple_height_finder_cm(string_to_search):
    # try search with and without space in between cm
    result = RedditAnalyzer.__try_search(["{cm:d}cm", "{cm:d} cm"], string_to_search)
    if result:
      height = result.named['cm'] / 2.54
      HITS_stats['height_cm'] += 1
      return height
    return None

  @staticmethod
  def __height_finder(string_to_search):
    simple_result = RedditAnalyzer.__simple_height_finder_inches(string_to_search)
    if simple_result is not None:
      HITS_stats['height_finder'] += 1
      return simple_result

    simple_result = RedditAnalyzer.__simple_height_finder_cm(string_to_search)
    if simple_result is not None:
      HITS_stats['height_finder'] += 1
      return simple_result

    """
    re_string = ""
    regex = re.compile(re_string, re.IGNORECASE)
    match = regex.search(string_to_search)
    if match:
      height_str = match.group(0)
      return RedditAnalyzer.__height_string_to_int_in(height_str)
    """
    return None


  @staticmethod
  def __gender_finder(string_to_search):
    """Finds the gender in a string. """
    # explained: male | female | (new string | space | / | ( | digit | [) (m | f) (space | / | ) ] -)
    re_string = "(male|female|(\A|\s|/|\(|\d|\[)(f|m)(\s|/|\)|\]|-|\.))"
    regex = re.compile(re_string, re.IGNORECASE)
    match = regex.search(string_to_search)
    if match:
      match_str = match.group(0)
      gender_str = ''.join(c for c in match_str if c.isalpha())  # remove preceding / trailing (/ or ()
      # print gender_str
      gender = RedditAnalyzer.__gender_from_string(gender_str)
      HITS_stats['gender_finder'] += 1
      return gender
    return None

  @staticmethod
  def __check_proper_gah(string_to_search):
    # Check for the gah (gender / height / age) when formatted as: M/28/5'7"
    re_string = "((m|f|male|female)/\d+/\d+'\d+)"
    regex = re.compile(re_string, re.IGNORECASE)
    # print regex.match(submission.tti)
    match = regex.search(string_to_search)
    if match:
      rvalue = {}
      gah_str = match.group(0)
      # print gah_str
      # self.debug_str = gah_str
      result = search("{gender}/{age:d}/{feet:d}'{in:d}", gah_str)
      # print result.named
      rvalue['gender_is_female'] = RedditAnalyzer.__gender_from_string(result.named['gender'])
      rvalue['age'] = result.named['age']
      rvalue['height_in'] = result.named['feet'] * 12 + result.named['in']
      HITS_stats['check_proper_gah'] += 1
      return rvalue
    return None
    # TODO: use the parse module to read the stuff from the string (ie. scanf equivalent)

  def __get_gender_age_height(self):
    gah_result = self.__check_proper_gah(self.title)
    if gah_result is not None:
      self.gender_is_female = gah_result['gender_is_female']
      self.age = gah_result['age']
      self.height_in = gah_result['height_in']
    else:
      # TODO: other ways to find this information
      gender = self.__gender_finder(self.title)
      if gender is not None:
        self.gender_is_female = gender

      height = self.__height_finder(self.title)
      if height is not None:
        self.height_in = height

    return

  @staticmethod
  def reasonable_weight(weight):
    if weight < 80:
      return False
    if weight > 400:
      return False
    return True


  @staticmethod
  def __simple_greater_than_or_hyphen_search(string_to_search):
    # search for two numbers seperated by a > symbol
    re_string = "(\d+\.?\d*)(\D*)(&gt;|-|to)\D*(\d+\.?\d*)\s*(\w*)"
    regex = re.compile(re_string)
    matches = regex.findall(string_to_search, re.IGNORECASE)
    # print matches
    if matches:
      for match in matches:
        previous = float(match[0])
        current = float(match[3])
        # print "previous: ", previous, "current:", current
        if (RedditAnalyzer.reasonable_weight(previous) and
            RedditAnalyzer.reasonable_weight(current)):
          # print "previous: ", previous, "current:", current
          HITS_stats['weight_identification'] += 1
          return {'previous_weight': previous, 'current_weight': current}

        # print match
    # exit()
    # result = None
    # time.sleep(4)

    return None

  def __get_weights(self):
    """ Gets the current and (if applicable) previous weight"""

    weight_rvalue = RedditAnalyzer.__simple_greater_than_or_hyphen_search(self.title)
    if weight_rvalue is not None:
      self.previous_weight = weight_rvalue['previous_weight']
      self.current_weight = weight_rvalue['current_weight']
    # time.sleep(4)
    return None

  def analyze_input(self):
    """ Only the functions directly called from this function should be
    instance methods. Others should be static to limit the number of
    places that instance variables are modified
    """

    # Step 1: Find the gender, age, and height
    self.__get_gender_age_height()

    # Step 2: Find the weights (current and previous if applicable)
    self.__get_weights()

    # Step 3:
    # self.__check_proper_gah_parse()

  def get_stats(self):
    pass

def main():
  query = 'SELECT * FROM submissions;'
  m = DatabaseManager(DATABASE_PATH)

  # TODO: get all unique user names

  # for each user:
  # look up their submitted posts in the following subreddits

  # return [Submission(x) for x in c.fetchall()]
  all_matches = []
  submissions = [Submission(x) for x in m.query(query)]
  for submission in submissions:
    # M/28/5'7" Day 1, goal is to look as great as I feel!
    # "[MF]/\d+/\d+'\d+"
    print "Title: ", submission.title
    print
    # Later, we can work on the selftext
    #text = nltk.word_tokenize("And now for something completely different")
    #text2 = nltk.word_tokenize(submission.title)
    #print nltk.pos_tag(text2)
    r = RedditAnalyzer(submission.title)
    if r.get_debug_str():
      #pass
      print "CLASSIFICATION: ", r.get_debug_str()

    # print matches
    #if matches and len(matches > 1):
    #  all_matches.append(matches[0])
    #  print matches[0]

    # print "classification: (nothing for now)"
    print "---------------------------------------------------------------------"
    #exit()
  print "stats:"
  print HITS_stats

if __name__ == "__main__":
  main()