__author__ = "Andreas H. Kelch"

import logging
import operator
import pymongo
from datetime import datetime
from viur.xeno.databases.unqlite_adapter import Entity,Key,Query


__db__ = pymongo.MongoClient("localhost", 27017)
logging.error("DB Init")

def connect():
	pass


def put(entity:Entity):
	logging.error("PUT")
	pass



def get_multi(keys:[Key]):
	pass

def delete(key:Key):
	pass


def query(query:Query):
	return []

def transaction_start():
	pass #__db__.startTransaction()

def transaction_commit():
	pass #__db__.commitTransaction()

def transaction_rollback():
	pass #__db__.abortTransaction()

def get(key): #not used
	pass
