from neo4jrestclient.client import GraphDatabase

class User:

	def __init__(self):
		self.db = GraphDatabase("http://localhost:7474/db/data")
		self.userIndex = self.db.nodes.indexes.get("uid_index")
		self.productIndex = self.db.nodes.indexes.get("frop_index")
		self.saved = false
		self.me = false
	
	def save(self):
		self.saveToGraph() 	# to add more, like saveToMongo and saveToMySQL
		# ...
		# ...
		self.saved = true
	
	def saveToGraph(self):
		uid = int(self.uid)
		self.createUniqueNode(uid)
		
	def get(self):
		if self.me == false:
			self.me = self.userIndex["uid"][int(self.uid)]
			
		return self.me
	
	def delete(self):
		if not self.saved:
			return false
		
		self.deleteFromGraph() # to add more, just like in self.save
		# ...
		# ...
		self.saved = false
		
	def deleteFromGraph(self):
		uid = int(self.uid)
		self.userIndex.delete("uid", uid, self.get())
		
		query = "START n=node:uid_index(uid='"+uid+"') DELETE n"
		return self.db.query(q=query) == ''
		
	def createUniqueNode(self, uid):
		uid = int(uid)
		
		if self.userIndex["uid"][uid] == []:
			userNode = self.db.nodes.create(uid=uid, points=0)
			self.userIndex["uid"][uid] = userNode
			return true
		
		return false
			

	def connectTo(self, uid2):
		if not self.saved:	
			return false
		
		uid = int(self.uid)
		uid2 = int(uid2)
		
		self.createUniqueNode(uid2)
		
		query = """ START me=node:uid_index(uid='"""+ uid +"""'),
						  friend=node:uid_index(uid='"""+ uid2 +"""')
					CREATE UNIQUE me-[:FRIENDS_WITH]-friend
				"""
		return self.db.query(q=query) == ''
	
	def owns(self, fropId):
		if not self.saved:
			return false
	
		uid = int(self.uid)
		fropId = int(fropId)
		
		productNode = self.productIndex["id"][fropId]
		
		if productNode != []:
			query = """ START me=node:uid_index(uid='"""+ uid +"""'), frop=node:frop_index(id='""" + fropId + """')
					CREATE UNIQUE me-[:OWNS]->frop """

			return self.db.query(q=query) == ''
		
		return false