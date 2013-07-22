from neo4j import GraphDatabase
from cgi import escape

class Product:

	def __init__(self, db):
		self.userIndex = self.db.node.indexes.get("uid_index")
		self.productIndex = self.db.node.indexes.get("frop_index")
		self.me = False
		self.saved = False
	
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
		
		with self.db.transaction:
			productNode = self.db.nodes.create(id=id,
											   price=price,
											   cover=cover,
											   title=title,
											   userUid=userUid,
											   category=category,
											   created=created
											   )

			self.productIndex["id"][id] = productNode
			return True
		
		return False
		
	def save(self):
		self.saveToGraph() # add others later...
		self.saved = True
		
	def get(self):
		if self.me == False:
			self.me = self.ProductIndex["id"][int(self.id)].single
		
		return self.me
	
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