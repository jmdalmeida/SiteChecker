# config.py
INTERVAL = 60  # Routine sleep interval (in seconds).
FILE = "sites.txt"  # File to get the site list from.
DELIMITER = "|"  # Determines which string to use as delimiter when splitting sites.
SAVE_DIFF = False # Wether to store the result of difflib.unified_diff.
# Path for the new file.
# $h - site's hostname; $t - current timestamp
DIFF_FILENAME = "change_logs/$h/$t.log" 
