__author__ = 'kyedidi'

from reddit_database_manager import DatabaseManager

DATABASE_PATH = "reddit_submissions.sqlite"


def main():
  query = 'SELECT * FROM submissions WHERE author="larissamarie16";'
  m = DatabaseManager(DATABASE_PATH)
  results = m.query(query)
  for result in results:
    print result.to_tuple()


if __name__ == "__main__":
  main()