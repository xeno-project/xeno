import os, logging,mimetypes
from viur.core import conf

bucketPath = os.path.join(conf[ "xeno.application.projectroot" ],"..","_service","files")
class bucket():
	'''
		Simplestorage bucket with minimal interface
	'''
	def __init__(self,path=None):
		if not path:
			path = bucketPath
		self.path = path
		self.name = "xeno.simplestorage"


	def get_blob( self,path ):
		requestedFile = os.path.join(self.path,path)
		xenofile(requestedFile)
		return xenofile

	def blob( self, path ):
		return self.get_blob(path)

	def generate_upload_policy( self,conditions ):
		return {}

	def list_blobs( self,prefix ):
		bloblist = []
		for root,dirs,files in os.walk( os.path.join(self.path,prefix)):
			bloblist.extend([xenofile(os.path.join(root,f)) for f in files])
		return bloblist

class xenofile():
	'''
		minimal file wrapper
	'''
	def __init__(self,filePath):
		self.filePath = filePath
		self.file = None
		self.fileloaded = False

		self.loadFile()
		self.content_type = mimetypes.guess_type(self.filePath)[0]
		self.name = os.path.basename(self.filePath)
		self.size = 0

	def loadFile( self ):
		if not os.path.exists( self.filePath ):
			return None

		self.file = open( self.filePath, "rb" )
		self.file.close()
		self.fileloaded = True

	def download_to_file( self,target=None ):
		if not self.file:
			self.loadFile()
		target = self.file
		return self.file

	def upload_from_file( self,fileData, mimetype=None ):
		targetdir = os.path.join(bucketPath,os.path.dirname(self.filePath))
		if not os.path.isdir(targetdir):
			os.makedirs(targetdir)
		with open( os.path.join(bucketPath,self.filePath), "wb" ) as f:
			f.write(fileData.getbuffer())
		self.name = os.path.basename( self.filePath )
		self.size = fileData.__sizeof__()
		self.content_type = mimetypes.guess_type(self.name)[0]

	def delete( self ):
		os.remove(self.filePath)

def fileUpload(key, file):
	'''
		upload entrypoint
	'''
	newFile = xenofile(key)
	newFile.upload_from_file(file.file)




