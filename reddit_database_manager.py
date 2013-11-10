
import os.path
import sqlite3

from reddit_submission import Submission

__author__ = 'kyedidi'


class DatabaseManager:
  """ Manages the database. Will create the database if it does not exist. """
  def __init__(self, database_path):
    self.database_path = database_path
    database_exists = os.path.isfile(database_path)
    self.conn = sqlite3.connect(database_path)
    self.rows_written = 0
    self.already_exist = 0
    if not database_exists:
      self.create_db()
    # At this point, the schema should be set-up

  def query(self, query):
    c = self.conn.cursor()
    c.execute(query)
    return c.fetchall()

  def replace_submission(self, submission):
    """ This is a seprate function because this is dangerous"""
    c = self.conn.cursor()
    # print submission.to_tuple()
    c.execute("INSERT OR REPLACE INTO submissions VALUES ("
              "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              submission.to_tuple())
    self.conn.commit()
    self.rows_written += 1
    print "Added a new entry."

  def insert_submission(self, submission, replace_if_exists):
    # Insert a row of data
    if self.row_exists(submission.id):
      # print "Submission with id =", submission.id, "already exists."
      return
    self.replace_submission(submission)


  def row_exists(self, row_id):
    c = self.conn.cursor()
    self.already_exist += 1
    # print "checking for row_id = ", row_id
    c.execute("SELECT * FROM submissions where id = ?", (row_id,))
    return c.fetchone() is not None

  def newest_from_subreddit(self, subreddit):
    # Returns the newest post id from the given subreddit
    pass

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
    # print "Created DB."
