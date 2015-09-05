import pdb

import hashlib
import time

import lxml.etree as le
import lxml.html
from lxml.html.clean import Cleaner
from lxml.cssselect import CSSSelector

from io import StringIO
import requests

import difflib
from urlparse import urlparse

import os


class SiteChecker:

    def __init__(self, _config):
        self.config = _config

    def start(self):
        sites = self.get_sites()
        while True:
            self._print("-" * 50)
            for site in sites:
                self._print("*")
                self._print("Checking " + site.url)
                content = self.get_content(site)
                if content is None:
                    self._print("Failed to retrieve page content.")
                    continue
                h = self.get_hash(content)
                self._print("Current hash: " + str(site.hashed_content))
                self._print("Generated hash: " + str(h))
                if h is None:
                    self._print("\033[0;31mError!\033[0m")
                    continue
                site.process_hash(h)
                txt = "Site changed: "
                if site.has_changed:
                    txt += "\033[0;32mYES\033[0m"
                    self.save_changes(site.url, site.plain_content, content)
                else:
                    txt += "\033[0;31mNO\033[0m"
                txt += " (changed " + str(site.changes_count) + " times)"
                self._print(txt)
                site.plain_content = content  # TEST
            time.sleep(self.config.INTERVAL)

    def get_sites(self):
        sites = []
        with open(self.config.FILE, "r") as f:
            content = f.read()
            content = content.strip().split("\n")
            for c in content:
                s = None
                tkns = c.split(self.config.DELIMITER)
                assert len(tkns) == 1 or len(tkns) == 3
                if len(tkns) == 3:
                    assert tkns[1] == "css" or tkns[1] == "xpath"
                    s = Site(tkns[0], tkns[1], tkns[2])
                else:
                    s = Site(c, "css", "body")  # default behavior
                if s is not None:
                    sites.append(s)
                else:
                    self._print("Error adding site to the list.")
        return sites

    def get_content(self, site):
        sel = None
        if site.id_type == "css":  # translates csspath into xpath
            s = CSSSelector(site.identifier)
            sel = s.path
        else:
            sel = site.identifier
        try:
            page = requests.get(site.url)
            parser = le.HTMLParser()
            tree = le.parse(StringIO(page.text), parser)
            xp = tree.xpath(sel)
            if len(xp) < 1:
                return None
            html = lxml.html.tostring(xp[0])
            cleaner = Cleaner(style=True, links=False,
                              page_structure=False, embedded=False,
                              frames=False, forms=False)
            cleaned_html = cleaner.clean_html(html)
            self._print("Cleaning html: " + str(len(html)) +
                        " -> " + str(len(cleaned_html)))
            return cleaned_html
        except Exception as e:
            self._print("EXCEPTION! " + str(e.message))
            return None

    def save_changes(self, url, old_content, new_content):
        if not self.config.SAVE_DIFF:
            return
        host = urlparse(url).hostname
        changes = self.get_changes(old_content, new_content)
        filename = self.config.DIFF_FILENAME \
            .replace("$h", host) \
            .replace("$t", str(time.time()))
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename, "w") as f:
            f.write(changes)

    def get_changes(self, old_content, new_content):
        udiff = difflib.unified_diff(old_content.splitlines(),
                                     new_content.splitlines())
        return '\n'.join(udiff)

    def get_hash(self, content):
        assert content is not None
        return hashlib.md5(content).hexdigest()

    def _print(self, msg):
        # TODO: check if verbose mode
        print(msg)


class Site:

    def __init__(self, url, id_type, identifier):
        self.url = url
        self.id_type = id_type
        self.identifier = identifier
        self.plain_content = None
        self.hashed_content = None
        self.has_changed = False
        self.changes_count = 0

    def process_hash(self, new_hash):
        if self.hashed_content is None:
            self.hashed_content = new_hash
            return
        if self.hashed_content != new_hash:
            self.has_changed = True
            self.hashed_content = new_hash
            self.changes_count += 1
        else:
            self.has_changed = False
