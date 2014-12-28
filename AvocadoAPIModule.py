import json
import urllib
import urllib2
import cookielib
import logging
import getpass
import hashlib
import sys

#AvocadoAPI class is used for communicating with the Avocado API
class AvocadoAPI(object):
  def __init__(self, config_parser, user_agent, auth_client):
    self.configuration = config_parser
    self.user_agent = user_agent
    self.authentication = auth_client

  def build_api_url(self, requested_url, ID = None, action = None):
    api_url = URLlib.base + requested_url
    if ID is not None:
      api_url = api_url + "/" + ID
    if action is not None:
      if ID is None:
        print "URL Builder: You have passed in an action but no object ID."
      else:
        api_url = api_url + "/" + action
    return api_url

  def authenticate(self):
   self.authentication.populate_values_from_config()
   self.authentication.update_signature()
   if self.authentication.dev_signature is None:
    print "Authentication Failed."
    sys.exit(0)
   else:
    print "Authentication Succeeded."

  def test_api_communication(self):
   try:
     couple = self.get_couple()
   except:
     print "Something went wrong."
     print "- If authentication succeeded but the request was unsigned, check the Dev ID and Dev Key in config.ini as they do not match."
     sys.exit(0)
   
   if couple is None:
     print "Couldn't get Couple information."
   else:   
     print "Couple information was successfully retrieved."

  def get_couple(self):
   couple_page = self.build_api_url(URLlib.couple)
   return json.load(self.get_request(couple_page));
  
  def get_list_of_lists(self):
   lists_page = self.build_api_url(URLlib.lists)
   return json.load(self.get_request(lists_page));

  def get_list(self, listID):
   list_page = self.build_api_url(URLlib.lists, listID)
   return json.load(self.get_request(list_page));
   
  def get_listname(self):
    listname = self.configuration.get('Avocado Information', 'List Name')
    if listname is "":
        logging.error('List Name is missing from config.ini')
        sys.exit(0)
    else:
      return listname

  # def return_api_json(self, requested_page):
    # try:
      # cookies = cookielib.CookieJar()
      # request = urllib2.Request(
        # url = requested_page,
        # headers = {
          # "Content-type": "application/x-www-form-urlencoded",
          # "User-Agent": self.user_agent,
          # "X-AvoSig": self.authentication.dev_signature,
          # }
      # )
      # request.add_header('Cookie',
        # '%s=%s' % (self.authentication.cookie_name, self.authentication.cookie_value))
      # json_object = urllib2.urlopen(request);

    # except urllib2.URLError, e:
      # logging.error(e.read())
    
    # if json_object is None:
      # print "There was a problem."
    # else:
      # return json_object

  def get_list_ID_by_name(self, lists, listname):
    i = 0
    for item in lists:
      if item["name"] == listname:
        ID = item["id"]
        i = i + 1
        #print ID
    if i <> 1 :
      print "No list with the name " + listname + "."
      sys.exit(0)
    else:
      return ID

  def get_request(self, requested_page):
    try:
      cookies = cookielib.CookieJar()
      request = urllib2.Request(
        url = requested_page,
        headers = {
          "Content-type": "application/x-www-form-urlencoded",
          "User-Agent": self.user_agent,
          "X-AvoSig": self.authentication.dev_signature,
          }
      )
      request.add_header('Cookie',
        '%s=%s' % (self.authentication.cookie_name, self.authentication.cookie_value))
      response = urllib2.urlopen(request);

    except urllib2.URLError, e:
      logging.error(e.read())

    return response

  def post_request(self, parameters, requested_url):
    params = urllib.urlencode(parameters)
    try:
      cookies = cookielib.CookieJar()
      request = urllib2.Request(
        url = requested_url,
        data = params,
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "User-Agent": self.user_agent,
            "X-AvoSig": self.authentication.dev_signature,
            }
        )
      request.add_header('Cookie',
        '%s=%s' % (self.authentication.cookie_name, self.authentication.cookie_value))
      response = urllib2.urlopen(request)

    except urllib2.URLError, e:
      logging.error(e.read())

    return response

#URLlib is used for storing URL information for accessing the AvocadoAPI
class URLlib(object):
    base = "https://avocado.io/api/"
    login = 'authentication/login'
    couple = 'couple'
    lists = 'lists'

#AuthClient is used to manage authentication to Avocado
class AuthClient(object):
  def __init__(self, config_parser, user_agent):
    self.configuration = config_parser
    self.email = None
    self.password = None
    self.dev_id = 0
    self.dev_key = None
    self.dev_signature = None
    self.cookie_name = None
    self.cookie_value = None
    self.user_agent = user_agent

  def populate_values_from_config(self):
      self.email = self.configuration.get('Avocado Authentication', 'Email')
      if self.email is "":
        logging.error('Email is missing from config.ini')
        sys.exit(0)
      
      self.password = self.configuration.get('Avocado Authentication', 'Password')
      if self.password is "":
        logging.error('Password is missing from config.ini')
        sys.exit(0)
      
      try:
        self.dev_id = self.configuration.get_int('Avocado Authentication', 'Developer ID')
      except:
        logging.error('Dev ID is missing from config.ini')
        sys.exit(0)
      
      self.dev_key = self.configuration.get('Avocado Authentication', 'Developer Key')
      if self.dev_key is "":
        logging.error('Dev Key is missing from config.ini')
        sys.exit(0)

      self.cookie_name = self.configuration.get('Avocado Authentication', 'Avocado Cookie Name')
      if self.cookie_name is "":
        logging.error('Cookie Name is missing from config.ini')
        sys.exit(0)

  def get_cookie_from_login(self):
    params = urllib.urlencode({
      "email": self.email,
      "password": self.password,
    })
    try:
      request = urllib2.Request(
        url = URLlib.base + URLlib.login,
        data = params,
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "User-Agent": self.user_agent
            }
        )
      response = urllib2.urlopen(request)

      cookies = cookielib.CookieJar()
      cookies.extract_cookies(response, request)
      for cookie in cookies:
          if cookie.name == self.cookie_name:
               self.cookie_value = cookie.value
               break
    except urllib2.URLError, e:
      logging.error(e.read())

  def hash_signature(self):
    hasher = hashlib.sha256()
    hasher.update(self.cookie_value + self.dev_key)
    self.dev_signature = '%d:%s' % (self.dev_id, hasher.hexdigest())

  def update_signature(self):
    self.get_cookie_from_login()
    if self.cookie_value is not None:
      self.hash_signature()


#List is used to store the information about the list the application uses
class List(object):
  @staticmethod
  def convert_to_python_list(jsonlist, listID, listname):
    pythonlist = List(listname, listID)
    pythonlist.listitems = []
    for item in jsonlist['items']:
      pythonlistitem = ListItem.build_listitem_from_json(item)
      pythonlist.listitems.append(pythonlistitem)
    return pythonlist

  def __init__(self, listname, listID = None):
    self.listID = listID
    self.listname = listname
    self.listitems = None

  def delete_from_avocado(self, AvocadoAPI):
    requested_url = AvocadoAPI.build_api_url(URLlib.lists, self.listID, 'delete')
    parameters = {}
    response = json.load(AvocadoAPI.post_request(parameters, requested_url))
    print "Deletion response: " + response

  def create_in_avocado(self, AvocadoAPI):
    requested_url = AvocadoAPI.build_api_url(URLlib.lists)
    parameters = {'name': self.listname,}
    response = json.load(AvocadoAPI.post_request(parameters, requested_url))
    self.listID = response['id']


#ListItem is used to store the items from the list in an accessible form
class ListItem(object):
  @staticmethod
  def build_listitem_from_json(jsonlistitem):
    notetext = jsonlistitem.get('text', None)
    complete = jsonlistitem.get('complete', False)
    important = jsonlistitem.get('important', False)
    userId = jsonlistitem.get('userId', None)
    updateTime = jsonlistitem.get('updateTime', None)
    
    pythonlistitem = ListItem(notetext, complete, important, userId, updateTime)
    return pythonlistitem
  
  def __init__(self, notetext, complete = False, important = False, userId = None, updateTime = None):
    self.text = notetext
    self.complete = complete
    self.important = important
    self.userId = userId
    self.updateTime = updateTime
    self.itemID = None

  def create_in_avocado(self, AvocadoAPI, listID):
    requested_url = AvocadoAPI.build_api_url(URLlib.lists, listID)
    parameters = {'text': self.text,}
    response = json.load(AvocadoAPI.post_request(parameters, requested_url))
    self.itemID = response['id']

  def update_in_avocado(self, AvocadoAPI, listID):
    requested_url = AvocadoAPI.build_api_url(URLlib.lists, listID + "/" + self.itemID)
    parameters = {'important': self.important,}
    response = json.load(AvocadoAPI.post_request(parameters, requested_url))