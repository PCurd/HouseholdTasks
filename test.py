#!/usr/bin/python

try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import gdata.spreadsheet.service
import gdata.service
import atom.service
import gdata.spreadsheet
import atom
import getopt
import sys
import string

class SimpleCRUD:

  def __init__(self, email, password):
    self.gd_client = gdata.spreadsheet.service.SpreadsheetsService()
    self.gd_client.email = email
    self.gd_client.password = password
    self.gd_client.source = 'PCurd Test Apps'
    self.gd_client.ProgrammaticLogin()
    self.curr_key = '1KqEFPnOxLt3-Ls1xsiRTLIDZI8lJ0Jlp3bD79Fzwi1g'
    self.curr_wksht_id = 'od6'
    
  def CellsGetAction(self):
    # Get the feed of cells
    feed = self.gd_client.GetCellsFeed(self.curr_key, self.curr_wksht_id)
    self._PrintFeed(feed)
    self._PrintCell(feed,2,2)

  def _PrintFeed(self, feed):
    for i, entry in enumerate(feed.entry):
      print '%s %s' % (entry.title.text, entry.content.text)

  def _PrintCell(self, feed, col, row):
    print '%s %s' % (feed[col][row].content.text, feed[col][row].title.text)








def main():
  # parse command line options
  try:
    opts, args = getopt.getopt(sys.argv[1:], "", ["user=", "pw="])
  except getopt.error, msg:
    print 'python test.py --user [username] --pw [password] '
    sys.exit(2)
  
  user = ''
  pw = ''
  key = ''
  # Process options
  for o, a in opts:
    if o == "--user":
      user = a
    elif o == "--pw":
      pw = a

  if user == '' or pw == '':
    print 'python spreadsheetExample.py --user [username] --pw [password] '
    sys.exit(2)
        
  sample = SimpleCRUD(user, pw)
  sample.CellsGetAction()

if __name__ == '__main__':
  main()



  