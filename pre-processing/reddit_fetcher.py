

import praw
from reddit_submission import Submission
from reddit_database_manager import DatabaseManager
from pprint import pprint
import time
from secret import REDDIT_USER_AGENT

# For PRAW Documentation:
# https://praw.readthedocs.org/en/latest/pages/code_overview.html

__author__ = 'Kapil'

DATABASE_PATH = "reddit_submissions.sqlite"
m = DatabaseManager(DATABASE_PATH)

class RedditFetcher:
  def __init__(self, image_manager):
    self.r = praw.Reddit(user_agent=REDDIT_USER_AGENT)
    self.image_manager = image_manager

  def __update_given_submissions(self, submissions):
    for submission in submissions:
      if not self.image_manager.row_exists(submission.id):
        s = Submission.from_reddit_api(submission)
        self.image_manager.insert_submission(s)
      else:
        # if submission does exist, update its score
        new_submission = Submission.from_reddit_api(submission)
        # existing_submission =
        query = 'SELECT * FROM submissions WHERE id = "%s";' % submission.id
        existing_submissions = [Submission(x) for x in m.query(query)]
        assert(len(existing_submissions) == 1)
        existing_submission = existing_submissions[0]
        if existing_submission.score != new_submission.score:
          #print "NEW_SUBMISSION: ", new_submission.to_tuple()
          #print "BEFORE: ", existing_submission.to_tuple()
          existing_submission.score = new_submission.score
          #print "AFTER: ", existing_submission.to_tuple()
          #time.sleep(5)
          m.replace_submission(existing_submission)

  def update_subreddit(self, subreddit):
    # get_hot
    submissions = self.r.get_subreddit(subreddit).get_hot(limit=1000)
    self.__update_given_submissions(submissions)
    print "Added", self.image_manager.rows_written, "new entries after get_subreddit (get_hot)."
    # get_new
    submissions = self.r.get_subreddit(subreddit).get_new(limit=1000)
    self.__update_given_submissions(submissions)
    print "Added", self.image_manager.rows_written, "new entries after get_subreddit (get_new)."
    # get_rising
    submissions = self.r.get_subreddit(subreddit).get_rising(limit=1000)
    self.__update_given_submissions(submissions)
    print "Added", self.image_manager.rows_written, "new entries after get_subreddit (get_rising)."
    # get_controversial
    submissions = self.r.get_subreddit(subreddit).get_controversial(limit=1000)
    self.__update_given_submissions(submissions)
    print "Added", self.image_manager.rows_written, "new entries after get_subreddit (get_controversial)."
    # get_top
    submissions = self.r.get_subreddit(subreddit).get_top(limit=1000)
    self.__update_given_submissions(submissions)
    print "Added", self.image_manager.rows_written, "new entries after get_subreddit (get_top)."

    search_terms = ['pounds', 'lost', 'm', 'f', 'lbs', 'progress', 'pics',
                    'down', 'shape', 'starting', 'hoping', 'start', 'weight',
                    'goal', 'NSFW', 'month', 'lose', 'gain', 'keto', 'bf', 'gf',
                    '22', 'year','f/','m/', 'body', 'transformation', 'my',
                    'face', 'week', 'weeks', 'jeans', 'shorts', 'fit', 'finally',
                    'diet', 'exercise', 'abs', 'tummy', 'stomach', 'slow',
                    'happy', 'huge', 'start', 'years', 'training', 'ladies',
                    'difference', 'support', 'proud', 'muscle', 'feeling',
                    'highest', 'getting', 'mo', 'achieved', 'realize', 'far',
                    'long', 'bikini', 'guys', 'conscious', 'photos',
                    'carb', 'waist', 'maintain', 'kept', 'proof', 'anyone', 'size',
                    'eat', 'eating', 'post', 'journey', 'went', 'down',
                    'heaviest', 'ago', 'diet', 'keep', 'approx', 'lifting', 'lift',
                    'pictures', 'between', 'school', 'girl', 'girls',
                    'dedication', 'confidence', 'girl friend', 'boy friend',
                    'bulimia', 'anorexia', 'fat', 'thin', 'skinny', 'lean',
                    'abs', 'biceps', 'back', 'reddit']
    for search_term in search_terms:
      submissions = self.r.search(search_term, subreddit, 'new', None, 'all')
      self.__update_given_submissions(submissions)
      print "Added", self.image_manager.rows_written, "new entries after (new) search for", search_term
      submissions = self.r.search(search_term, subreddit, 'top', None, 'all')
      self.__update_given_submissions(submissions)
      print "Added", self.image_manager.rows_written, "new entries after (top) search for", search_term

    # TODO: add all posts by all the users in the given subreddits



    # TODO: get the newest after a submission id
    # r.get_subreddit('python').get_top(limit=None,
    #                                  place_holder=submission.id)


  def update_posts(self):
    #submissions = r.get_subreddit('python').get_top(limit=10)
    subreddits = ['progresspics', 'loseit', 'nakedprogress', 'brogress', 'keto', 'gainit']
    for subreddit in subreddits:
      self.update_subreddit(subreddit)


