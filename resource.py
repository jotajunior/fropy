class Resource:
	
	def extractUids(self, uids, name="friend"):
		to_return = []
		
		for row in uids:
			node = row[name]
			to_return.append(int(str(node["uid"])))
		
		return to_return
		
	def extractProducts(self, products, name="frop"):
			to_return = []
			
			for row in products:
				to_append = []
				node = row[name]
				to_append["id"] = str(node["id"])
				to_append["cover"] = str(node["cover"])
				to_append["title"] = str(node["title"])
				to_append["price"] = str(node["price"])
				to_append["uid"] = str(node["uid"])
				to_append["category"] = str(node["category"])
				to_return.append(to_append)
			
			return to_return