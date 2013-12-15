__author__ = 'kyedidi'

from reddit_analyzer import RedditAnalyzer, HITS_stats
from blessings import Terminal
t = Terminal()


def test_weight_2():
  title = """27 [M] 5'11" - 250 to 205 lbs - 3 months."""
  self_text = ""
  r = RedditAnalyzer(title, self_text)
  r.search_slash_delimited(title)

  return


def test_weight_1():

  title = """27 [M] 5'11" - 250 to 205 lbs - 3 months."""
  self_text = """
  In the two years after graduating high school, I packed on nearly 100 pounds. For the past 6 or 7 years, I've been in the 250+lbs. range and I wanted to change it so very badly, but never could. I changed that at the beginning of this year, and wanted to share [my progress.](http://i.imgur.com/JcuvVXh.jpg)

This has all been through healthy eating with a plan of my own creation. I've got another 15 pounds to go before I hit my first weight goal, and I'll start exercising at that point to shape up whatever I'm working with at that point. I'm hoping to be there by June, so I'll report back around that time.
  """


  r = RedditAnalyzer(title, self_text)



  # Start Print statements
  if r.has_gender() and r.has_height() and not r.has_current_weight():
    print "Title: ", title
    print "Self text: ", self_text
    # submission.manually_verified

    # search_slash_delimited

    #exit()
    print
    # Later, we can work on the selftext
    #text = nltk.word_tokenize("And now for something completely different")
    #text2 = nltk.word_tokenize(submission.title)
    #print nltk.pos_tag(text2)

    print t.bold(t.red("CLASSIFICATION: " + r.get_debug_str()))
    print t.bold(t.red("LOW CONFIDENCE CLASSIFICATION: " + r.get_lc_debug_str()))

def main():
  # test_weight_1()
  test_weight_2()

if __name__ == "__main__":
  main()