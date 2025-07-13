class ChannelDB:
    def __init__(self, location=None):
        self.channels = []
        if not location == None:
            self.read(location)

    def read(self, location):
        fd = open(location, "r")
        [self.channels.append(i.rstrip()) for i in fd.readlines()]
        fd.close()

    def add(self, channel):
        self.channels.append(channel)

    def remove(self, channel):
        self.channels.remove(channel)

    def list(self):
        return self.channels

    def write(self, location):
        fd = open(location, "w")
        [fd.write(i + "\n") for i in self.channels]
        fd.close()
