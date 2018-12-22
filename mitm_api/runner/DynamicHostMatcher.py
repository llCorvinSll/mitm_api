import re


class DynamicHostMatcher:
    """
    Работает по принципу белого списка -
    следит  только за теми хостамит, что дали ему
    """

    def __init__(self, patterns=tuple()):
        self.patterns = list(patterns)
        self.regexes = []
        self.recalculate_regexps()

    def __call__(self, address):
        if not address:
            return False
        host = "%s:%s" % address

        if any(rex.search(host) for rex in self.regexes):
            return False
        else:
            return True

    def __bool__(self):
        return True

    def add(self, pattern):
        self.patterns.append(pattern)
        self.recalculate_regexps()

    def recalculate_regexps(self):
        self.regexes = [re.compile(p, re.IGNORECASE) for p in self.patterns]