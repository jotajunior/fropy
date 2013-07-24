from cgi import escape
import resource

class Product(resource.Resource):

	def __init__(self):
		self.me = False
		self.saved = False
	
	def setup(self, id):
		self.id = int(id)
		self.save()
		return self
	
	def saveToGraph(self):
		if self.saved:
			return True

		id = int(self.id)
		
		if self.productIndex["id"][id].single != None:
			return True
		
		price = float(self.price)
		cover = escape(self.cover)
		title = escape(self.title)
		userUid = int(self.userUid)
		category = int(self.category)
		created = escape(self.created)
		userName = escape(self.userName)
		
		with self.db.transaction:
			productNode = self.db.nodes.create(id=id,
											   price=price,
											   cover=cover,
											   title=title,
											   userUid=userUid,
											   category=category,
											   created=created,
											   userName=userName
											   )

			self.productIndex["id"][id] = productNode
			return True
		
		return False
		
	def save(self):
		self.saveToGraph() # add others later...
		self.saved = True
		
	def get(self):
		return self.productIndex["id"][int(self.id)].single
	
	def deleteOwnerships(self):
		id = int(self.id)
		
		query = """ START thisFrop=node:frop_index(id='{id}')
					MATCH ()-[r:OWNS]->thisFrop
					DELETE r
				"""
				
		return self.db.query(query, id=id)
		
	def deleteFromGraph(self):
		id = int(self.id)
		
		with self.db.transaction:
			del self.productIndex["id"][id][self.get()]
			self.get().delete()
	
	def delete(self):
		self.deleteFromGraph()
		self.saved = False