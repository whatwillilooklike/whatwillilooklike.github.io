__author__ = 'kyedidi'

# import praw
# import nltk
import re
from reddit_database_manager import DatabaseManager
from reddit_submission import Submission

from parse import parse,search

DATABASE_PATH = "reddit_submissions.sqlite"
HITS_check_proper_gah = 0

# check this out for reg ex's:
# https://pythex.org/

class RedditAnalyzer:
  def __init__(self, title):
    self.title = title  # title of the post

    self.height_in = None
    self.age = None
    self.gender_is_female = None

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

    return ','.join(result)

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
  def __gender_finder(string_to_search):
    """Finds the gender in a string. """
    # explained: male | female | (new string | space | / | ( | digit) (m | f) (space | / | ) )
    re_string = "(male|female|(\A|\s|/|\(|\d)(f|m)(\s|/|\)))"
    regex = re.compile(re_string, re.IGNORECASE)
    match = regex.search(string_to_search)
    if match:
      match_str = match.group(0)
      gender_str = ''.join(c for c in match_str if c.isalpha())  # remove preceding / trailing (/ or ()
      # print gender_str
      gender = RedditAnalyzer.__gender_from_string(gender_str)
      return gender
    return None

  def __check_proper_gah(self):
    # Check for the gah (gender / height / age) when formatted as: M/28/5'7"
    re_string = "([MF]/\d+/\d+'\d+)"
    regex = re.compile(re_string, re.IGNORECASE)
    # print regex.match(submission.tti)
    match = regex.search(self.title)
    if match:
      gah_str = match.group(0)
      # print gah_str
      # self.debug_str = gah_str
      result = search("{gender}/{age:d}/{feet:d}'{in:d}", gah_str)
      # print result.named
      self.gender_is_female = self.__gender_from_string(result.named['gender'])
      self.age = result.named['age']
      self.height_in = result.named['feet'] * 12 + result.named['in']
      return True
    return False
    # TODO: use the parse module to read the stuff from the string (ie. scanf equivalent)

  def analyze_input(self):
    global HITS_check_proper_gah

    # Step 1: Find the gender
    if self.__check_proper_gah():
      HITS_check_proper_gah += 1
    else:
      # TODO: other ways to find this information
      gender = self.__gender_finder(self.title)
      if gender is not None:
        self.gender_is_female = gender

    # Step 2: Find the
    # else, try other ways to search for weight, and height

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
    print "---------------------------------------------------------------------"
    print "Title: ", submission.title
    print
    # Later, we can work on the selftext
    #text = nltk.word_tokenize("And now for something completely different")
    #text2 = nltk.word_tokenize(submission.title)
    #print nltk.pos_tag(text2)
    r = RedditAnalyzer(submission.title)
    if r.get_debug_str():
      print "CLASSIFICATION: ", r.get_debug_str()

    # print matches
    #if matches and len(matches > 1):
    #  all_matches.append(matches[0])
    #  print matches[0]

    # print "classification: (nothing for now)"
    print "---------------------------------------------------------------------"
    #exit()
  print "stats:"
  print "HITS_check_proper_gah = ", HITS_check_proper_gah

if __name__ == "__main__":
  main()