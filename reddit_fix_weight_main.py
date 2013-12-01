__author__ = 'kyedidi'

from reddit_database_manager import DatabaseManager
from reddit_submission import Submission
from reddit_imgur import Imgur
import time
DATABASE_PATH = "reddit_submissions.sqlite"

""" Clears (sets NULL) analysis / calculated features for given ID."""

def main():
  """
  query = 'SELECT * FROM submissions WHERE manually_marked = 0 and ' \
          'manually_verified = 0 and gender IS NOT NULL and age IS NOT NULL and ' \
          'height_in IS NOT NULL and current_weight_lbs IS NOT NULL;'
  """
  submission_id = raw_input("Enter submission id to enter weight manually: ")
  query = 'SELECT * FROM submissions WHERE id = "%s";' % submission_id
  # query = 'SELECT * FROM submissions;'
  m = DatabaseManager(DATABASE_PATH)
  submissions = [Submission(x) for x in m.query(query)]
  #count = 0
  #max_count = 50
  assert(len(submissions) == 1)

  previous_weight = int(raw_input("Enter previous weight: "))
  current_weight = int(raw_input("Enter current weight: "))

  for submission in submissions:
    #submission.media_json = None
    #submission.media_embed_json = None

    print "Title: ", submission.title
    print "Selftext: ", submission.self_text
    print "URL: ", submission.url
    print "Media JSON: ", submission.media_json
    # print json_str
    print "--------------------------------------------------------------------------------"

    submission.manually_verified = 1
    submission.manually_marked = 1
    submission.previous_weight_lbs = previous_weight
    submission.current_weight_lbs = current_weight
    m.replace_submission(submission)

  #json_dump_str = Submission.submission_list_to_json(submissions)
  #f = open('json_dump.json', 'w')
  #f.write(json_dump_str)

if __name__ == "__main__":
  while True:
    main()
