__author__ = 'kyedidi'


from reddit_database_manager import DatabaseManager
from reddit_fetcher import RedditFetcher

DATABASE_PATH = "reddit_submissions.sqlite"

def main():
  #r = praw.Reddit('Search post info example by u/_Daimon')
  #help(r.search)
  #exit()
  image_manager = DatabaseManager(DATABASE_PATH)

  # Example submission tuple:
  # submission_tuple = ('id', 1, 1, 'Title', 'Self text', 160, 190, 69, 0, 22, 100, 538, 0,
  #                     'media_embed_json', 'media_json', 'author', 123456789, 'subreddit',
  #                     'url', 'permalink')
  # s = Submission(submission_tuple)
  # image_manager.insert_submission(s, False)

  # PRAW Stuff
  f = RedditFetcher(image_manager)
  f.update_posts()
  print "Added", image_manager.rows_written, "new entries total."
  print "Found", image_manager.already_exist, "that already exist."



if __name__ == "__main__":
  main()