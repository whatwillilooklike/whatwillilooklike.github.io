__author__ = 'kyedidi'
__author__ = 'kyedidi'

from reddit_database_manager import DatabaseManager
from reddit_submission import Submission
from reddit_analyzer import RedditAnalyzer, HITS_stats

from blessings import Terminal
t = Terminal()

DATABASE_PATH = "reddit_submissions.sqlite"


def run_test():
  # We primarily want to classify pictures which have associated media, but do not have a classification
  # We really don't give a shit about any of the other submissions.
  submission_id = "1hncxw"
  query = 'SELECT * FROM submissions WHERE id="%s"' % submission_id
  m = DatabaseManager(DATABASE_PATH)
  # TODO: get all unique user names

  # for each user:
  # look up their submitted posts in the following subreddits

  # return [Submission(x) for x in c.fetchall()]
  all_matches = []
  submissions = [Submission(x) for x in m.query(query)]
  assert(len(submissions) == 1)
  submission = submissions[0]

  # M/28/5'7" Day 1, goal is to look as great as I feel!
  # "[MF]/\d+/\d+'\d+"

  r = RedditAnalyzer(submission.title, submission.self_text)

  # Start Print statements
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

  # End Print statement.

def main():
  run_test()

if __name__ == "__main__":
  main()
