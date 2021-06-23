class Admin:
    def __init__(self, nick):
        self.nicks = []
        self.nicks.append(nick)
    def __eq__(self, val):
        return val in self.nicks
    def append(self, nick):
        self.nicks.append(nick)
    def remove(self, nick):
        self.nicks.remove(nick)
