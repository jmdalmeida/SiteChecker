import config as cfg

def get_hash(url):
	import urllib2
	import hashlib
	try:
		response = urllib2.urlopen(url)
		html = response.read()
		hashed_html = hashlib.md5(html).hexdigest()
		return hashed_html
	except:
		return None

def get_sites():
	from site_wrapper import site_wrapper
	sites = []
	with open(cfg.FILE, "r") as f:
		content = f.read()
		content = content.strip().split("\n")
		for c in content:
			tkns = c.split("$@$")
			if len(tkns) > 1:
				sites.append(site_wrapper(tkns[0], tkns[1]))
			else:
				sites.append(site_wrapper(c, None))
	return sites


def main():
	import time
	sites = get_sites()
	while True:
		print("*" * 50)
		for s in sites:
			print("Checking " + s.url)
			h = get_hash(s.url)
			if h is None:
				print "\033[0;31mError!\033[0m"
				continue
			s.check_new_hash(h)
			result = "> Site changed: "
			if s.has_changed:
				result += "\033[0;32mYES\033[0m"
			else:
				result += "\033[0;31mNO\033[0m"
			print result

		time.sleep(cfg.INTERVAL)
	
if __name__ == "__main__":
	main()	
