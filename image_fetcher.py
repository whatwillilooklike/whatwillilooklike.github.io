import json
import os.path
import praw
import sqlite3

from pprint import pprint

__author__ = 'Kapil'

DATABASE_PATH = "reddit_submissions.sqlite"

class Submission:
  def __init__(self, submission_tuple):
    self.id = submission_tuple[0]
    self.manually_verified = submission_tuple[1]
    self.manually_marked = submission_tuple[2]
    self.title = submission_tuple[3]
    self.self_text = submission_tuple[4]
    self.current_weight_lbs = submission_tuple[5]
    self.previous_weight_lbs = submission_tuple[6]
    self.height_in = submission_tuple[7]
    self.gender = submission_tuple[8]
    self.age = submission_tuple[9]
    self.duration_days = submission_tuple[10]
    self.score = submission_tuple[11]
    self.adult_content = submission_tuple[12]
    self.media_embed_json = submission_tuple[13]
    self.media_json = submission_tuple[14]
    self.author = submission_tuple[15]
    self.created = submission_tuple[16]
    self.subreddit = submission_tuple[17]
    self.url = submission_tuple[18]
    self.permalink = submission_tuple[19]

  @staticmethod
  def from_reddit_api(r):
    # TODO: submission is not being set properly
    selftext = None if not r.selftext else r.selftext
    media = None if not r.media else json.dumps(r.media)
    media_embed = None if not r.media_embed else json.dumps(r.media_embed)
    url = None if not r.url else r.url

    submission_tuple = (r.id, 0, 0, r.title, selftext, None, None, None, None,
                        None, None, r.score, int(r.over_18), media_embed, media,
                        r.author.name, r.created, r.subreddit.display_name,
                        url, r.permalink)
    s = Submission(submission_tuple)
    print s
    return s

  def to_tuple(self):
    # returns a tuple representation of the submission
    return (self.id, self.manually_verified, self.manually_marked, self.title,
            self.self_text, self.current_weight_lbs, self.previous_weight_lbs,
            self.height_in, self.gender, self.age, self.duration_days, self.score,
            self.adult_content, self.media_embed_json, self.media_json, self.author,
            self.created, self.subreddit, self.url, self.permalink)



class ImageManager:
  """ Manages the database. Will create the database if it does not exist. """
  def __init__(self, database_path):
    self.database_path = database_path
    database_exists = os.path.isfile(database_path)
    self.conn = sqlite3.connect(database_path)
    if not database_exists:
      self.create_db()
    # At this point, the schema should be set-up

  def insert_submission(self, submission, replace_if_exists):
    # Insert a row of data
    c = self.conn.cursor()
    if self.row_exists(submission.id) and not replace_if_exists:
      print "Submission with id =", submission.id, "already exists."
      return

    # TODO: handle care when replace_if_exists = True
    # print submission.to_tuple()
    c.execute("INSERT INTO submissions VALUES ("
              "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              submission.to_tuple())
    self.conn.commit()

  def row_exists(self, row_id):
    c = self.conn.cursor()
    print "checking for row_id = ", row_id
    c.execute("SELECT * FROM submissions where id = ?", (row_id,))
    return c.fetchone() is not None

  def create_db(self):
    c = self.conn.cursor()
    c.execute("""
    CREATE TABLE "submissions" (
      "id" text NOT NULL,
      "manually_verified" integer NOT NULL,
      "manually_marked" integer NOT NULL,
      "title" text NOT NULL,
      "selftext" text,
      "current_weight_lbs" integer,
      "previous_weight_lbs" integer,
      "height_in" integer,
      "gender" integer,
      "age" integer,
      "duration_days" integer,
      "score" integer NOT NULL,
      "adult_content" integer NOT NULL,
      "media_embed_json" text,
      "media_json" text,
      "author" text NOT NULL,
      "created" integer NOT NULL,
      "subreddit" text NOT NULL,
      "url" text,
      "permalink" text NOT NULL,
      PRIMARY KEY("id")
    );
    """)
    self.conn.commit()
    print "Created DB."

class RedditFetcher:
  def __init__(self):
    self.r = praw.Reddit(user_agent='reddit_image_fetcher')

  def update_posts(self, image_manager):
    #submissions = r.get_subreddit('python').get_top(limit=10)

    submissions = self.r.get_subreddit('progresspics').get_hot(limit=200)
    for submission in submissions:
      # print "got submission"
      # pprint(vars(submission))
      if submission.media or submission.media_embed:
        s = Submission.from_reddit_api(submission)
        print "Media: ", json.dumps(submission.media)
        print "Media Dumps:", json.dumps(submission.media_embed)
        print s.to_tuple()
        # exit()
        # pprint(vars(submission))
        # print s.to_tuple()
        image_manager.insert_submission(s, False)
        exit()
        # pprint(vars(submission))
    # print submissions
    #print [str(x) for x in submissions]

def main():
  image_manager = ImageManager(DATABASE_PATH)

  submission_tuple = ('id', 1, 1, 'Title', 'Self text', 160, 190, 69, 0, 22, 100, 538, 0,
                      'media_embed_json', 'media_json', 'author', 123456789, 'subreddit',
                      'url', 'permalink')
  s = Submission(submission_tuple)
  image_manager.insert_submission(s, False)

  # PRAW Stuff
  f = RedditFetcher()
  f.update_posts(image_manager)




if __name__ == "__main__":
  main()