import json

__author__ = 'kyedidi'


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
    # TODO: rename gender to gender_is_female and don't keep gender
    # and adult_content as integers. Keep them as boolean internally
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
  def submission_list_to_json(submissions):
    final_result = {}
    result = []
    for submission in submissions:
      media_embed_json = None if submission.media_embed_json is None else json.loads(submission.media_embed_json)
      media_json = None if submission.media_json is None else json.loads(submission.media_json)
      py_obj = {
        'id': submission.id,
        'title': submission.title,
        'current_weight_lbs': submission.current_weight_lbs,
        'previous_weight_lbs': submission.previous_weight_lbs,
        'gender': bool(submission.gender),
        'height_in': submission.height_in,
        'age': submission.age,
        'score': submission.score,
        'adult_content': bool(submission.adult_content),
        'media_embed_json': media_embed_json,
        'media_json': media_json,
        'url': submission.url,
        'permalink': submission.permalink
      }
      result.append(py_obj)
    final_result['result'] = result
    return json.dumps(final_result)

  @staticmethod
  def from_reddit_api(r):
    # TODO: submission is not being set properly
    selftext = None if not r.selftext else r.selftext
    # media = None if not r.media else json.dumps(r.media)
    media_embed = None  # useless feild now
    # media_embed = None if not r.media_embed else json.dumps(r.media_embed)
    url = None if not r.url else r.url
    author_name = "unknown" if not r.author else r.author.name

    # NOTE: media is just being set to None because I'll set it myself after
    # looking through the file
    submission_tuple = (r.id, 0, 0, r.title, selftext, None, None, None, None,
                        None, None, r.score, int(r.over_18), media_embed, None,
                        author_name, r.created, r.subreddit.display_name,
                        url, r.permalink)
    s = Submission(submission_tuple)
    # Moved the code below to reddit_imgur_main.py
    # Imgur.load_imgur_information_for_submission(s)
    # print s
    return s

  def to_tuple(self):
    # returns a tuple representation of the submission
    return (self.id, self.manually_verified, self.manually_marked, self.title,
            self.self_text, self.current_weight_lbs, self.previous_weight_lbs,
            self.height_in, self.gender, self.age, self.duration_days, self.score,
            self.adult_content, self.media_embed_json, self.media_json, self.author,
            self.created, self.subreddit, self.url, self.permalink)


