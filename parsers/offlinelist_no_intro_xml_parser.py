import re
from lxml import etree


class NoIntroOfflineListParser(object):
    """ Parses No-Intro XML .dat files into list of dicts
    """

    locations = {
        '0': ('Europe',),
        '1': ('USA',),
        '2': ('Germany',),
        '3': ('China',),
        '4': ('Spain',),
        '5': ('France',),
        '6': ('Italy',),
        '7': ('Japan',),
        '8': ('Netherlands',),
        '9': ('England',),
        '10': ('Denmark',),
        '11': ('Finland',),
        '12': ('Norway',),
        '13': ('Poland',),
        '14': ('Portugal',),
        '15': ('Sweden',),
        '16': ('Europe', 'USA',),
        '17': ('Europe', 'USA', 'Japan',),
        '18': ('USA', 'Japan',),
        '19': ('Australia',),
        '20': ('North Korea',),
        '21': ('Brazil',),
        '22': ('South Korea',),
        '23': ('Europe', 'Brazil',),
        '24': ('Europe', 'USA', 'Brazil',),
        '25': ('USA', 'Brazil')
    }

    languages = {
        1: 'French',
        2: 'English (US)',
        4: 'Chinese',
        8: 'Danish',
        16: 'Dutch',
        32: 'Finland',
        64: 'German',
        128: 'Italian',
        256: 'Japanese',
        512: 'Norwegian',
        1024: 'Polish',
        2048: 'Portuguese',
        4096: 'Spanish',
        8192: 'Swedish',
        16384: 'English (UK)',
        32768: 'Portuguese (BR)',
        65536: 'Korean',
    }

    def _find_languages(self, found, codes, sum_of_game_languages):
        # Bit flags like... See http://forums.no-intro.org/viewtopic.php?f=2&t=992
        code = codes.pop()  # pops last, i.e. highest
        if sum_of_game_languages % code == sum_of_game_languages:  # doesn't contain this language
            found = self._find_languages(found, codes, sum_of_game_languages)  # Try again, highest code gone
            return found
        elif sum_of_game_languages % code > 0:
            found += (self.languages[code],)
            sum_of_game_languages -= sum_of_game_languages % code
            found = self._find_languages(found, codes, sum_of_game_languages)  # Try again, highest code gone
            return found
        elif sum_of_game_languages % code == 0:
            found += (self.languages[code],)
            return found

    def __init__(self, filename):
        self.tree = etree.parse(filename)
        self.games = []

    def parse(self):
        system = self.tree.find('//system').text
        for game_element in self.tree.find('//games').iterchildren():
            game = dict()
            game['title'] = self.get_game_title(game_element)
            game['publisher'] = self.get_game_publisher(game_element)
            game['date'] = self.get_game_date(game_element)
            game['languages'] = self.get_game_language(game_element)
            game['locations'] = self.get_game_locations(game_element)
            self.games.append(game)

    def get_game_title(self, game_element):
        return game_element.find('title').text

    def get_game_publisher(self, game_element):
        text = game_element.find('publisher').text
        publisher = re.sub(r"\(.*\)$", '', text).strip()
        if publisher == '':
            publisher = None
        return publisher

    def get_game_date(self, game_element):
        text = game_element.find('publisher').text
        date = re.search("\(.*\)$", text)
        if date:
            date = date.group()[1:-1]
        if date == "????-??-??":
            date = None
        return date

    def get_game_language(self, game_element):
        offlinelist_language_codes = [n for n in self.languages.keys()]
        offlinelist_language_codes.sort()  # from lowest to highest

        game_language_codes = game_element.find('language').text
        if game_language_codes:
            game_language_codes = int(game_language_codes)
            if game_language_codes > 0:
                return self._find_languages(tuple(), offlinelist_language_codes, game_language_codes)

        return None

    def get_game_locations(self, game_element):
        location_code = game_element.find('location').text
        if location_code == '-1':
            return None
        else:
            return self.locations[location_code]
