from bottle import run, route
from neo4j import GraphDatabase
import user
import product
import json

# Base Configuration #
global graph
graph = None
global userIndex
userIndex = None
global productIndex
productIndex = None

def startGraph():
	global graph
	global userIndex
	global productIndex
	
	if graph == None:
		print "Starting graph"
		graph = GraphDatabase("/usr/local/Cellar/neo4j/")
		userIndex = graph.node.indexes.get("uid_index")
		productIndex = graph.node.indexes.get("frop_index")

startGraph()

global u
u = user.User()
u.db = graph
u.userIndex = userIndex
u.productIndex = productIndex

global p
p = product.Product()
p.db = graph
p.userIndex = userIndex
p.productIndex = productIndex

# Routes #


@route('/v1.1/<uid>/friends', method='GET')
def get_friends(uid):
	global u
	friends = u.setup(uid).getFriends()

	result = []
	
	for friend in friends:
		result.append(friend["uid"])

		
	return json.dumps(result)

@route('/v1.1/<uid>/connectTo/<uid2>')
def connect_to(uid, uid2):
	global u
	result = u.setup(uid).connectTo(uid2)
	return str(result)

@route('/v1.1/create/<uid>')
def create(uid):
	global u
	u.setup(uid)

@route('/counter')
def counter():
	global u
	return str(u.getCounter())

@route('/rcounter')
def rcounter():
	global u
	return str(u.getRelCounter())
## RUNNING SERVER ##
run(host='localhost', port=8080, debug=True)