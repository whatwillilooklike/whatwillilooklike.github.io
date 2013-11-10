__author__ = 'kyedidi'

from reddit_database_manager import DatabaseManager
from reddit_submission import Submission
from reddit_analyzer import RedditAnalyzer, HITS_stats


DATABASE_PATH = "reddit_submissions.sqlite"


def analyze_all_progress_pics():
  query = 'SELECT * FROM submissions WHERE manually_marked = 0 and manually_verified = 0;'
  m = DatabaseManager(DATABASE_PATH)

  # TODO: get all unique user names

  # for each user:
  # look up their submitted posts in the following subreddits

  # return [Submission(x) for x in c.fetchall()]
  all_matches = []
  submissions = [Submission(x) for x in m.query(query)]
  classifications = 0
  for submission in submissions:
    # M/28/5'7" Day 1, goal is to look as great as I feel!
    # "[MF]/\d+/\d+'\d+"
    print "Title: ", submission.title
    # submission.manually_verified

    #exit()
    print
    # Later, we can work on the selftext
    #text = nltk.word_tokenize("And now for something completely different")
    #text2 = nltk.word_tokenize(submission.title)
    #print nltk.pos_tag(text2)
    r = RedditAnalyzer(submission.title)

    # the if statement below is what makes it primary work for progress pics
    if r.everything_complete_including_previous_weight() and r.get_debug_str():
      #pass
      print "CLASSIFICATION: ", r.get_debug_str()
      print "BEFORE: ", submission.to_tuple()

      submission.gender = r.gender_is_female
      submission.age = r.age
      submission.height_in = r.height_in

      submission.previous_weight_lbs = r.previous_weight
      submission.current_weight_lbs = r.current_weight

      m.replace_submission(submission)

      print "AFTER: ", submission.to_tuple()
      classifications += 1

    print "---------------------------------------------------------------------"
    #exit()
  print "stats:"
  print HITS_stats
  print "classifications: ", classifications

def main():
  analyze_all_progress_pics()

if __name__ == "__main__":
  main()