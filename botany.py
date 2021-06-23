import json
import time
import os

class Botany:
    visitors = "/home/{}/.botany/visitors.json"
    plant = "/home/{}/.botany/{}_plant_data.json"
    def __init__(self, user):
        self.user = user
        self.euser = user.lower()
    def getVisitors(self):
        formatted = self.visitors.format(self.euser)
        try:
            if os.stat(formatted).st_size > 0:
                with open(formatted) as fd:
                    return json.load(fd)
            else:
                return []
        except FileNotFoundError:
            print("FileNotFoundError in getVisitors()")
            return False
    def insertVisitor(self, data, waterer):
        if data == False: return False
        formatted = self.visitors.format(self.euser)
        data.append({"timestamp": int(time.time()), "user": waterer})
        try:
            with open(formatted, "w") as fd:
                json.dump(data, fd, indent=4)
                return True
        except PermissionError:
            print("PermissionError in insertVisitor()")
            return False
        except FileNotFoundError:
            print("FileNotFoundError in insertVisitor()")
            return False
    def getInfo(self):
        formatted = self.plant.format(self.euser, self.euser)
        try:
            with open(formatted) as fd:
                return json.load(fd)
        except:
            print("error in getInfo()")
            return []
    def score(self):
        i = self.getInfo()
        if len(i) > 1: return i['score'] + min(i['last_watered'] - int(time.time()), 24 * 3600) * 0.2 * (i['generation'] - 1) + 1
        return 0

class IRCBotany(Botany):
    def plantDescription(self):
        string = ""
        data = self.getInfo()
        if(data == []): return "{}'s invisible plant".format(self.euser)

        string += self.euser
        print(self.euser)
        string += "'s "
        if(data['is_dead']): string += "dead "
        string += data['description']
        string += ' '
        string += "generation "
        string += str(data['generation'])
        string += ' '
        string += "plant"

        return string

    def cantWater(self):
        return "I can't water {}!".format(self.plantDescription())

    def watered(self):
        return "I watered {}!".format(self.plantDescription())

    def dead(self):
        return "Your {} is dead!".format(self.plantDescription())

    def water(self, waterer):
        return self.insertVisitor(self.getVisitors(), waterer)
