__author__ = 'kyedidi'

""" Manually enter weights for unclassified entries with weight and gender. """
from reddit_database_manager import DatabaseManager
from reddit_submission import Submission
from reddit_analyzer import RedditAnalyzer, HITS_stats

from blessings import Terminal
t = Terminal()

import time

DATABASE_PATH = "reddit_submissions.sqlite"

def verify_submission_meets_criteria(submission):
  return (submission.current_weight_lbs is not None and
          submission.height_in is not None and
          submission.gender is not None)

def main():
  time_taken = 0
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
    #submission.media_json = None
    #submission.media_embed_json = None
    r = RedditAnalyzer(submission.title, submission.self_text)

    entries_processed = 0
    global_start_time = time.time()

    if r.has_gender() and r.has_height() and not r.has_current_weight():
      local_start_time = time.time()
      entries_processed += 1

      # TODO submission.manually_marked = 1


      print "ID: ", submission.id
      print "Title: ", submission.title
      print "Self text: ", submission.self_text

      print t.bold(t.red("CLASSIFICATION: " + r.get_debug_str()))
      print t.bold(t.red("LOW CONFIDENCE CLASSIFICATION: " + r.get_lc_debug_str()))
      print t.bold(t.green("Potential weights:" + ','.join(str(x) for x in r.potential_weights)))


      print "NOTE: If current weight is skipped, nothing will be saved."
      previous_weight = raw_input('Enter previous weight: ')
      current_weight = raw_input('Enter current weight: ')

      if previous_weight:
        print "Entered previous weight of: ", previous_weight

      if current_weight:
        print "Entered current weight of: ", current_weight


      if current_weight:
        submission.current_weight_lbs = int(current_weight)
        submission.previous_weight_lbs = int(previous_weight)

        # We know that one of the low confidence or regual is set,
        # so we know the below two if statements will be successful
        # in setting the values
        if not r.gender_is_female:
          r.gender_is_female = r.lc_gender_is_female

        if not r.height_in:
          r.height_in = r.lc_height_in



        submission.gender = r.gender_is_female
        submission.height_in = r.height_in
        if r.age:
          submission.age = r.age
        # submission.manually_verified
        print submission.to_tuple()
        assert(verify_submission_meets_criteria(submission))

        m.replace_submission(submission)
        print "Successfully entered."
        # entries_processed
        local_end_time = time.time()
        print "Entry took ", local_end_time - local_start_time, "seconds."
        print "Rate:", (3600 / (local_end_time - local_start_time)), "entries / hr."
        entries_per_second_so_far = entries_processed / (local_end_time - global_start_time)
        print "Ongoing Rate:", entries_per_second_so_far * 3600, "entries / hr."


      print
      # Later, we can work on the selftext
      #text = nltk.word_tokenize("And now for something completely different")
      #text2 = nltk.word_tokenize(submission.title)
      #print nltk.pos_tag(text2)


      print "---------------------------------------------------------------------"



  print title



if __name__ == "__main__":
  main()