__author__ = "Andreas H. Kelch"

# xeno-Project - A no Google, no cloud ViUR Framework
#
# Copyright (c) 2019-2020 Andreas H. Kelch
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of version 2.1 of the GNU Lesser General Public License
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


from viur.database.datastore.entity import Entity
from viur.database.datastore.key import Key
from viur.database.datastore.geopoint import GeoPoint
from datetime import datetime
'''
Jeden datastore typen convertieren

Musst habe Features der Datenbanken: Nested dicts und listen
Entity == DatastoreEntity
Document == Other Database Object

'''

class converter:

	def toDocument( self, entity:[Entity, dict] ):
		document = {}
		fieldtypes = {}

		for key, value in entity.items():
			datatype, field = self.entityConverter(key,value)
			document.update({key:field})
			fieldtypes.update({key:datatype.__name__})
		document.update({"__entitytypes__":fieldtypes}) #save original datatypes
		return document

	def entityConverter( self,key,value ):
		'''
		Datastore types
		datetime.datetime
		Key
		bool
		float
		int (as well as long in Python 2)     int
		unicode (called str in Python 3)      str
		bytes (called str in Python 2)        bytes
		GeoPoint
		None
		-----
		list
		Entity
		dict (will just be treated like an Entity without a key or exclude_from_indexes)


		UnqLite supports
		string
		int
		float
		bool
		None
		----
		list
		dict


		MISSING
		Datetime
		Key
		bytes
		GeoPoint



		:param key:
		:param value:
		:return:
		'''

		if isinstance( value, list ):
			field = []
			for entity in value:
				field.append(self.toDocument(entity))
		elif isinstance(value,Entity) or isinstance(value,dict):
			field = self.toDocument(value)
		elif isinstance(value, datetime):
			field = self.convertEntityDatetime(key,value)
		elif isinstance(value,Key):
			field = self.convertEntityKey(key,value)
		elif isinstance(value,bool):
			field = self.convertEntityBool(key,value)
		elif isinstance(value,float):
			field = self.convertEntityFloat(key,value)
		elif isinstance(value,int):
			field = self.convertEntityInt(key,value)
		elif isinstance(value,str):
			field = self.convertEntityStr(key,value)
		elif isinstance(value,bytes):
			field = self.convertEntityBytes(key,value)
		elif isinstance(value,GeoPoint):
			field = self.convertEntityGeoPoint(key,value)
		elif value is None:
			field = self.convertEntityNone(key,value)
		else:
			field = value

		datatype = type(value)

		return datatype,field

	def convertEntityDatetime( self,key,value ):
		return value

	def convertEntityKey( self,key,value ):
		return value

	def convertEntityBool( self,key,value ):
		return value

	def convertEntityFloat( self,key,value ):
		return value

	def convertEntityInt( self,key,value ):
		return value

	def convertEntityStr( self,key,value ):
		return value

	def convertEntityBytes( self,key,value ):
		return value

	def convertEntityGeoPoint( self,key,value ):
		return value

	def convertEntityNone( self,key,value ):
		return value

	# the way back
	def toEntity( self,document ):
		if "__key__" in document:
			keyObj: dict = document[ "__key__" ]  # load saveable Key {"kind":k, "id_or_name":id}

			key = Key( keyObj[ "kind" ], keyObj[ "id_or_name" ] )
			entity = Entity( key = key )
		else:
			entity = {}

		if "__entitytypes__" in document:
			entitytypes = document[ "__entitytypes__" ]
		else:
			entitytypes = None

		for key, value in document.items():
			if not key.startswith("__") and not key.endswith("__"):
				if entitytypes:
					currentType = entitytypes["key"]
				else:#normal dict
					currentType = type(value).__name__

				entity.update({key:self.documentConverter( key, value,currentType )})

		return entity

	def documentConverter( self,key,value,type ):

		if type == "list":
			field = [ ]
			for document in value:
				field.append( self.toEntity( document ) )
		elif type == "Entity" or type == "dict":
			field = self.toEntity( value )
		elif type == "datetime":
			field = self.convertDocumentDatetime( key, value )
		elif type == "Key":
			field = self.convertDocumentKey( key, value )
		elif type == "bool":
			field = self.convertDocumentBool( key, value )
		elif type == "float":
			field = self.convertDocumentFloat( key, value )
		elif type == "int":
			field = self.convertDocumentInt( key, value )
		elif type == "str":
			field = self.convertDocumentStr( key, value )
		elif type == "bytes":
			field = self.convertDocumentBytes( key, value )
		elif type == "GeoPoint":
			field = self.convertDocumentGeoPoint( key, value )
		elif type == "NoneType":
			field = self.convertDocumentNone( key, value )
		else:
			field = value

		return field

	def convertDocumentDatetime( self,key,value ):
		return value

	def convertDocumentKey( self,key,value ):
		return value

	def convertDocumentBool( self,key,value ):
		return value

	def convertDocumentFloat( self,key,value ):
		return value

	def convertDocumentInt( self,key,value ):
		return value

	def convertDocumentStr( self,key,value ):
		return value

	def convertDocumentBytes( self,key,value ):
		return value

	def convertDocumentGeoPoint( self,key,value ):
		return value

	def convertDocumentNone( self,key,value ):
		return value