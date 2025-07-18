from irctokens import build

# This file is part of modbot.

# modbot is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any
# later version.

# modbot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero
# General Public License along with modbot.  If not, see
# <https://www.gnu.org/licenses/>.

def message(srv, channel, msg):
    srv.send(build("PRIVMSG", [channel, msg]))

def cmdparse(line):
    splitted = line.params[1].split(' ')
    try: command = splitted[0][1:]
    except IndexError: command = None
    try: params = splitted[1:]
    except IndexError: params = None
    return (command, params)

def is_admin(srv, nick):
    return nick in srv.admins


