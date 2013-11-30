__author__ = 'kyedidi'

# check this out for reg ex's:
# https://pythex.org/

# import praw
# import nltk
import re
import time

from parse import parse,search

HITS_stats = {'check_proper_gah': 0, 'gender_finder': 0,
              'height_finder': 0, 'height_inches': 0,
              'height_cm': 0, 'weight_identification': 0,
              'sw_cw_identification': 0}

class RedditAnalyzer:
  def __init__(self, title, self_text):
    self.title = title  # title of the post
    self.self_text = self_text

    self.height_in = None
    self.age = None
    self.gender_is_female = None

    self.previous_weight = None
    self.current_weight = None

    # lc_ = low confidence
    self.lc_height_in = None
    self.lc_age = None
    self.lc_gender_is_female = None
    self.lc_previous_weight = None
    self.lc_current_weight = None

    self.potential_weights = []

    self.analyze_input()
    # self.is_complete = check_if_complete()

  def has_height(self):
    return self.height_in is not None or self.lc_height_in is not None

  def has_gender(self):
    return self.gender_is_female is not None or self.lc_gender_is_female is not None

  def has_current_weight(self):
    return self.current_weight is not None or self.lc_current_weight is not None

  """
  def everything_complete_including_previous_weight(self):
    return (self.height_in is not None and
            self.age is not None and
            self.gender_is_female is not None and
            self.previous_weight is not None and
            self.current_weight is not None)

  """

  def get_lc_debug_str(self):
    result = []
    if self.lc_gender_is_female is not None:
      gender_str = "gender: "
      gender_str += "F" if self.lc_gender_is_female else "M"
      result.append(gender_str)
    if self.lc_age is not None:
      result.append("age: " + str(self.lc_age))
    if self.lc_height_in is not None:
      result.append("height(in):" + str(self.lc_height_in))

    if self.lc_previous_weight is not None:
      result.append("previous weight(lbs):" + str(self.lc_previous_weight))
    if self.lc_current_weight is not None:
      result.append("current weight(lbs):" + str(self.lc_current_weight))
    return ', '.join(result)

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
  def __is_reasonable_height(height_in):
    if height_in < 36 or height_in > 100:
      return False
    else:
      return True

  @staticmethod
  def __simple_height_finder_inches(string_to_search):
    """Converts a height string to an int (to height in inches)"""
    re_string = "(\d)'(\d*)"
    regex = re.compile(re_string)
    matches = regex.findall(string_to_search, re.IGNORECASE)
    if not matches or len(matches) > 1:
      return None
    match = matches[0]

    #print string_to_search
    #print match
    assert(len(match) == 2)
    feet = int(match[0])
    inches = 0
    if match[1] != "":
      inches = int(match[1])

    height = feet * 12 + inches

    if RedditAnalyzer.__is_reasonable_height(height):
      HITS_stats['height_inches'] += 1
      return height
    else:
      return None

  # TODO: make cm function more like inches
  """
  @staticmethod
  def __simple_height_finder_cm(string_to_search):
    # try search with and without space in between cm
    result = RedditAnalyzer.__try_search(["{cm:d}cm", "{cm:d} cm"], string_to_search)
    if result:
      height = result.named['cm'] / 2.54
      HITS_stats['height_cm'] += 1
      return height
    return None
  """

  @staticmethod
  def __height_finder(string_to_search):
    simple_result = RedditAnalyzer.__simple_height_finder_inches(string_to_search)
    if simple_result is not None:
      HITS_stats['height_finder'] += 1
      return simple_result

    # Temporarily disabling cm because of bugs

    """
    simple_result = RedditAnalyzer.__simple_height_finder_cm(string_to_search)
    if simple_result is not None:
      HITS_stats['height_finder'] += 1
      return simple_result
    """

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
  def __process_arbitrary_element_list(l):
    result = {}
    for e in l:

       # if elem in height
      # if elem is weight
      weight = RedditAnalyzer.__get_weight_from_str(e)
      if weight:
        result["weight"] = weight
        continue

      # if elem is age
      gender_is_female = RedditAnalyzer.__gender_finder(e)
      if gender_is_female:
        result["gender_is_female"] = gender_is_female
        continue

    return result

  def get_potential_weights(self, string_to_search):
    if not string_to_search:
      return
    re_string = """(\d+)\s*(lb|pounds)"""
    regex = re.compile(re_string)
    matches = regex.findall(string_to_search, re.IGNORECASE)
    for match in matches:
      # check match[0] and match[1]
      self.potential_weights.append(int(match[0]))

    if self.potential_weights:
      # remove duplicates
      self.potential_weights = sorted(list(set(self.potential_weights)))

    return



  def search_slash_delimited(self, string_to_search):
    # Four elements
    re_string = """([\w'"]*)/([\s\w'"]*)/([\s\w'"]*)/([\w'"]*)"""
    regex = re.compile(re_string)
    matches = regex.findall(string_to_search, re.IGNORECASE)

    if not matches:
      # Three elements
      re_string = """([\w'"]*)/([\s\w'"]*)/([\w'"]*)"""
      regex = re.compile(re_string)
      matches = regex.findall(string_to_search, re.IGNORECASE)

    if not matches:
      re_string = """([\w'"]*)/([\w'"]*)"""
      regex = re.compile(re_string)
      matches = regex.findall(string_to_search, re.IGNORECASE)

    if matches:
      result = RedditAnalyzer.__process_arbitrary_element_list(matches)

      if "height_in" in result:
        self.lc_height_in = result["height_in"]
      if "age" in result:
        self.lc_age = result["age"]
      if "gender_is_female" in result:
        self.lc_gender_is_female = result["gender_is_female"]
      if "current_weight" in result:
        self.lc_current_weight = result["current_weight"]

    return

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

      if self.self_text:
        self.lc_gender_is_female = self.__gender_finder(self.self_text)
        self.lc_height_in = self.__height_finder(self.self_text)

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
  def __get_weight_from_str(str):
    # TODO: handle the arrows and shit. Currently only handles one value
    # get number(s) from string
    # english_weight = ["pounds", "lbs"]
    re_string = "(\d+)\s*(lbs|pounds)*"
    regex = re.compile(re_string)
    matches = regex.findall(str, re.IGNORECASE)

    values_found = []
    if matches:
      for match in matches:
        values_found.append(match[0])  # has to be a number

    print values_found

    return

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

  @staticmethod
  def __find_number_after_prefix(prefix, text):
    """Finds number after text, eg. SW: 145"""
    re_string = prefix + "[\s:-]*(\d+)"
    regex = re.compile(re_string)
    matches = regex.findall(text, re.IGNORECASE)
    # print matches
    if not matches:
      return None
    if len(matches) > 1:
      # TODO: deal with this case
      return None

    match = matches[0]

    return match

  @staticmethod
  def __get_sw_and_cw(text):
    """ Searches text for SW and CW and returns the numbers
    after
    """

    if not text:
      return None, None

    sw = RedditAnalyzer.__find_number_after_prefix("SW", text)
    cw = RedditAnalyzer.__find_number_after_prefix("CW", text)
    return sw, cw

  def __get_weights(self):
    """ Gets the current and (if applicable) previous weight"""

    weight_rvalue = RedditAnalyzer.__simple_greater_than_or_hyphen_search(self.title)
    if weight_rvalue is not None:
      self.previous_weight = weight_rvalue['previous_weight']
      self.current_weight = weight_rvalue['current_weight']
      return
    # time.sleep(4)

    # Get weight by using SW: and CW:
    sw1, cw1 = RedditAnalyzer.__get_sw_and_cw(self.title)
    sw2, cw2 = RedditAnalyzer.__get_sw_and_cw(self.self_text)

    sw = None
    cw = None
    if sw1:
      sw = sw1
    if cw1:
      cw = cw1
    if sw2:
      sw = sw2
    if cw2:
      cw = cw2

    # print "current weight: ", cw
    # print "starting weight: ", sw
    if cw:
      self.previous_weight = sw
      self.current_weight = cw
      HITS_stats['sw_cw_identification'] += 1
      return



    # New way to extract all weights
    self.get_potential_weights(self.self_text)
    self.get_potential_weights(self.title)

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