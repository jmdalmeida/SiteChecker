class SiteChecker:
	def __init__(self, _config):
		self.config = _config

	def start(self):
		import time
		sites = self.get_sites()
		while True:
			self._print("*" * 50)
			for s in sites:
				content = self.get_content(s)
				h = self.get_hash(content)
				if h is None:
					self._print("\033[0;31mError!\033[0m")
					continue
				s.check_new_hash(h)
				txt = "> Site changed: "
				if s.has_changed:
	                txt += "\033[0;32mYES\033[0m"
	            else:
	                txt += "\033[0;31mNO\033[0m"
			    self._print(txt)
			time.sleep(self.cfg.INTERVAL)

class Site:
	def __init__(self, url, id_type, identifier):
		self.url = url
		self.id_type = id_type
		self.identifier = identifier
		self.hashed_content = None
		self.has_changed = False

	def process_hash(self, new_hash):
		if self.hashed_content is None:
			self.hashed_content = new_hash
			return
		if self.hashed_content != new_hash:
			self.has_changed = True
			self.hashed_content = new_hash
		else:
			self.has_changed = False
