
class User:

	def __init__(self):
		self.saved = False
		self.me = False
		self.setSearchDefaults()
	
	def setup(self, uid):
		self.uid = int(uid)
		self.save()
		return self
	
	def setSearchDefaults(self):
		self.order = "DESC"
		self.page = 1
		self.perPage = 20
		self.criteria = "frop.id"
		self.depth = 2

	def save(self):
		self.saveToGraph() 	# to add more, like saveToMongo and saveToMySQL
		# ...
		# ...
		self.saved = True
	
	def saveToGraph(self):
		uid = int(self.uid)
		self.createUniqueNode(uid)
		
	def get(self):
		return self.userIndex["uid"][int(self.uid)].single
	
	def delete(self):
		if not self.saved:
			return False
		
		self.deleteFromGraph() # to add more, just like in self.save
		# ...
		# ...
		self.saved = False
		
	def deleteFromGraph(self):
		uid = int(self.uid)
		with self.db.transaction:
			del self.userIndex["uid"][uid][self.get()]
			self.get().delete()
		
	def createUniqueNode(self, uid):
		uid = int(uid)
		
		with self.db.transaction:
			if self.userIndex["uid"][uid].single == None:
				userNode = self.db.nodes.create(uid=uid, points=0)
				#self.userIndex["uid"][uid] = userNode
				return True
			return True
		
		return False
			

	def connectTo(self, uid2):
		if not self.saved:	
			return False
		
		uid = int(self.uid)
		uid2 = int(uid2)
		
		if not self.createUniqueNode(uid2):
			return False
		
		query = """ START me=node:uid_index(uid='"""+str(uid)+"""'),
						  friend=node:uid_index(uid='"""+str(uid2)+"""')
					CREATE UNIQUE me-[r:FRIENDS_WITH]-friend
					RETURN r
				"""
		self.db.query(query)
		return True
	
	def owns(self, fropId):
		if not self.saved:
			return False
	
		uid = int(self.uid)
		fropId = int(fropId)
		
		productNode = self.productIndex["id"][fropId].single
		
		if productNode != None:
			query = """ START me=node:uid_index(uid='{uid}'), 
							  frop=node:frop_index(id='{fropId}')
					CREATE UNIQUE me-[:OWNS]->frop """

			return self.db.query(query, uid=uid, fropId=fropId)
		
		return False
	
	###### short methods for method chaining when using search() ########
	
	def depth(self, depth):
		if depth in range(0, 2):
			self.depth = int(depth)

		return self
	
	def page(self, page):
		self.page = int(page)
		return self
		
	def perPage(self, perPage):
		self.perPage = int(perPage)
		return self
	
	def orderBy(self, criteria):
		if criteria in ["me.points", "frop.id"]:
			self.criteria = criteria

		return self

	def desc(self):
		self.order = "DESC"
		return self
	
	def asc(self):
		self.order = "ASC"
		return self
		
	def uid(self, uid):
		self.uid = int(uid)
		return self
		
	######### /end method-chaining methods ###########
	
	def search(self):
		uid = int(self.uid)
		
		query = """ START me=node:uid_index(uid='{uid}')
					MATCH me-[:FRIENDS_WITH*0..{depth}]-()-[:OWNS]->frop
					RETURN DISTINCT frop 
					ORDER BY {criteria} {order} 
					SKIP {skip}
					LIMIT {perPage} """
		
		skip = ( self.page - 1 )*self.perPage
		
		return self.db.query(query, uid=uid, 
									depth=self.depth, 
									criteria=self.criteria, 
									skip=skip, 
									perPage=self.perPage 
							)["frop"]
	
	def deleteFriendships(self):
		uid = int(self.uid)
		
		query = """ START me=node:uid_index(uid='{uid}')
					MATCH me-[r:FRIENDS_WITH]-()
					DELETE r
				"""
		return self.db.query(query, uid=uid)
	
	def getFriends(self):
		uid = int(self.uid)
		
		query = """ START me=node:uid_index(uid='{uid}')
					MATCH me-[:FRIENDS_WITH]-friend
					RETURN friend
				"""
		
		return self.db.query(query, uid=uid)["friend"]
	
	def getFriendCount(self):
		uid = int(self.uid)
		
		query = """ START me=node:uid_index(uid='{uid}')
					MATCH me-[:FRIENDS_WITH]-friend
					RETURN COUNT(friend) AS counter
				"""
				
		return self.db.query(query, uid=uid)["counter"]
		
	def getMutualFriendCount(self, uid2):
		uid2 = int(uid2)
		uid = int(self.uid)
		
		query = """ START me=node:uid_index(uid='{uid}'),
						  friend=node:uid_index(uid='{uid2}')
					MATCH me-[:FRIENDS_WITH]-mutual-[:FRIENDS_WITH]-friend
					RETURN COUNT(DISTINCT mutual) AS counter
				"""
		
		return self.db.query(query, uid=uid, uid2=uid2)["counter"].single
		
	def getMutualFriends(self, uid2, limit = 9):
		uid = int(self.uid)
		uid2 = int(uid2)
		limit = int(limit)
		
		query = """ START me=node:uid_index(uid='{uid}'),
						  friend=node:uid_index(uid='{uid2}')
					MATCH me-[:FRIENDS_WITH]-mutual-[:FRIENDS_WITH]-friend
					RETURN DISTINCT mutual
					LIMIT {limit}
				"""
		
		return self.db.query(query, uid=uid, uid2=uid2, limit=limit)["mutual"]
	
	def getProducts(self):
		uid = int(self.uid)
		
		query = """ START me=node:uid_index(uid='{uid}')
					MATCH me-[:OWNS]->frop
					RETURN DISTINCT frop
				"""
		
		return self.db.query(query, uid=uid)["frop"]
		
	def getCounter(self):
		query = """ START me=node(*)
					WHERE HAS(me.uid)
					RETURN COUNT(DISTINCT me) AS counter
				"""
		return self.db.query(query)["counter"].single
		
	def getRelCounter(self):
		query = """ START r = relationship(*)
					RETURN COUNT(DISTINCT r) AS counter
				"""
		
		return self.db.query(query)["counter"].single

#	def getAllNodes(self):
#		q = "START m=relationship(*) RETURN COUNT(m) AS c"
#		return self.db.query(q)["c"].single