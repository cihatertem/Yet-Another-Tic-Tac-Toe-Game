"""
Contains Game class and related constants
"""
import os

GAME_LOGO = """
                    .-'''-.                     .-'''-.                     .-'''-.     
                   '   _    \                  '   _    \                  '   _    \   
                 /   /` '.   \               /   /` '.   \               /   /` '.   \  
                .   |     \  '              .   |     \  '              .   |     \  '  
                |   '      |  '             |   '      |  '             |   '      |  ' 
  ____     _____\    \     / /____     _____\    \     / /____     _____\    \     / /  
 `.   \  .'    / `.   ` ..' /`.   \  .'    / `.   ` ..' /`.   \  .'    / `.   ` ..' /   
   `.  `'    .'     '-...-'`   `.  `'    .'     '-...-'`   `.  `'    .'     '-...-'`    
     '.    .'                    '.    .'                    '.    .'                   
     .'     `.                   .'     `.                   .'     `.                  
   .'  .'`.   `.               .'  .'`.   `.               .'  .'`.   `.                
 .'   /    `.   `.           .'   /    `.   `.           .'   /    `.   `.              
'----'       '----'         '----'       '----'         '----' ___   '----'             
                                                            .'/   \                     
         /|                  /|              __.....__     / /     \                    
         ||                  ||          .-''         '.   | |     |                    
         ||                  ||         /     .-''"'-.  `. | |     |                    
         ||  __        __    ||  __    /     /________\   \|/`.   .'                    
         ||/'__ '.  .:--.'.  ||/'__ '. |                  | `.|   |                     
         |:/`  '. '/ |   \ | |:/`  '. '\    .-------------'  ||___|                     
         ||     | |`" __ | | ||     | | \    '-.____...---.  |/___/                     
         ||\    / ' .'.''| | ||\    / '  `.             .'   .'.--.                     
         |/\'..' / / /   | |_|/\'..' /     `''-...... -'    | |    |                    
         '  `'-'`  \ \._,\ '/'  `'-'`                       \_\    /                    
                    `--'  `"                                 `''--'                     
"""
WINNING_LINES = (
    ["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"], ["1", "4", "7"],
    ["2", "5", "8"], ["3", "6", "9"], ["1", "5", "9"], ["3", "5", "7"]
)
GAME_UI = f"""
      (1)  |  (2)  |  (3)
    -----------------------
      (4)  |  (5)  |  (6)
    -----------------------
      (7)  |  (8)  |  (9)
    """


class GAME:
    """
    Creates and initialize "Yet Another Tic-Tac-Toe Game"
    """
    __player1_line: list
    __player2_line: list
    __player_no: int

    def __init__(self):
        self.ui = GAME_UI

    def start(self, new_round=None) -> None:
        """
        Starts, maintains a new Tic-Tac-Toe game
        :param new_round: adjusts clear_screen() usage.
        :return:
        """
        if new_round is None:
            self.clear_screen()
        coin = input("Start A New Game or Quit (y | q): ").lower()

        if coin == "y":
            self.__player1_line = []
            self.__player2_line = []
            self.__player_no = 1
            self.ui = GAME_UI

            is_game_over = False
            while not is_game_over:
                is_game_over = self.player_turn()
            self.start(new_round=True)

    def player_turn(self) -> bool:
        """
        Control players' turns.
        :return:
        """
        self.clear_screen()
        while True:
            print(f"Player{self.__player_no}")
            player_input = self.get_input()
            self.update_game_ui(player_input)
            self.update_player_line_and_player_no(player_input)

            if self.game_over():
                return True

            os.system("clear")
            return False

    def clear_screen(self) -> None:
        """
        Clears previous turn's screen and redraw with uptodate ui
        :return:
        """
        os.system("clear")
        print(GAME_LOGO)
        print("Yet Another Tic-Tac-Toe Game")
        print(self.ui)

    def game_over(self) -> bool:
        """
        Checks win or draw situations.If win/draw, returns True otherwise False
        :return: If win/draw, returns True otherwise False
        """
        self.clear_screen()
        if self.check_winning_line():
            print("Game Over!")
            return True

        if self.is_grid_full():
            print("Game Over: Draw!")
            return True

        return False

    def is_grid_full(self) -> bool:
        """
        Checks game grid is full.
        :return: If grid is full, returns True otherwise False
        """
        all_turns = self.__player1_line + self.__player2_line
        if len(all_turns) == 9:
            return True
        return False

    def get_input(self) -> str:
        """
        Get a grid number from player
        :return: str(player_input)
        """
        while True:
            player_input = input("Enter a grid number: ")
            try:
                player_input = int(player_input)
                if player_input not in range(1, 10):
                    raise IndexError
                elif player_input in self.__player1_line \
                        or player_input in self.__player2_line:
                    raise KeyError
            except ValueError:
                print("Enter only numbers!")
            except IndexError:
                print("Enter a number in range 1:9!")
            except KeyError:
                print("Enter an unused grid number!")
            else:
                return str(player_input)

    def update_player_line_and_player_no(self, player_input) -> None:
        """
        Updates and sorts player's grid line list with player's input and
        next turn's player no attr.
        :param player_input: Player's grid number input
        :return:
        """
        if self.__player_no == 1:
            self.__player1_line.append(player_input)
            self.__player1_line.sort()
            self.__player_no = 2
        elif self.__player_no == 2:
            self.__player2_line.append(player_input)
            self.__player2_line.sort()
            self.__player_no = 1

    def update_game_ui(self, player_input) -> None:
        """
        Updates grid's interface with "X" for player1, "O" for player2
        :param player_input: Player's grid number input
        :return:
        """
        if self.__player_no == 1:
            self.ui = self.ui.replace(player_input, "X")
        elif self.__player_no == 2:
            self.ui = self.ui.replace(player_input, "O")

    def check_winning_line(self) -> bool:
        """
        Checks game winning or draw situations
        :return: bool: Returns True for win or draw otherwise False
        """
        for winning_line in WINNING_LINES:
            if set(winning_line).issubset(set(self.__player1_line)):
                print("Player1 Win!")
                return True
            elif set(winning_line).issubset(set(self.__player2_line)):
                print("Player2 Win!")
                return True

        return False
