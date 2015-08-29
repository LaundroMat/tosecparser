from .parsers.offlinelist_no_intro_xml_parser import NoIntroOfflineListParser
from .parsers.tosec_parser import TosecParser, TosecNamingConvention

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


def import_no_intro_xml_dat_file(filename):
    p = NoIntroOfflineListParser(filename)
    p.parse()
    print('{} games parsed.'.format(len(p.games)))
    return p

# import argparse
#
# parser = argparse.ArgumentParser(description="Load .dat files and convert to list of dicts")
#
# # only arg is filename
# parser.add_argument("filename", help="Database name")
# parser.add_argument("-p", help="parser")
#
# args = parser.parse_args()
#
# import_no_intro_xml_dat_file(args.filename)
