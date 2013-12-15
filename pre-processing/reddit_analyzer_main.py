__author__ = 'kyedidi'

from reddit_database_manager import DatabaseManager
from reddit_submission import Submission
from reddit_analyzer import RedditAnalyzer, HITS_stats

from blessings import Terminal
t = Terminal()

DATABASE_PATH = "reddit_submissions.sqlite"


def analyze_all_progress_pics():
  # We primarily want to classify pictures which have associated media, but do not have a classification
  # We really don't give a shit about any of the other submissions.
  query = 'SELECT * FROM submissions WHERE manually_marked = 0 and manually_verified = 0 and media_json NOT NULL;'
  m = DatabaseManager(DATABASE_PATH)

  # TODO: get all unique user names

  # for each user:
  # look up their submitted posts in the following subreddits

  # return [Submission(x) for x in c.fetchall()]
  all_matches = []
  submissions = [Submission(x) for x in m.query(query)]
  classifications = 0
  total = 0
  weight_and_height = 0
  atleast_height = 0
  for submission in submissions:
    total += 1
    # M/28/5'7" Day 1, goal is to look as great as I feel!
    # "[MF]/\d+/\d+'\d+"

    r = RedditAnalyzer(submission.title, submission.self_text)


    # print "BEFORE: ", submission.to_tuple()

    # the if statement below is what makes it primary work for progress pics
    if r.has_gender() and r.has_height() and r.has_current_weight():
      #pass
      #print "CLASSIFICATION: ", r.get_debug_str()
      #print "BEFORE: ", submission.to_tuple()

      # Either the value or the lc_value (low confidence)
      # value will be set. We want to set the submission with
      # one of those, preferably the non-lc version

      # Gender
      if r.gender_is_female is not None:
        submission.gender = r.gender_is_female
      else:
        submission.gender = r.lc_gender_is_female

      # Height
      if r.height_in is not None:
        submission.height_in = r.height_in
      else:
        submission.height_in = r.lc_height_in

      # Current Weight
      if r.current_weight is not None:
        submission.current_weight_lbs = r.current_weight
      else:
        submission.current_weight_lbs = r.lc_current_weight

      # Previous Weight
      if r.previous_weight is not None:
        submission.previous_weight_lbs = r.previous_weight
      else:
        submission.previous_weight_lbs = r.lc_previous_weight

      m.replace_submission(submission)
      # print "AFTER: ", submission.to_tuple()
      classifications += 1

    if r.has_current_weight() and r.has_height() and r.get_debug_str():
      weight_and_height += 1

    if r.has_height():
      atleast_height += 1

    # Start Print statements
    if r.has_gender() and r.has_height() and not r.has_current_weight():
      print "Title: ", submission.title
      print "Self text: ", submission.self_text
      # submission.manually_verified

      #exit()
      print
      # Later, we can work on the selftext
      #text = nltk.word_tokenize("And now for something completely different")
      #text2 = nltk.word_tokenize(submission.title)
      #print nltk.pos_tag(text2)

      print t.bold(t.red("CLASSIFICATION: " + r.get_debug_str()))
      print t.bold(t.red("LOW CONFIDENCE CLASSIFICATION: " + r.get_lc_debug_str()))
      print t.bold(t.green("Potential weights:" + ','.join(str(x) for x in r.potential_weights)))

    # End Print statements


    print "---------------------------------------------------------------------"
    #exit()
  print "stats:"
  print HITS_stats
  print "classifications: ", classifications, " out of a total: ", total
  print "Only weight and height: ", weight_and_height
  print "Atleast height: ", atleast_height


def main():
  analyze_all_progress_pics()

if __name__ == "__main__":
  main()