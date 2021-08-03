def cmd(line, srv):
    splitted = line.params[1].split(' ')
    command = splitted[0][1:]
    if command == "load":
        srv.load_mod(splitted[1])
        print("loaded")
