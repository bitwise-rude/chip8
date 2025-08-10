from file_manager import load_game
from interpreter import Interpreter
from visuals import Screen


loaded_rom = load_game("Games\\TANK.ch8")

game_screen = Screen()

interpreter = Interpreter(loaded_rom,game_screen)
    

while True:
    if interpreter.step()== False:
        break
    