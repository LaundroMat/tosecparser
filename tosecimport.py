import os
from parsers.parser import TosecParser, TosecNamingConvention

def convert_dat_to_dicts(filename):
	print("Importing {}".format(filename))
	with open(filename, 'r') as tosec_dat:
		dat_contents = tosec_dat.readlines()

	tosec_parser = TosecParser(dat_contents)
	tosec_parser.parse()

	category = tosec_parser.headers['name']
	
	print(category)

	for game in tosec_parser.games:
		tnc = TosecNamingConvention(game['name'])
		print(tnc.__dict__)

import argparse
parser = argparse.ArgumentParser(description="Load .dat files and convert to list of dicts")

# only arg is filename
parser.add_argument("filename", help="Database name")

args = parser.parse_args()

convert_dat_to_dicts(args.filename)

