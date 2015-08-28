class site_wrapper:
	def __init__(self, url, identifier):
		self.url = url
		self.identifier = identifier
		self.hashed_content = None
		self.has_changed = False

	def check_new_hash(self, new_hash):
		if self.hashed_content is None:
			self.hashed_content = new_hash
			return
		if self.hashed_content != new_hash:
			self.has_changed = True
			self.hashed_content = new_hash
		else:
			self.has_changed = False
	
