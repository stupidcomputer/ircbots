from ircrobots.glob import compile as gcompile

class Nicklist:
    def __init__(self):
        self.nick = []
        self.hostnick = []
    def __str__(self):
        return ' '.join(self.nick + self.hostnick)
    def __len__(self):
        return len(self.nick) + len(self.hostnick)
    def __contains__(self, item):
        if gcompile("*!*@*").match(item):
            return item in self.hostnick
        else:
            return item in self.nick
    def append(self, mask):
        if gcompile("*!*@*").match(mask):
            self.hostnick.append(mask)
        elif not mask in self.nick:
            self.nick.append(mask)
        return 1
    def remove(self, mask):
        try:
            if gcompile("*!*@*").match(mask):
                self.hostnick.remove(mask)
            else:
                self.nick.remove(mask)
            return 1
        except ValueError:
            return 0
    def host(self):
        return self.hostnick
    def nick(self):
        return nick
    def write(self, name):
        fd = open(name + "nick", "w")
        fd.writelines(i + "\n" for i in self.nick)
        fd.close()

        fd = open(name + "mask", "w")
        fd.writelines(i + "\n" for i in self.hostnick)
        fd.close()
        return 1
    def read(self, name):
        fd = open(name + "nick", "r")
        for i in fd.readlines():
            self.nick.append(i.rstrip("\n"))
        fd.close()

        fd = open(name + "mask", "r")
        for i in fd.readlines():
            self.hostnick.append(i.rstrip("\n"))
        fd.close()
        return 1
