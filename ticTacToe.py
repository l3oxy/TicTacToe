# Tic-Tac-Toe
# by l3oxy
# The purpose of this program is to play a game of Tic-Tac-Toe.

# Module importations
import os # This is used by clear_screen()

# The purpose of this function is to print an introduction message.
def display_introduction():
    introduction_message = "_______________\n" + "| TIC-TAC-TOE |\n" + "|   by l3oxy  |\n" + "|_____________|\n"
    print(introduction_message)
    print("\nEnter 'QUIT' at any time to quit.")

# The purpose of this function is to clear the CLI
def clear_screen():
    # Save the output to a recycleBin variable, else the exit-code is printed.
    recycleBin = os.system("clear" if os.name=="posix" else "cls")

# Construct the game board, and return it.
def construct_board(ICONS_OPEN):
    # Define variables
    board = []
    board_rows = 3
    board_columns = 3

    # Construct the board using the variables above
    for current_row in range(board_rows):
        board.append([])
        for current_column in range(board_columns):
            board[current_row].append(ICONS_OPEN)

    # Return the board back to the function that calls this function
    return(board)

# Display the current board
def display_board(board):
    for row in board:
        for spot in row:
            print(spot, end=" ")
        print("\n")

# The purpose of this function is to update the screen.
def update_screen(board, also_print_this=""):
    clear_screen()
    display_introduction()
    display_board(board)
    print(also_print_this)

# Define quit condition that a user can use to end the program right away
def does_player_want_quit(userInput):
    if str(userInput).upper() == "QUIT":
        exit()

# Have all players choose their icons (e.g. X, O, 7, etc), then return the list.
# Returns a list,
#  The 1st value within the list is a list of player icons.
#  The 2nd value within the lsit is a string of the 'open' icon.
def pick_icons(number_of_players, ICONS_OPEN):
    # Define variables.
    icons = []
    player_icons = []

    for playerNumber in range(1, (number_of_players + 1)):
        ask_player_for_input = "Player" + str(playerNumber) + ", pick your icon: "
        current_player_icon_choise_is_valid = False

        while current_player_icon_choise_is_valid != True:
            # Capture player icon choise input.
            playerInput = input(ask_player_for_input)

            # Test if the quit-code was entered.
            does_player_want_quit(playerInput)

            # Verify current player's icon choise has a length of 1.
            playerInputLength = len(playerInput)
            if playerInputLength != 1:
                # If icon choise is too large/long.
                if playerInputLength > 1:
                    print("INVALID: Requires length of 1")
                continue

            # Verify current player hasn't chosen an already selected icon.
            if playerInput in player_icons:
                print("INVALID: That icon has already been selected")
                continue

            # If none of the above tests failed, then the input is good, and
            # this while loop can be ended.
            current_player_icon_choise_is_valid = True

        player_icons.append(playerInput)

    icons.append(player_icons)
    icons.append(ICONS_OPEN)
    return(icons)

# The purpose of this function is to verify that an input is a valid coordinate
def verify_coordinate_input(in_value):
    does_player_want_quit(in_value)
    test_value = int(in_value)
    if test_value in [0, 1, 2]:
        good_value = test_value
        return(good_value)
    else:
        return("Fail")


# The purpose of this function is to prompt for a coordinate, verify if it ...
# meets the requirements, and if so, return it as an int.
def get_coordinate(axis):
    # Prepare prompt
    message = "Choose " + axis + " (0-2): "

    # Enter loop, asking for input, testing it, and repeating until tests successfully.
    verification_result = "Fail"
    while verification_result == "Fail":
        verification_result = verify_coordinate_input(input(message))
    verified_input = verification_result
    return(verified_input)


# The purpose of this function is to place the current player's icon.
def pick(board, current_player, ICONS_OPEN, ICONS_PLAYERS, row, col):
    response = "[" + str(row) + "][" + str(col) + "] "

    if board[row][col] == ICONS_OPEN:
        # Spot is open.
        board[row][col] = ICONS_PLAYERS[current_player]
        update_screen(board)
        return(board)
    else:
        # Spot is taken.
        print(response + "is already occupied by " + str(board[row][col]))
        return(False)

# The purpose of this function is to prompt the current player (whomever that is) to
# choose the location for their next icon placement. Then place it there.
def play_turn(board, current_player, ICONS_PLAYERS, ICONS_OPEN):
    # Define variables
    board_update = False

    # Get the coordinates for the next icon placement, and call the function to place it.
    while board_update is False:
        row = get_coordinate("row")
        col = get_coordinate("column")
        board_update = pick(board, current_player, ICONS_OPEN, ICONS_PLAYERS, row, col)

    # Return the now update board
    return(board_update)


# Detect if a player has won horizontaly
# If a player has won horizontaly, return the victor's icon
# If no player has won horizontaly, return False
def victory_horizontal(board, ICONS_PLAYERS):
    winner = False

    for row in board:
        icon_left = row[0]
        icon_mid = row[1]
        icon_right = row[2]

        # Test that the left icon is a player (in contrast to being open/unused)
        if icon_left in ICONS_PLAYERS:
            # Test if the left, middle, and right, are all the same player
            if icon_left == icon_mid and icon_left == icon_right:
                # If so, then return the winning player
                winner = icon_left
                return(winner)

    # If the control flow gets to this point, then there is no horizontal winner
    return(False)

# The purpose of this function is to detect if a player has win verticaly.
# If a player has won verticaly, return the victor's icon.
# If no player has won verticaly, return False.
def victory_verticle(board, ICONS_PLAYERS):
    total_number_of_columns = 3
    winner = False

    for column in range(total_number_of_columns):
        icon_top = board[0][column]
        icon_middle = board[1][column]
        icon_bottom = board[2][column]

        if icon_top in ICONS_PLAYERS:
            if icon_middle == icon_top:
                if icon_bottom == icon_top:
                    winner = icon_top
                    return(winner)

    # This only happens if there is no winner
    return(False)

# Check if top-left to bottom-right victory
# Return a list,
#  1st list value is if a victory was detected
#  2nd list value is the winner
def victory_diagonaly_topLeft_to_bottomRight(board, ICONS_PLAYERS):
    # Define variables
    icon_top_left = board[0][0]
    icon_center = board[1][1]
    icon_bottom_right = board[2][2]
    returnValue = [False, "null"]

    # Test if the top-left is a player icon
    if icon_top_left in ICONS_PLAYERS:
        # If it is a player icon, then test if others are the same
        if icon_center == icon_top_left and icon_bottom_right == icon_top_left:
            returnValue = [True, icon_top_left]

    return(returnValue)

# Check if top-right to bottom-left victory
# Return a list,
#  1st list value is if a victory was detected
#  2nd list value is the winner
def victory_diagonaly_topRight_to_bottomLeft(board, ICONS_PLAYERS):
    # Define variable
    icon_top_right = board[0][-1]
    icon_center = board[1][1]
    icon_bottom_left = board[-1][0]
    returnValue = [False, "null"]

    # Test if the top-right is a player icon
    if icon_top_right in ICONS_PLAYERS:
        # If it is a player icon, then test if others are the same
        if icon_center == icon_top_right and icon_bottom_left == icon_top_right:
            returnValue = [True, icon_top_right]

    return(returnValue)

# Detect if a player has won diagonaly
# Returns a list,
#  The 1st value in the list is if a victory was detected.
#  The 2nd value in the list the victor's icon. (if no victor, then "null")
def victory_diagonaly(board, ICONS_PLAYERS):
    # Define variables
    TopLeft_to_BottomRight_test = victory_diagonaly_topLeft_to_bottomRight(board, ICONS_PLAYERS)
    TopRight_to_BottomLeft_test = victory_diagonaly_topRight_to_bottomLeft(board, ICONS_PLAYERS)
    diagonal_test_result = [False, "null"]

    # Review test results, and return any result that indicates a victory
    if TopLeft_to_BottomRight_test[0]:
        diagonal_test_result = TopLeft_to_BottomRight_test
    elif TopRight_to_BottomLeft_test[0]:
        diagonal_test_result = TopRight_to_BottomLeft_test

    return(diagonal_test_result)


# The purpose of this function is to test if either player has won.
# If there is a winner, return the winner's icon.
# If there is not a winner, return False.
def has_anyone_won(board, ICONS_PLAYERS, ICONS_OPEN):
    winner_horizontal = victory_horizontal(board, ICONS_PLAYERS)

    if winner_horizontal in ICONS_PLAYERS:
        return(winner_horizontal)
    else:
        winner_verticle = victory_verticle(board, ICONS_PLAYERS)

        if winner_verticle in ICONS_PLAYERS:
            return(winner_verticle)
        else:
            diagonal_victory_test = victory_diagonaly(board, ICONS_PLAYERS)
            if diagonal_victory_test[0]:
                return(diagonal_victory_test[1])
            else:
                return(False)


# The purpose of this function is to test if there are any spots available.
def any_spots_available(board, ICONS_OPEN):
    for row in board:
        for spot in row:
            if spot == ICONS_OPEN:
                return(True)

    print("NO MORE SPOTS")
    return(False)

# The purpose of this function is to test if the game is complete or not.
# If complete and a player won, return victor's icon
# If complete and a tie, return True
# If not complete yet, return False
def is_game_complete(board, ICONS_PLAYERS, ICONS_OPEN):
    winner = has_anyone_won(board, ICONS_PLAYERS, ICONS_OPEN)

    if winner in ICONS_PLAYERS:
        game_winner = winner
        return(game_winner)
    elif any_spots_available(board, ICONS_OPEN):
        return(False)
    else:
        return(True)

# The purpose of this function is to select the next player.
# Expects current_player to be 0-based
# Expects NUMBER_OF_PLAYERS to be 1-based
def next_player(current_player, NUMBER_OF_PLAYERS):
    # new_current_player should be (current_player + 1),
    # unless it would be out of the range of NUMBER_OF_PLAYERS, in which case set to 0.
    if (current_player + 1) >= NUMBER_OF_PLAYERS:
        new_current_player = 0
    else:
        new_current_player = (current_player + 1)

    return(new_current_player)

# Go back and forst between all players, having each take a turn until the complete ends.
def play_game(board, NUMBER_OF_PLAYERS, ICONS_PLAYERS, ICONS_OPEN):
    # Define variables
    current_player = 0
    game_completion_status = False

    while game_completion_status == False:
        # Let current_player play their turn
        play_turn(board, current_player, ICONS_PLAYERS, ICONS_OPEN)

        # Check if game is complete
        game_completion_status = is_game_complete(board, ICONS_PLAYERS, ICONS_OPEN)

        # Rotate current player
        current_player = next_player(current_player, NUMBER_OF_PLAYERS)

    return(game_completion_status)

# The purpose of this function is to display why the game ended.
def display_result(result):
    return()
    #game_complete = is_game_complete(board, player_icons, ICONS_OPEN)
    #while game_complete == False:
    #    play_turn(current_player)
    #    game_complete = is_game_complete(board, player_icons, ICONS_OPEN)
    #
    #if game_complete in ICONS_PLAYERS:
    #    print("Congratulations!\nThe winner is " + str(game_complete))
    #    exit()
    #elif game_complete:
    #    print("That's a Tie! Good Game!")
    #    exit()
    #else:
    #    print("Error: Game ended but cannot determine result")
    #    exit()

# The purpose of this function is to be the mainline/controller function.
def mainline():
    # Define variables
    NUMBER_OF_PLAYERS = 2
    ICONS_OPEN = "_"

    # Call functions
    display_introduction()
    board = construct_board(ICONS_OPEN)
    display_board(board)
    ICONS = pick_icons(NUMBER_OF_PLAYERS, ICONS_OPEN)
    ICONS_PLAYERS = ICONS[0]
    ICONS_OPEN = ICONS[1]
    update_screen(board)
    RESULT = play_game(board, NUMBER_OF_PLAYERS, ICONS_PLAYERS, ICONS_OPEN)

    #display_result(RESULT) # Wait until display_result is functional before calling it here.

mainline()
