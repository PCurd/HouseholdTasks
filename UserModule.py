#User class is used to store information about the two users in the couple#
class User(object):
  @staticmethod
  def create_currentUser(couple):
    currentUser = User(couple['currentUser']['firstName'], couple['currentUser']['id'], couple['currentUser']['email'])
    return currentUser

  @staticmethod
  def create_otherUser(couple):
    otherUser = User(couple['otherUser']['firstName'], couple['otherUser']['id'], couple['otherUser']['email'])
    return otherUser
  
  def __init__(self, firstName, AvocadoID, email):
    self.firstName = firstName
    self.AvocadoID = AvocadoID
    self.email = email


#Couple class is used to store the two users in the couple
class Couple(object):
  @staticmethod
  def convert_to_python_couple(jsoncouple):
    currentUser = User.create_currentUser(jsoncouple)
    otherUser = User.create_otherUser(jsoncouple)
    pythoncouple = Couple(currentUser, otherUser)
    return pythoncouple

  def __init__(self, currentUser, otherUser):
    self.currentUser = currentUser
    self.otherUser = otherUser

  def get_first_name_by_ID(self, ID):
    if self.currentUser.AvocadoID == ID:
      return self.currentUser.firstName
    else:
      if self.otherUser.AvocadoID == ID:
        return self.otherUser.firstName
      else:
        print "No user in the couple has the ID " + ID + "."
        sys.exit(0)