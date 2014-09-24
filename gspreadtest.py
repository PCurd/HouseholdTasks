#!/usr/bin/python

import gspread
from oauth2client.client import SignedJwtAssertionCredentials

import logging
logging.basicConfig(filename='debug.log',level=logging.DEBUG)



class TodoItem(object):
    """An instance of this class represents a single row
    of a todo task.

    """
    def __init__(self):
        #self.element = element
        #cell_elem = element.find(_ns1('cell'))
        #self._row = int(cell_elem.get('row'))
        #self._col = int(cell_elem.get('col'))
        #self.input_value = cell_elem.get('inputValue')
        
        self._task = ''
        self._frequency = ''
        self._whenlast = ''
        self._wholast = ''
        self._whennext = ''
        self._overdue = ''
        self._whonormallydoes = ''
        self._howoftenarewedoingit = ''


        #: Value of the cell.
        self.value = ''

    @property
    def Task(self):
        """Task title"""
        return self._task

    @property
    def Frequency(self):
        """Task when last done"""
        return self._frequency

    @property
    def WhenWasItLastDone(self):
        """Task title"""
        return self._whenlast

    @property
    def WhoLastDidIt(self):
        """Task title"""
        return self._wholast        
        
    @property
    def WhenIsItNextDue(self):
        """Task title"""
        return self._whennext

    @property
    def Overdue(self):
        """Task title"""
        return self._overdue

    @property
    def WhoNormallyDoes(self):
        """Task title"""
        return self._whonormallydoes

    @property
    def HowOftenAreWeDoingIt(self):
        """Task title"""
        return self._howoftenarewedoingit        
        
        
    def ParseDictionary(self, dict):
      self._task=dict['Task']
      self._frequency = dict['Frequency']
      self._whenlast = dict['When it was last done']
      self._wholast = dict['Who last did it']
      self._whennext = dict['When it is next due']
      self._overdue = dict['Overdue?']
      self._whonormallydoes = dict['Who normally does it?']
      self._howoftenarewedoingit = dict['How often are we doing it?']
      
    def PrintItem(self):
      print '%s %s' % ('Task:', self.Task)
      print '%s %s' % ('Frequency:', self.Frequency)
      print '%s %s' % ('When it was last done:', self.WhenWasItLastDone)
      print '%s %s' % ('Who last did it:', self.WhoLastDidIt)
      print '%s %s' % ('When it is next due:', self.WhenIsItNextDue)
      print '%s %s' % ('Overdue?:', self.Overdue)
      print '%s %s' % ('Who normally does it?:', self.WhoNormallyDoes)
      print '%s %s' % ('How often are we doing it?:', self.HowOftenAreWeDoingIt)
      

scope = ['https://spreadsheets.google.com/feeds', 'https://docs.google.com/feeds']

f = file('/Users/pc/Downloads/Household Todo-aafb6e63aee2.p12', 'rb')
key = f.read()
f.close()

credentials = SignedJwtAssertionCredentials(service_account_name='802536618833-rfs5lcmms4okrua1hlh9aiv0ldvba8o9@developer.gserviceaccount.com', 
private_key=key, scope=scope, private_key_password='notasecret')

gc = gspread.authorize(credentials)

wks = gc.open("API Test Spreadsheet").sheet1

wks = gc.open("Household Tasks").sheet1

#wks=gc.openall()

#print len(wks)


#wks=gc.open_by_url('https://docs.google.com/spreadsheets/d/1KqEFPnOxLt3-Ls1xsiRTLIDZI8lJ0Jlp3bD79Fzwi1g/edit')

records = wks.get_all_records()

#values = wks.get_all_values()

#print wks.acell('B3').value

items =[]

for record in records:
  t = TodoItem()
  t.ParseDictionary(record)
  items.append(t)
  
  
  

for item in items:  
  print 'Parsed results:'
  print item.PrintItem()
  print '\n'

