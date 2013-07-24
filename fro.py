#!flask/bin/python
from flask.ext.cache import Cache
from flask import Flask, jsonify
from neo4j import GraphDatabase
import user
import product

# Base Configuration #
print "Base Config"
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
		graph = GraphDatabase("/usr/local/Cellar/neo4j")
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
app = Flask(__name__)
print "On Routes"

#global cache
#cache = Cache()
#cache.init_app(app, config={'CACHE_TYPE':'memcached'})

@app.route('/', methods=['GET'])
def index():
	return "Hello"

@app.route('/v1.1/<int:uid>/friends', methods=['GET'])
def get_friends(uid):
	global u
	friends = u.setup(uid).getFriends()

	result = []
	return friends
	for friend in friends:
		print friend

	return jsonify(result)

@app.route('/v1.1/<int:uid>/connectTo/<int:uid2>', methods=['GET'])
def connect_to(uid, uid2):
	global u
	result = u.setup(uid).connectTo(uid2)
	return str(result)

@app.route('/v1.1/<int:uid>/save', methods=['GET'])
def save(uid):
	global u
	u.setup(uid)
	return str(True)

@app.route('/counter', methods=['GET'])
def counter():
	global u
	return str(u.getCounter())

@app.route('/rcounter', methods=['GET'])
def rcounter():
	global u
	return str(u.getRelCounter())

## RUNNING SERVER ##
if __name__ == '__main__':
    app.run(debug = False)