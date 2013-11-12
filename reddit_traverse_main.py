"""Use this for simple scripts which require DB queries."""

__author__ = 'kyedidi'
import json
import re

from reddit_database_manager import DatabaseManager
from reddit_submission import Submission

DATABASE_PATH = "reddit_submissions.sqlite"



def main():
  """
  query = 'SELECT * FROM submissions WHERE manually_marked = 0 and ' \
          'manually_verified = 0 and gender IS NOT NULL and age IS NOT NULL and ' \
          'height_in IS NOT NULL and current_weight_lbs IS NOT NULL;'
  """
  query = 'SELECT * FROM submissions;'
  m = DatabaseManager(DATABASE_PATH)
  submissions = [Submission(x) for x in m.query(query)]
  #count = 0
  #max_count = 50
  for submission in submissions:

    if submission.self_text:

      print "Title: ", submission.title
      #print "URL: ", submission.url
      #print "selftext: ", submission.self_text
      # print
      # print "imgur urls: "
      print
      # re_string = "\S+imgur\.com/\S+"
      # regex =
      Submission.load_imgur_information_for_submission(submission)
      # print submission.media_json
      m.replace_submission(submission)

  #json_dump_str = Submission.submission_list_to_json(submissions)
  #f = open('json_dump.json', 'w')
  #f.write(json_dump_str)

if __name__ == "__main__":
  main()