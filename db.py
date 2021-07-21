class DuckDB:
    def __init__(self, location=None):
        self.location = location
        self.db = []
        if location != None: read(location)

    def parse(self, fd):
        lines = [i.rstrip() for i in fd.readlines()]
        for i in lines:
            self.db.append(DuckEvent(i))

    def output(self, fd):
        for i in self.db:
            fd.write(i.stringify() + "\n")

    def read(self, location):
        fd = open(location, "r")
        self.parse(fd)
        fd.close()

    def write(self, location):
        fd = open(location, "w")
        self.output(fd)
        fd.close

class DuckEvent:
    def __init__(self, line=None):
        self.status = ""
        self.nick = ""
        self.time = None
        self.offset = None
        self.channel = None
        if not line == None: self.internalize(line)

    def internalize(self, line):
        self.status = line[0].upper()
        spl = line.split(' ')
        self.nick = spl[0][1:]
        self.time = float(spl[1])
        self.offset = float(spl[2])
        self.channel = spl[3]

    def stringify(self):
        return "{}{} {} {} {}".format(
            self.status,
            self.nick,
            self.time,
            self.offset,
            self.channel
        )

class DuckStats:
    def __init__(self, db):
        self.db = db

    def countstatus(self, nick, status):
        cnt = 0
        for i in self.db.db:
            if i.status == status and i.nick == nick: cnt += 1
        return cnt

    def cought(self, nick):
        return self.countstatus(nick, "B")

    def missed(self, nick):
        return self.countstatus(nick, "M")

    def ratio(self, nick):
        return (self.cought(nick) / self.missed(nick)) * 100
