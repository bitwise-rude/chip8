def load_game(path:str) -> bytes:
    '''Open a ROM and return the byte codes inside the ROM'''
    file = open(path,'rb')
    data = file.read()
    return data