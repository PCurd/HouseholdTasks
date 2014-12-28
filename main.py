from ConfigModule import Config
from UserModule import Couple
from AvocadoAPIModule import AvocadoAPI
from AvocadoAPIModule import AuthClient
from AvocadoAPIModule import List
from AvocadoAPIModule import ListItem
from AvocadoAPIModule import URLlib
import logging
import datetime
import json

#Initialise config & logging
logging.basicConfig(level=logging.DEBUG)
configuration = Config("config.ini")
avocado_user_agent = configuration.get('Avocado Requests', 'Avocado User Agent')
app_avocado_list_name = configuration.get('Avocado Information', 'List Name')

#Authenticate with Avocado
api = AvocadoAPI(configuration, avocado_user_agent, AuthClient(configuration, avocado_user_agent))
api.authenticate()

#Get couple names and user IDs
couple = api.get_couple()
couple = Couple.convert_to_python_couple(couple)

#Get the list belonging to the app
list_of_lists = api.get_list_of_lists()
listname = api.get_listname()
listID = api.get_list_ID_by_name(list_of_lists, listname)
oldlist = api.get_list(listID)
oldlist = List.convert_to_python_list(oldlist, listID, listname)

#Check list items to find any that have been marked as complete
items_to_update = []
for item in oldlist.listitems:
  if item.complete == True:
    items_to_update.append(item)

for item in items_to_update:
  print "\n - item:"
  print "Item Text: " + item.text
  print "Completed by ID: " + item.userId
  print "Completed by First Name: " + couple.get_first_name_by_ID(item.userId)
  print "Completed at: " + (datetime.datetime.fromtimestamp(int(item.updateTime/1000)).strftime('%Y-%m-%d %H:%M:%S'))
  
#Pass items_to_update off to db

#Receive lists of items to be added back to the main list
overdue_items = []
overdue_items.append(ListItem('Overdue Item #1', important = 1))
overdue_items.append(ListItem('Overdue Item #2', important = 1))
overdue_items.append(ListItem('Overdue Item #3', important = 1))
overdue_items.append(ListItem('Overdue Item #4', important = 1))

due_items = []
due_items.append(ListItem('Due Item #1', important = 0))
due_items.append(ListItem('Due Item #2', important = 0))
due_items.append(ListItem('Due Item #3', important = 0))

# delete the old list
oldlist.delete_from_avocado(api)

# #create the new list
newlist = List(listname)
newlist.listitems = []
for item in overdue_items:
  newlist.listitems.append(item)
for item in due_items:
  newlist.listitems.append(item)

newlist.create_in_avocado(api)

for item in newlist.listitems:
  item.create_in_avocado(api, newlist.listID)
  item.update_in_avocado(api, newlist.listID)

print "Done."