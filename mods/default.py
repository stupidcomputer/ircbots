import utils

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

def cmd(line, srv):
    command, params = utils.cmdparse(line)
    if command == "load":
        if utils.is_admin(params[0]):
            try:
                srv.load_mod(params[0])
                utils.message(srv, line.params[0],
                    "loaded: `" + params[0] + "'")
            except ModuleNotFoundError:
                utils.message(srv, line.params[0],
                    "failed to load `" + params[0] + "'")
        else:
            utils.message(srv, line.params[0],
                "invalid permissions!")
    elif command == "unload":
        if utils.is_admin(params[0]):
            try:
                srv.unload_mod(params[0])
                utils.message(srv, line.params[0],
                    "unloaded: `" + params[0] + "'")
            except:
                utils.message(srv, line.params[0],
                    "failed to unload `" + params[0] + "'")
        else:
            utils.message(srv, line.params[0],
                "invalid permissions!")
    elif command == "op":
        if utils.is_admin(params[0]):
            srv.admins.append(Admin(params[0]))
            utils.message(srv, line.params[0],
                "operator added")
        else:
            utils.message(srv, line.params[0],
                "invalid permissions!")
