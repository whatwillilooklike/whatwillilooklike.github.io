

import praw
from reddit_submission import Submission

from pprint import pprint

# For PRAW Documentation:
# https://praw.readthedocs.org/en/latest/pages/code_overview.html

__author__ = 'Kapil'



class RedditFetcher:
  def __init__(self, image_manager):
    self.r = praw.Reddit(user_agent='reddit_image_fetcher')
    self.image_manager = image_manager

  def __update_given_submissions(self, submissions):
    for submission in submissions:
      s = Submission.from_reddit_api(submission)
      self.image_manager.insert_submission(s, False)

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
                    'eat', 'eating', 'post', 'journey', 'thong', 'underwear', 'bra',
                    'heaviest', 'ago', 'diet', 'keep', 'approx', 'lifting', 'lift',
                    'pictures', 'between', 'school', 'girl', 'girls',
                    'dedication', 'confidence', 'girl friend', 'boy friend']
    for search_term in search_terms:
      submissions = self.r.search(search_term, subreddit, 'new', None, 'all')
      self.__update_given_submissions(submissions)
      print "Added", self.image_manager.rows_written, "new entries after (new) search for", search_term
      submissions = self.r.search(search_term, subreddit, 'top', None, 'all')
      self.__update_given_submissions(submissions)
      print "Added", self.image_manager.rows_written, "new entries after (top) search for", search_term


    # TODO: get the newest after a submission id
    # r.get_subreddit('python').get_top(limit=None,
    #                                  place_holder=submission.id)


  def update_posts(self):
    #submissions = r.get_subreddit('python').get_top(limit=10)
    subreddits = ['progresspics', 'loseit', 'nakedprogress']
    for subreddit in subreddits:
      self.update_subreddit(subreddit)


