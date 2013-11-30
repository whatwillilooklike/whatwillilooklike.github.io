__author__ = 'kyedidi'

__author__ = 'kyedidi'
from reddit_database_manager import DatabaseManager
from reddit_submission import Submission

DATABASE_PATH = "reddit_submissions.sqlite"

def main():
  query = 'SELECT * FROM submissions WHERE ' \
          'manually_verified = 0 and gender IS NOT NULL and ' \
          'height_in IS NOT NULL and current_weight_lbs IS NOT NULL and media_json IS NOT NULL;'
  m = DatabaseManager(DATABASE_PATH)
  submissions = [Submission(x) for x in m.query(query)]
  json_dump_str = Submission.submission_list_to_json(submissions)
  f = open('json_dump.json', 'w')
  f.write(json_dump_str)

if __name__ == "__main__":
  main()