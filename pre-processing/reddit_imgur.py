__author__ = 'kyedidi'

import json
import pyimgur
import re
from urlparse import urlparse

CLIENT_ID = 'd8645c0ba36315b'
# API_CALLS = 0
im = pyimgur.Imgur(CLIENT_ID)

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
    image_list = [x for x in regex.findall(text) if "/a/" not in x]
    final_list = []
    for image in image_list:
      if image[-4:] == ".jpg" or image[-4:] == ".png" or image[-4:] == ".gif":
        # Make sure you remove the extension
        image = image[:-4]
        # image = image + ".jpg"
      final_list.append(image)
    return final_list

  @staticmethod
  def get_image_page_for_url(url):
    if url[-4:] == ".jpg" or url[-4:] == ".png" or url[-4:] == ".gif":
      # Make sure you remove the extension
      url = url[:-4]

    return url

  @staticmethod
  def get_all_images_for_album(album_url):
    global API_CALLS
    global im
    print "trying to find images for album: ", album_url
    # return []
    # The imgur object is primarily needed to grab the images from an imgur album
    """
    if API_CALLS > 500:
      print "Too many API calls to IMGUR for this hour.. Exiting."
      #return []
      exit()
    """
    # Gets the album id for imgur and then runs with it
    album_id = album_url.split('/')[-1]
    album = None
    try:
      # API_CALLS += 1
      album = im.get_album(album_id)
    except:
      print "***** Was not able to open the album: ", album_url, " with id: ", album_id
      return None
      # return []

    images = []
    if len(album.images) == 0:
      print "The album is empty."
      return []
    for image in album.images:
      # print image.link
      images.append(Imgur.get_image_page_for_url(image.link))
      API_CALLS += 1

    return images

  @staticmethod
  def get_url_for_url_object(u):
    """Returns a url for a url object without the trailing slash"""
    path = u.path if u.path[-1] != '/' else u.path[:-1]
    if len(path) < 5 or len(path) > 14:
      print "ERROR: wrong path for url: ", u, path
      exit()
    return u.scheme + '://' + u.netloc + path

  @staticmethod
  def get_urls_for_possible_urls(possible_urls):
    imgur_urls = []
    imgur_album_urls = []
    for possible_url in possible_urls:
      u = urlparse(possible_url, scheme='http', allow_fragments=True)
      url_path = Imgur.get_url_for_url_object(u)
      if "/a/" in u.path:
        imgur_album_urls.append(url_path)
      else:
        # This is an imgur
        url_path = Imgur.get_image_page_for_url(url_path)

        imgur_urls.append(url_path)
        # TODO: make sure that it's a valid imgur image


      # http://imgur.com/a/RMoR1#0
    return imgur_urls, imgur_album_urls

  @staticmethod
  def get_imgur_urls(text):
    if not text:
      return []
    re_string = "[/:\.\w]*imgur\.com/[/\.\w]+"
    regex = re.compile(re_string, re.IGNORECASE)
    matches = regex.findall(text)
    results = []
    for match in matches:
      if match.count(':') > 1:
        # example: here's the after:http://i.imgur.com/MMcxAnf.jpg?2
        # when there's no space after the colon
        match = match.split(':', 1)[1]
      results.append(match)
    return results
    # return [x for x in re.split('\s|,', text) if "imgur.com" in x]

  @staticmethod
  def load_imgur_information_for_submission(submission):
    # call the above two functions and if there's a response, put it into a json object


    possible_imgur_urls = Imgur.get_imgur_urls(submission.self_text) + Imgur.get_imgur_urls(submission.url)
    # imgur_images = Imgur.get_images_for_possible_urls(possible_imgur_urls)
    imgur_image_urls, imgur_album_urls = Imgur.get_urls_for_possible_urls(possible_imgur_urls)

    imgur_album_image_urls = []
    for imgur_album_url in imgur_album_urls:
       temp_images_for_album = Imgur.get_all_images_for_album(imgur_album_url)
       if temp_images_for_album == None:  # as opposed to empty list
         print "Imgur API is not responding to album requests...... Exiting. "
         print "Was looking up submission: ", submission.to_tuple()
         # I'll just return here, so it can still run
         # With this code flow, we make sure that if we could not successuflly
         # open an album and that contains non album images, we don't save anything
         # ensuring that once we save image info, we have all of it.
         return
         # exit()
       imgur_album_image_urls += temp_images_for_album



    # Images need to be unique
    imgur_images = list(set(imgur_image_urls + imgur_album_image_urls))

    """
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

    """

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