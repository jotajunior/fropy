import falcon
from neo4j import GraphDatabase
import json
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

def startGraph(): # small hack to persist just one instance of the embedded graph database
	global graph
	global userIndex
	global productIndex
	
	if graph == None:
		print "Starting graph"
		graph = GraphDatabase("/usr/local/Cellar/neo4j")
		userIndex = graph.node.indexes.get("uid_index")
		productIndex = graph.node.indexes.get("frop_index")
		
startGraph()

def userInstance():
	global graph
	global userIndex
	global productIndex
	
	u = user.User()
	u.db = graph
	u.userIndex = userIndex
	u.productIndex = productIndex

	return u

def productInstance():
	global graph
	global userIndex
	global productIndex
	
	p = product.Product()
	p.db = graph
	p.userIndex = userIndex
	p.productIndex = productIndex
	
	return p
	

# Routes #
print "On Routes"

#global cache
#cache = Cache()
#cache.init_app(app, config={'CACHE_TYPE':'memcached'})

class MutualFriendResource(object):
	def on_get(self, req, resp, uid1, uid2):
		u = userInstance()
		u.setup(uid1)
		resp.set_header('Content-Type', 'application/json')
		resp.status = falcon.HTTP_200
		resp.body = json.dumps(u.getMutualFriends(uid2))
		del u

class MutualFriendCountResource(object):
	def on_get(self, req, resp, uid1, uid2):
		u = userInstance()
		u.setup(uid1)
		resp.set_header('Content-Type', 'text/plain')
		resp.status = falcon.HTTP_200
		resp.body = str(u.getMutualFriendCount(uid2))
		del u

class UserResource(object):
	def on_get(self, req, resp, uid):
		u = userInstance
		products = u.setup(uid).getProducts()
		resp.set_header('Content-Type', 'application/json')
		resp.status = falcon.HTTP_200
		resp.body = json.dumps(products)
		del u

	def on_post(self, req, resp, uid):
		u = userInstance()
		u.setup(uid)
		resp.status = falcon.HTTP_202
		del u

class SocialSearchResource(object):
	def on_get(self, req, resp, uid):
		u = userInstance()
		depth = req.get_param('depth') or 2
		page = req.get_param('page') or 1
		limit = req.get_param('limit') or 20
		products = u.setup(uid).depth(depth).page(page).perPage(limit).orderBy("frop.id").desc().search()
		resp.set_header('Content-Type', 'application/json')
		resp.status = falcon.HTTP_200
		resp.body = json.dumps(products)
		del u

class FriendshipResource(object):
	def on_post(self, req, resp, uid):
		u = userInstance()
		
		try:
			raw = req.stream.read()
		except Exception as ex:
			raise falcon.HTTPError(falcon.HTTP_400, 'Error', ex.message)

		try:
			received = json.loads(raw)
			me = u.setup(uid)

			for i in received:
				me.connectTo(i)

			resp.status = falcon.HTTP_202
			
			del u
			del me
		except ValueError:
			raise falcon.HTTPError(falcon.HTTP_400, 'Malformed JSON')
			
	def on_get(self, req, resp, uid):
		u = userInstance()
		friends = u.setup(uid).getFriends()
		resp.body = json.dumps(friends)
		del u
		del friends
		
class CounterResource(object):
	def on_get(self, req, resp):
		u = userInstance()
		resp.body = str(u.getCounter())
		del u

class RCounterResource(object):
	def on_get(self, req, resp):
		u = userInstance()
		resp.body = str(u.getRelCounter())
		del u

wsgi_app = api = falcon.API()
mutual_friend = MutualFriendResource()
mutual_friend_count = MutualFriendCountResource()
userRes = UserResource()
social_search = SocialSearchResource()
friendship = FriendshipResource()
counter = CounterResource()
rcounter = RCounterResource()

api.add_route('/v1.2/user/{uid1}/user/{uid2}/mutual', mutual_friend)
api.add_route('/v1.2/user/{uid1}/user/{uid2}/mutual/count', mutual_friend_count)
api.add_route('/v1.2/user/{uid}', userRes)
api.add_route('/v1.2/user/{uid}/socialsearch', social_search)
api.add_route('/v1.2/user/{uid}/friends', friendship)
api.add_route('/counter', counter)
api.add_route('/rcounter', rcounter)