from .parsers.offlinelist_no_intro_xml_parser import NoIntroOfflineListParser
from tosecparser.parsers.tosec_parser import TOSECParser

def import_tosec_xml_dat_file(filename):
    p = TOSECParser(filename)
    p.parse()
    print('{} games parsed.'.format(len(p.games)))
    return p


def import_no_intro_xml_dat_file(filename):
    p = NoIntroOfflineListParser(filename)
    p.parse()
    print('{} games parsed.'.format(len(p.games)))
    return p


