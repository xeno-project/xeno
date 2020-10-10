__author__ = "Andreas H. Kelch"

import logging
import pymongo,bson
from viur.xeno.databases.unqlite_adapter import Entity,Key,Query
from viur.xeno import xeno_conf

__currentSession__ = None
__client__ = None
__db__ = None

def generateID():
	'''
		create a new DB Key
	'''
	return bson.objectid.ObjectId()

def connect():
	'''
		establish mongodb connection
	'''
	global __client__, __db__
	__client__ = pymongo.MongoClient(xeno_conf.conf["xeno.application.databaseConnection"][0],
									 xeno_conf.conf["xeno.application.databaseConnection"][1],tz_aware=True)

	try:
		logging.error( "Try to connect to MongoDB..." )
		__client__.server_info()
	except:
		logging.error( "No MongoDB connection!" )
		raise

	__db__ = __client__[ "xeno" ]
	logging.info( "DB Init" )

def dbobjToEntity(value):
	'''
		convert dbObj to Entity
	'''
	if isinstance(value,(dict)):
		for k,v in value.items():
			if k!="__keyDB__" and isinstance(v,dict) and "ext.type" in v and v["ext.type"] == "key":
				value[k] = Key(v["kind"],v["key"])
			else:
				value[k] = dbobjToEntity(v)

		if "__keyDB__" in value:
			e = Entity()
			e.update(value)
			e.fromDict()
			value = e

	elif isinstance(value,list):
		value = [ dbobjToEntity(i) for i in value ]

	return value

def EntityToDbobj(value):
	'''
		convert Enitity to dbObj
	'''
	if isinstance(value,(Entity,dict)):
		for k,v in value.items():
			if k!="__keyDB__" and isinstance(v,Key):
				value[k] = {"ext.type":"key","kind":v.kind, "key":v.id_or_name}
			else:
				value[k] = EntityToDbobj(v)

		if isinstance(value,Entity):
			value = value.toDict()

	elif isinstance(value,list):
		value = [ EntityToDbobj(i) for i in value ]

	return value

def put(entity:Entity):
	'''
	write Entity to DB
	'''
	currentKey = entity.key.id_or_name
	entity[ "_id" ] = currentKey
	mdbEntity = EntityToDbobj( entity )
	collection = __db__.get_collection(entity.kind)
	result = collection.update_one({"_id":currentKey},{"$set":mdbEntity},upsert = True)

def get_multi(keys:[Key]):
	'''
		read entries from DB
	'''
	entities = []

	for key in keys:
		collection = __db__.get_collection( key.kind )
		result = collection.find_one({"_id":key.id_or_name})
		if result:
			entities.append(dbobjToEntity(result))

	return entities

def delete(key:Key):
	'''
		remove from DB
	'''
	collection = __db__.get_collection( key.kind )
	collection.remove({"_id":key.id_or_name})


def dbFilterToQuery(filterList):
	'''
		convert filterobj to Queryobj
	'''
	mdbFilter = {}

	ops = {
		'>' : "$gt",
		'<' : "$lt",
		'>=': "$gte",
		'<=': "$lte",
		'=' : "$eq",
		"in": "$in"
	}
	for filter in filterList:
		if isinstance(filter[2],Key):
			value = str(filter[2].id_or_name)
			field = "%s.key"%filter[0]
		else:
			value = filter[2]
			field = filter[0]

		mdbFilter.update({field:{ops[filter[1]]:value}})

	return mdbFilter


def query(query:Query):
	'''
		run a query
		TODO: implement ordering
			.sort([("field1", pymongo.ASCENDING), ("field2", pymongo.DESCENDING)])
	'''
	entities = [ ]
	collection = __db__.get_collection( query.kind )

	mdbFilter = dbFilterToQuery(query.filters)

	result = collection.find(mdbFilter)
	for r in list(result):
		r = dbobjToEntity(r)
		if r:
			entities.append(r)

	return entities

def transaction_start():
	'''
		start Transaction
	'''
	global __currentSession__
	__currentSession__ = __client__.start_session()
	__currentSession__.start_transaction()

def transaction_commit():
	'''
		commit Transaction
	'''
	global __currentSession__
	if not __currentSession__ or __currentSession__.has_ended:
		__currentSession__ = __client__.start_session()
		__currentSession__.start_transaction()

	__currentSession__.commit_transaction()

def transaction_rollback():
	'''
		rollback Transaction
	'''
	__currentSession__.abort_transaction()
	__currentSession__.end_session()

def get(key): #not used
	pass
