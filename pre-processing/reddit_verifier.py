__author__ = 'kyedidi'
from reddit_database_manager import DatabaseManager
from reddit_submission import Submission

DATABASE_PATH = "reddit_submissions.sqlite"

def main():
  query = 'SELECT * FROM submissions WHERE manually_marked = 0 and ' \
          'manually_verified = 0 and gender IS NOT NULL and age IS NOT NULL and ' \
          'height_in IS NOT NULL and previous_weight_lbs IS NOT NULL and ' \
          'current_weight_lbs IS NOT NULL;'
  m = DatabaseManager(DATABASE_PATH)
  submissions = [Submission(x) for x in m.query(query)]
  for submission in submissions:
    print submission.id
    print "TITLE:", submission.title
    print "CLASSIFICATION: "
    print "gender: ", submission.gender, "age: ", submission.age, "height_in: ", submission.height_in, "previous_weight: ", submission.previous_weight_lbs, "current_weight: ", submission.current_weight_lbs
    """
    submission.gender = r.gender_is_female
      submission.age = r.age
      submission.height_in = r.height_in

      submission.previous_weight_lbs = r.previous_weight
      submission.current_weight_lbs = r.current_weight
      """
    print "----------------------------------------------------------------------------------------"

if __name__ == "__main__":
  main()