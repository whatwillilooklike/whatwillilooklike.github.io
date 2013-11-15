"""Use this for simple scripts which require DB queries."""

__author__ = 'kyedidi'


from reddit_database_manager import DatabaseManager
from reddit_submission import Submission
from reddit_imgur import Imgur

DATABASE_PATH = "reddit_submissions.sqlite"



def main():
  """
  query = 'SELECT * FROM submissions WHERE manually_marked = 0 and ' \
          'manually_verified = 0 and gender IS NOT NULL and age IS NOT NULL and ' \
          'height_in IS NOT NULL and current_weight_lbs IS NOT NULL;'
  """
  query = 'SELECT * FROM submissions WHERE media_json IS NULL;'
  # query = 'SELECT * FROM submissions;'
  m = DatabaseManager(DATABASE_PATH)
  submissions = [Submission(x) for x in m.query(query)]
  #count = 0
  #max_count = 50
  for submission in submissions:
    #submission.media_json = None
    #submission.media_embed_json = None
    Imgur.load_imgur_information_for_submission(submission)
    m.replace_submission(submission)

  #json_dump_str = Submission.submission_list_to_json(submissions)
  #f = open('json_dump.json', 'w')
  #f.write(json_dump_str)

if __name__ == "__main__":
  main()