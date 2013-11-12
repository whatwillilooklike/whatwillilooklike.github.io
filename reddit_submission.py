import json
import re

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
  def __get_imgur_albums(text):
    """Returns a list of imgur albums given in the text"""
    if not text:
      return []
    re_string = "[/:\.\w]*imgur\.com/a/\w+"
    regex = re.compile(re_string, re.IGNORECASE)
    return regex.findall(text)

  @staticmethod
  def __get_imgur_images(text):
    """Returns a list of imgur images given in the text"""
    if not text:
      return []
    re_string = "[/:\.a-zA-z]*imgur\.com/[/:\.\w]+"  # TODO: need to exclude the /a/ (albums)
    regex = re.compile(re_string, re.IGNORECASE)
    image_list = [x for x in regex.findall(text) if "a/" not in x]
    final_list = []
    for image in image_list:
      if image[-4:] != ".jpg" and image[-4:] != ".png" and image[-4:] != ".gif":
        image = image + ".jpg"
      final_list.append(image)
    return final_list

  @staticmethod
  def load_imgur_information_for_submission(submission):
    # call the above two functions and if there's a response, put it into a json object
    imgur_albums_set = set()
    imgur_albums_in_self_text = Submission.__get_imgur_albums(submission.self_text)
    for imgur_album in imgur_albums_in_self_text:
      imgur_albums_set.add(imgur_album)
    imgur_albums_in_url = Submission.__get_imgur_albums(submission.url)
    for imgur_album in imgur_albums_in_url:
      imgur_albums_set.add(imgur_album)

    imgur_albums = list(imgur_albums_set)

    imgur_images_set = set()
    imgur_images_in_self_text = Submission.__get_imgur_images(submission.self_text)
    for imgur_image in imgur_images_in_self_text:
      imgur_images_set.add(imgur_image)
    imgur_images_in_url = Submission.__get_imgur_images(submission.url)
    for imgur_image in imgur_images_in_url:
      imgur_images_set.add(imgur_image)

    imgur_images = list(imgur_images_set)

    json_obj = {}
    if imgur_albums:
      json_obj['imgur_albums'] = imgur_albums
    if imgur_images:
      json_obj['imgur_images'] = imgur_images

    if len(json_obj) == 0:
      submission.media_json = None
      return

    json_str = json.dumps(json_obj)
    submission.media_json = json_str
    return

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
    media = None if not r.media else json.dumps(r.media)
    media_embed = None if not r.media_embed else json.dumps(r.media_embed)
    url = None if not r.url else r.url
    author_name = "unknown" if not r.author else r.author.name

    # NOTE: media is just being set to None because I'll set it myself after
    # looking through the file
    submission_tuple = (r.id, 0, 0, r.title, selftext, None, None, None, None,
                        None, None, r.score, int(r.over_18), media_embed, None,
                        author_name, r.created, r.subreddit.display_name,
                        url, r.permalink)
    s = Submission(submission_tuple)
    Submission.load_imgur_information_for_submission(s)
    # print s
    return s

  def to_tuple(self):
    # returns a tuple representation of the submission
    return (self.id, self.manually_verified, self.manually_marked, self.title,
            self.self_text, self.current_weight_lbs, self.previous_weight_lbs,
            self.height_in, self.gender, self.age, self.duration_days, self.score,
            self.adult_content, self.media_embed_json, self.media_json, self.author,
            self.created, self.subreddit, self.url, self.permalink)


