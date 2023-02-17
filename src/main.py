"""
TapnSwap game.
Main script. Launches the navigation menu (rules, number of players, ...).
"""

# Copyright (C) 2020, Jean-Rémy Conti, ENS Paris-Saclay (France).
# All rights reserved. You should have received a copy of the GNU
# General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

from tapnswap import TapnSwap
from interact import tap_valid_digits, game_1vs1, game_1vsAgent
from agent import Agent, RandomAgent, RLAgent
import os


def main():
    while game_manager():
        continue


def game_manager() -> bool:
    """
    Game manager, used for navigation among different choices offered to user.
    """

    new_frame()
    command_prompt = "Enter Play to start playing or Rules to read the rules.\n"
    command_prompt += "Enter Quit to exit."
    command = pick_option(["PLAY", "RULES", "QUIT"], command_prompt)

    if command == "QUIT":
        return False

    while command == "RULES":
        print_rules()
        print("Enter anything to go back to title.")
        input()
        return True

    new_frame()
    game_mode = pick_option(
        ["Solo", "Versus", "Back"],
        "Do you want to play against the computer or against a friend ? "
        + "Or do you want to go back to title",
    )

    # 1 player
    if game_mode == "SOLO":
        new_frame()
        difficulty_setting = pick_option(
            ["Easy", "Hard", "Back"],
            "Choose the difficulty setting, "
            + "or enter Back to go back to title",
        )

        # Go back
        if difficulty_setting == "BACK":
            return True

        # Define agent
        if difficulty_setting == "EASY":
            agent = RandomAgent()
        else:
            # Load agent
            agent = RLAgent()
            agent.load_model("greedy0_2_vsRandomvsSelf")

        # Ask player's name
        player = input_names(n_players=1)

        # Init scores
        scores = [0, 0]

        # Games
        tapnswap = TapnSwap()
        over = False
        while not over:
            game_over, winner = game_1vsAgent(
                tapnswap, player, agent, greedy=False
            )
            scores[winner] += 1
            if game_over:
                # Display scores
                restart = display_endgame(scores, player, "Computer")
                # Go back
                if not restart:
                    over = True
                    return True

    # 2 players
    if game_mode == "VERSUS":

        # Ask players' name
        player1, player2 = input_names(n_players=2)

        # Init scores
        scores = [0, 0]

        # Games
        tapnswap = TapnSwap()
        over = False
        while not over:
            game_over, winner = game_1vs1(tapnswap, player1, player2)
            scores[winner] += 1
            if game_over:
                # Display scores
                restart = display_endgame(scores, player1, player2)
                # Go back
                if not restart:
                    over = True
                    return True

    if game_mode == "BACK":
        return True


LINE_LENGTH = 80
CENTER_COLUMN = int(LINE_LENGTH / 2)


def pick_option(options, prompt):
    for option in options:
        print(option.center(CENTER_COLUMN) + "\n")
    print("\n" + prompt)
    return get_user_input_between(options).upper()


def get_user_input_between(choices):
    lowercase_choices = [item.lower() for item in choices]
    choice = input(">>> ")
    while choice.lower() not in lowercase_choices:
        choice = input()
    return choice


def input_names(n_players):
    """
    Ask user the names of players.

    Parameter
    ---------
    n_players: int
        Number of human players, 1 or 2.

    Return
    ------
    player or (player1, player2): strings
        Names of players given by user. Return player if n_players = 1.
        Return player1, player2 otherwise.
    """

    header_screen()
    assert n_players in [1, 2], "The number of names must be 1 or 2."

    # 1 human player
    if n_players == 1:
        player = input("Name of player ? \n")
        print()
        return player

    # 2 human players
    player1 = input("Name of 1st player ? \n")
    print()
    print("Name of 2nd player ? ")
    player2 = input()
    while player2 == player1:
        print("Please choose a different name than 1st player")
        player2 = input()
    return player1, player2


def display_endgame(scores, name1, name2) -> bool:
    """
    Print scores at the end of a game and asks user whether to start again.

    Parameters
    ----------
    scores: list of 2 int
        List containing scores of both players.
    name1, name2: str
        Names of players.

    Return
    ------
    bool
        True to play again, False otherwise
    """

    # Print scores
    print("Current scores:\n")
    print(name1 + ": %i" % (scores[0]))
    print(name2 + ": %i" % (scores[1]))
    print("----------------------------")

    # Continue or go back
    print("Another game ? (1 : Yes  |   2 : No)\n")
    restart = tap_valid_digits([1, 2])
    restart = int(restart)
    restart = bool(2 - restart)
    return restart


def new_frame():
    clear_screen()
    header_screen()


def clear_screen() -> None:
    """ 
    Clear console screen on either windows, mac or linux.
    """

    # for windows
    if os.name == "nt":
        _ = os.system("cls")
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system("clear")


def header_screen() -> None:
    """
    Print the game's header.
    """

    clear_screen()
    print("---------------------------------------")
    print(str("TAP 'N SWAP").center(42))
    print("---------------------------------------\n\n")


def print_rules() -> None:
    """
    Display the rules of TapnSwap game on screen.
    """

    header_screen()

    names = ["Player 1", "Player 2"]

    print(
        "TapnSwap is a 2-player game. Both players have a "
        + "variable number of fingers on both of their hands. "
        + "If one player has a hand composed of more than 4 fingers, this "
        + 'hand is "killed". The goal of the game is to kill both hands of '
        + "the opponent player.\n"
    )

    print("--------------")
    print(" First round ")
    print("--------------\n")

    print(
        "Each player starts with 1 finger on each hand and one of them "
        + "has to make the first move. The configuration of hands is then:\n"
    )

    print("-> Press Enter to continue")
    input()

    # Example
    print("Round of", names[0])
    print("----------------------------")
    print()
    print(str(names[1]).center(CENTER_COLUMN))
    print("  |  ".center(CENTER_COLUMN))
    print(
        str(4 * " " + 1 * "|" + "   |   " + 1 * "|" + 4 * " ").center(
            CENTER_COLUMN
        )
    )
    print("  |  ".center(CENTER_COLUMN))
    print("L -------------------- R".center(CENTER_COLUMN))
    print("  |  ".center(CENTER_COLUMN))
    print(
        str(4 * " " + 1 * "|" + "   |   " + 1 * "|" + 4 * " ").center(
            CENTER_COLUMN
        )
    )
    print("  |  ".center(CENTER_COLUMN))
    print(names[0].center(CENTER_COLUMN))
    print()

    print(
        "Both players are separated from each other by the horizontal line. "
        + "The main vertical line separates the hands of both players "
        + "(L: left hands, R: right hands). There is currently 1 finger "
        + "on each hand of each player.\n"
    )

    print("-> Press Enter to continue")
    input()

    print("----------")
    print(" Actions ")
    print("----------\n")

    print(
        "At each round of the game, each player has to choose an action "
        + "among the list of possible actions. There are 2 main kinds of "
        + "actions: tap and swap.\n"
    )

    print(
        "* Tap actions involve adding the number of fingers on one of "
        + "your hands to one of your opponent's hands.\n"
    )

    print(
        "For instance, with the previous initial configuration, Player 1 "
        + "may tap only with 1 (both of Player 1's hands have 1 finger) "
        + "on 1 (both of Player 2's hands have 1 finger). If it happens, "
        + "the configuration of hands at the next round is then:\n"
    )

    print("-> Press Enter to continue")
    input()

    # Example
    print("Round of", names[1])
    print("----------------------------")
    print()
    print(str(names[0]).center(CENTER_COLUMN))
    print("  |  ".center(CENTER_COLUMN))
    print(
        str(4 * " " + 1 * "|" + "   |   " + 1 * "|" + 4 * " ").center(
            CENTER_COLUMN
        )
    )
    print("  |  ".center(CENTER_COLUMN))
    print("L -------------------- R".center(CENTER_COLUMN))
    print("  |  ".center(CENTER_COLUMN))
    print(
        str(3 * " " + 2 * "|" + "   |   " + 1 * "|" + 4 * " ").center(
            CENTER_COLUMN
        )
    )
    print("  |  ".center(CENTER_COLUMN))
    print(names[1].center(CENTER_COLUMN))
    print()

    print(
        "Player 2 had 1 finger on each hand but Player 1 tapped with 1 "
        + "so now Player 2 has one hand with 1+1 = 2 fingers.\n"
    )

    print("-> Press Enter to continue")
    input()

    print("Now let's consider a more complex example:\n")

    # Example
    print("Round of", names[0])
    print("----------------------------")
    print()
    print(str(names[1]).center(CENTER_COLUMN))
    print("  |  ".center(CENTER_COLUMN))
    print(
        str(3 * " " + 2 * "|" + "   |   " + 4 * "|" + 1 * " ").center(
            CENTER_COLUMN
        )
    )
    print("  |  ".center(CENTER_COLUMN))
    print("L -------------------- R".center(CENTER_COLUMN))
    print("  |  ".center(CENTER_COLUMN))
    print(
        str(2 * " " + 3 * "|" + "   |   " + 1 * "|" + 4 * " ").center(
            CENTER_COLUMN
        )
    )
    print("  |  ".center(CENTER_COLUMN))
    print(names[0].center(CENTER_COLUMN))
    print()

    print(
        "It is Player 1's round. Her hands have respectively 3 and 1 "
        + "fingers while Player 2 has hands with 2 and 4 fingers. Player 1 "
        + "can then tap with 3 or 1 on a hand of Player 2, that is on 2 or 4.\n"
    )

    print(
        "Player 1 is able to kill the hand of Player 2 with 2 fingers, "
        + "by tapping with 3 on 2 (3+2 = 5 > 4). The next round is then:\n"
    )

    print("-> Press Enter to continue")
    input()

    # Example
    print("Round of", names[1])
    print("----------------------------")
    print()
    print(str(names[0]).center(CENTER_COLUMN))
    print("  |  ".center(CENTER_COLUMN))
    print(
        str(2 * " " + 3 * "|" + "   |   " + 1 * "|" + 4 * " ").center(
            CENTER_COLUMN
        )
    )
    print("  |  ".center(CENTER_COLUMN))
    print("L -------------------- R".center(CENTER_COLUMN))
    print("  |  ".center(CENTER_COLUMN))
    print(
        str(5 * " " + 0 * "|" + "   |   " + 4 * "|" + 1 * " ").center(
            CENTER_COLUMN
        )
    )
    print("  |  ".center(CENTER_COLUMN))
    print(names[1].center(CENTER_COLUMN))
    print()

    print(
        "Now Player 2 has lost a hand. Notice that Player 1 could have "
        + "killed the hand of Player 2 which has 4 fingers instead, in the "
        + "same way.\n"
    )

    print(
        "* Swap actions consist in exchanging some fingers of one of your "
        + "hand to the other one.\n"
    )

    print(
        "To illustrate this process, let's come back to the previous "
        + "complex example:\n"
    )

    print("-> Press Enter to continue")
    input()

    # Example
    print("Round of", names[0])
    print("----------------------------")
    print()
    print(str(names[1]).center(CENTER_COLUMN))
    print("  |  ".center(CENTER_COLUMN))
    print(
        str(3 * " " + 2 * "|" + "   |   " + 4 * "|" + 1 * " ").center(
            CENTER_COLUMN
        )
    )
    print("  |  ".center(CENTER_COLUMN))
    print("L -------------------- R".center(CENTER_COLUMN))
    print("  |  ".center(CENTER_COLUMN))
    print(
        str(2 * " " + 3 * "|" + "   |   " + 1 * "|" + 4 * " ").center(
            CENTER_COLUMN
        )
    )
    print("  |  ".center(CENTER_COLUMN))
    print(names[0].center(CENTER_COLUMN))
    print()

    print(
        "Instead of tapping with 1 or 3, Player 1 may swap some fingers "
        + "from one of her hands to the other. By swapping 1 finger, "
        + "Player 1 can obtain the configuration of hands 2-2 or 4-0. "
        + "Let's look at the first possibility:\n"
    )

    print("-> Press Enter to continue")
    input()

    # Example
    print("Round of", names[0])
    print("----------------------------")
    print()
    print(str(names[1]).center(CENTER_COLUMN))
    print("  |  ".center(CENTER_COLUMN))
    print(
        str(3 * " " + 2 * "|" + "   |   " + 4 * "|" + 1 * " ").center(
            CENTER_COLUMN
        )
    )
    print("  |  ".center(CENTER_COLUMN))
    print("L -------------------- R".center(CENTER_COLUMN))
    print("  |  ".center(CENTER_COLUMN))
    print(
        str(3 * " " + 2 * "|" + "   |   " + 2 * "|" + 3 * " ").center(
            CENTER_COLUMN
        )
    )
    print("  |  ".center(CENTER_COLUMN))
    print(names[0].center(CENTER_COLUMN))
    print()

    print(
        "By swapping, Player 1 gets the configuration of hands 2-2. "
        + "Changing the hand that loses 1 finger, Player 1 could have "
        + "obtained the configuration 4-0.\n"
    )

    print("-> Press Enter to continue")
    input()

    print(
        "There is one main restriction to swap actions: swapping to an "
        + "identical but reversed configuration is NOT allowed. For "
        + "instance, in this case, Player 1 could not have swapped from "
        + "3-1 to 1-3, exchanging 2 fingers.\n"
    )

    print(
        "But it is still possible to exchange 2 fingers. For instance, "
        + "a swap from 3-2 to 1-4 is a valid swap.\n"
    )

    print("Note that it is also possible to revive a killed hand:\n")

    print("-> Press Enter to continue")
    input()

    # Example
    print("Round of", names[0])
    print("----------------------------")
    print()
    print(str(names[1]).center(CENTER_COLUMN))
    print("  |  ".center(CENTER_COLUMN))
    print(
        str(3 * " " + 2 * "|" + "   |   " + 1 * "|" + 4 * " ").center(
            CENTER_COLUMN
        )
    )
    print("  |  ".center(CENTER_COLUMN))
    print("L -------------------- R".center(CENTER_COLUMN))
    print("  |  ".center(CENTER_COLUMN))
    print(
        str(3 * " " + 2 * "|" + "   |   " + 0 * "|" + 5 * " ").center(
            CENTER_COLUMN
        )
    )
    print("  |  ".center(CENTER_COLUMN))
    print(names[0].center(CENTER_COLUMN))
    print()

    print(
        "In this case, Player 1 has one hand with 2 fingers and a "
        + "killed hand. Exchanging 1 finger from the left to the right, "
        + "Player 1 may revive the killed hand:\n"
    )

    print("-> Press Enter to continue")
    input()

    # Example
    print("Round of", names[0])
    print("----------------------------")
    print()
    print(str(names[1]).center(CENTER_COLUMN))
    print("  |  ".center(CENTER_COLUMN))
    print(
        str(3 * " " + 2 * "|" + "   |   " + 1 * "|" + 4 * " ").center(
            CENTER_COLUMN
        )
    )
    print("  |  ".center(CENTER_COLUMN))
    print("L -------------------- R".center(CENTER_COLUMN))
    print("  |  ".center(CENTER_COLUMN))
    print(
        str(4 * " " + 1 * "|" + "   |   " + 1 * "|" + 4 * " ").center(
            CENTER_COLUMN
        )
    )
    print("  |  ".center(CENTER_COLUMN))
    print(names[0].center(CENTER_COLUMN))
    print()

    print("That's all for the rules, thanks !\n")


if __name__ == "__main__":
    main()
