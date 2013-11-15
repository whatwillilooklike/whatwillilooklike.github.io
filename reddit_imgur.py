__author__ = 'kyedidi'

import json
import pyimgur
import re

CLIENT_ID = 'c1a3920d783f7ea'

class Imgur:

  def __init__(self):

    pass


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
      if image[-4:] == ".jpg" or image[-4:] == ".png" or image[-4:] == ".gif":
        # Make sure you remove the extension
        image = image[:-4]
        # image = image + ".jpg"
      final_list.append(image)
    return final_list

  @staticmethod
  def get_all_images_for_album(album_url):
    # The imgur object is primarily needed to grab the images from an imgur album
    im = pyimgur.Imgur(CLIENT_ID)
    # Gets the album id for imgur and then runs with it
    album_id = album_url.split('/')[-1]
    album = im.get_album(album_id)

    images = []
    for image in album.images:
      print image.link
      images.append(image.link)

    return images

  @staticmethod
  def load_imgur_information_for_submission(submission):
    # call the above two functions and if there's a response, put it into a json object
    imgur_images_set = set()

    imgur_albums_set = set()
    imgur_albums_in_self_text = Imgur.__get_imgur_albums(submission.self_text)
    for imgur_album in imgur_albums_in_self_text:
      imgur_albums_set.add(imgur_album)
    imgur_albums_in_url = Imgur.__get_imgur_albums(submission.url)
    for imgur_album in imgur_albums_in_url:
      imgur_albums_set.add(imgur_album)

    imgur_albums = list(imgur_albums_set)

    for album_url in imgur_albums:
      imgur_images_in_album = Imgur.get_all_images_for_album(album_url)
      for imgur_image in imgur_images_in_album:
        imgur_images_set.add(imgur_image)


    imgur_images_in_self_text = Imgur.__get_imgur_images(submission.self_text)
    for imgur_image in imgur_images_in_self_text:
      imgur_images_set.add(imgur_image)
    imgur_images_in_url = Imgur.__get_imgur_images(submission.url)
    for imgur_image in imgur_images_in_url:
      imgur_images_set.add(imgur_image)

    imgur_images = list(imgur_images_set)

    json_obj = {}
    #if imgur_albums:
    #  json_obj['imgur_albums'] = imgur_albums
    if imgur_images:
      json_obj['imgur_images'] = imgur_images

    if len(json_obj) == 0:
      submission.media_json = None
      return

    json_str = json.dumps(json_obj)
    submission.media_json = json_str
    return