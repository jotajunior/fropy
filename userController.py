import user
import json

class UserController:
	
	def __init__(self):
		self.model = User(db)
		self.model.uid(uid).save()
		
	def updateFriends(self, friends)
		uid = int(self.uid)
		friends = json.loads(friends)
		
		for friend in friends:
			friend = int(friend)
			