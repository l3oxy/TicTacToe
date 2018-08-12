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
        for coord in row:
            print(" " + coord, end="")
        print("\n")

# The purpose of this function is to update the screen.
def update_screen(board, also_print_this=""):
    clear_screen()
    display_introduction()
    display_board(board)
    if also_print_this:
        print(also_print_this)

# Define quit condition that a user can use to end the program right away
def does_player_want_quit(userInput):
    if userInput.upper() == "QUIT":
        exit()

# Have all players choose their icons (e.g. X, O, 7, etc), then return the list.
# Returns a list,
#  The 1st value within the list is a list of player icons.
#  The 2nd value within the lsit is a string of the 'open' icon.
def pick_player_icons(number_of_players):
    # Define variables.
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
                # If icon choise is too large/long tell the player.
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

        # Add the new player icon to the list of player icons.
        player_icons.append(playerInput)

    # Return the list of player icons.
    return(player_icons)

# The purpose of this function is to verify that an input is a valid coordinate
# Returns a dict that says what the value is , and if it is valid.
def is_valid_coordinate(test_value):
    # Define variable
    accaptable_ints = [0,1,2]
    validity_test = {"int":None, "is_valid?":False}

    # Verify that it is not the quit code
    does_player_want_quit(test_value)

    # Test if the value is valid
    if test_value.isdigit():
        validity_test["int"] = int(test_value)
        if validity_test["int"] in accaptable_ints:
            validity_test["is_valid?"] = True

    # Return the results
    return(validity_test)

# The purpose of this function is to prompt for a coordinate, verify if it ...
# meets the requirements, and if so, return it as an int.
def get_coordinate(ICONS_PLAYERS, current_player, axis):
    # Prepare prompt
    message = "[" + ICONS_PLAYERS[current_player] + "] Choose " + axis + " (0-2): "

    # Enter loop, asking for input, testing it, and repeating until tests successfully.
    coordinate_test = is_valid_coordinate(input(message))
    while coordinate_test["is_valid?"] != True:
        coordinate_test = is_valid_coordinate(input(message))

    verified_input = coordinate_test["int"]
    return(verified_input)


# The purpose of this function is to place the current player's icon.
def pick(board, current_player, ICONS, row, col):
    response = "[" + str(row) + "][" + str(col) + "] "

    if board[row][col] == ICONS["OPEN"]:
        # Spot is open.
        board[row][col] = ICONS["PLAYERS"][current_player]
        update_screen(board)
        return(board)
    else:
        # Spot is taken.
        print(response + "is already occupied by " + str(board[row][col]))
        return(False)

# The purpose of this function is to prompt the current player (whomever that is) to
# choose the location for their next icon placement. Then place it there.
def play_turn(board, current_player, ICONS):
    # Define variables
    board_update = False

    # Get the coordinates for the next icon placement, and call the function to place it.
    while board_update is False:
        row = get_coordinate(ICONS["PLAYERS"], current_player, "row")
        col = get_coordinate(ICONS["PLAYERS"], current_player, "column")
        board_update = pick(board, current_player, ICONS, row, col)

    # Return the now update board
    return(board_update)


# Detect if a player has won horizontaly, and if so then whom
# If a player has won horizontaly, return the victor's icon
# If no player has won horizontaly, return None
def victory_horizontal(board, ICONS_PLAYERS):
    detected_horizontal_winner = None

    for row in board:
        icon_left = row[0]
        icon_mid = row[1]
        icon_right = row[2]

        # Test that the left icon is a player (in contrast to being open/unused)
        if icon_left in ICONS_PLAYERS:
            # Test if the left, middle, and right, are all the same player
            if icon_left == icon_mid and icon_left == icon_right:
                # If so, then return the winning player
                detected_horizontal_winner = icon_left

    return(detected_horizontal_winner)

# The purpose of this function is to detect if a player has win verticaly.
# If a player has won verticaly, return the victor's icon.
# If no player has won verticaly, return None.
def victory_vertical(board, ICONS_PLAYERS):
    # Define variables
    total_number_of_columns = len(board[0])
    detected_vertical_winner = None

    # For each column
    for column in range(total_number_of_columns):
        # Capture all rows within the current column
        icon_top = board[0][column]
        icon_middle = board[1][column]
        icon_bottom = board[2][column]

        # Check if all in column are the same player
        if icon_top in ICONS_PLAYERS:
            if icon_middle == icon_top:
                if icon_bottom == icon_top:
                    detected_vertical_winner = icon_top
                    break

    return(detected_vertical_winner)

# Check if top-left to bottom-right victory
# The winner, else if no winner this returns None
def victory_diagonaly_topLeft_to_bottomRight(board, ICONS_PLAYERS):
    # Define variables
    icon_top_left = board[0][0]
    icon_center = board[1][1]
    icon_bottom_right = board[2][2]
    detected_TLBR_winner = None  # TLBR is shorthand for 'Top-Left to Bottom-Right'

    # Test if the top-left is a player icon
    if icon_top_left in ICONS_PLAYERS:
        # If it is a player icon, then test if others are the same
        if icon_center == icon_top_left and icon_bottom_right == icon_top_left:
            detected_TLBR_winner = icon_top_left

    return(detected_TLBR_winner)

# Check if top-right to bottom-left victory
# If there is a winner, return winner's icon. Else return None
def victory_diagonaly_topRight_to_bottomLeft(board, ICONS_PLAYERS):
    # Define variable
    icon_top_right = board[0][-1]
    icon_center = board[1][1]
    icon_bottom_left = board[-1][0]
    detected_TRBL_winner = None # TRBL is shorthand for 'Top-Right to Bottom-Left'

    # Test if the top-right is a player icon
    if icon_top_right in ICONS_PLAYERS:
        # If it is a player icon, then test if others are the same
        if icon_center == icon_top_right and icon_bottom_left == icon_top_right:
            detected_TRBL_winner = icon_top_right

    return(detected_TRBL_winner)

# Detect if a player has won diagonaly
# If a player diagonaly this returns the winner's icon, ...
# ... else if there is no winner, this returns None
def victory_diagonal(board, ICONS_PLAYERS):
    # Define variables
    TopLeft_to_BottomRight_test = victory_diagonaly_topLeft_to_bottomRight(board, ICONS_PLAYERS)
    TopRight_to_BottomLeft_test = victory_diagonaly_topRight_to_bottomLeft(board, ICONS_PLAYERS)
    diagonal_test_result = None

    # Review test results, and return any winner
    if TopLeft_to_BottomRight_test in ICONS_PLAYERS:
        diagonal_test_result = TopLeft_to_BottomRight_test
    elif TopRight_to_BottomLeft_test in ICONS_PLAYERS:
        diagonal_test_result = TopRight_to_BottomLeft_test

    return(diagonal_test_result)


# The purpose of this function is to test if either player has won.
# If there is a winner, return the winner's icon.
# If there is not a winner, return False.
def has_anyone_won(board, ICONS_PLAYERS, ICONS_OPEN):
    # Define variables
    victory_result = {"win_detected?":False, "winner":None}

    # For each way to win (verticle, horizontal, diagonal), test that way.
    for victory_method in [victory_horizontal, victory_vertical, victory_diagonal]:
        victory_method_result = victory_method(board, ICONS_PLAYERS)
        if victory_method_result in ICONS_PLAYERS:
            victory_result["winner"] = victory_method_result
            victory_result["win_detected?"] = True
            break

    # Return dict that lists if any wins were detected, and if so includes the winner.
    return(victory_result)

# The purpose of this function is to test if there are any spots available.
def board_out_of_spots(board, ICONS_OPEN):
    for row in board:
        for coordinate in row:
            if coordinate == ICONS_OPEN:
                return(False)

    return(True)

# The purpose of this function is to test if the game is complete or not.
# If complete and a player won, return victor's icon
# If complete and a tie, return True
# If not complete yet, return False
def is_game_complete(board, ICONS_PLAYERS, ICONS_OPEN):
    has_anyone_won_result = has_anyone_won(board, ICONS_PLAYERS, ICONS_OPEN)

    if has_anyone_won_result["win_detected?"]:
        game_winner = has_anyone_won_result["winner"]
        return(game_winner)
    else:
        return(board_out_of_spots(board, ICONS_OPEN))

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
def play_game(board, NUMBER_OF_PLAYERS, ICONS):
    # Define variables
    current_player = 0
    game_completion_status = False
    ICONS_OPEN = ICONS["OPEN"]
    ICONS_PLAYERS = ICONS["PLAYERS"]

    while game_completion_status == False:
        # Let current_player play their turn
        play_turn(board, current_player, ICONS)

        # Check if game is complete
        game_completion_status = is_game_complete(board, ICONS_PLAYERS, ICONS_OPEN)

        # Rotate current player
        current_player = next_player(current_player, NUMBER_OF_PLAYERS)

    return(game_completion_status)

# The purpose of this function is to display why the game ended.
def display_result(board, RESULT, ICONS_PLAYERS):
    if RESULT in ICONS_PLAYERS:
        update_screen(board, "Congratulations!\nThe winner is " + RESULT)
    elif RESULT == True:
        # If there are no spots available, and nobody has won.
        update_screen(board, "That's a Tie! Good Game!")
    else:
       print("Error: Game ended but cannot determine result")
       exit()

# The purpose of this function is to be the mainline/controller function.
def mainline():
    # Define variables
    NUMBER_OF_PLAYERS = 2
    ICONS = {"OPEN": "_"}

    # Call functions
    display_introduction()
    board = construct_board(ICONS["OPEN"])
    display_board(board)
    ICONS["PLAYERS"] = pick_player_icons(NUMBER_OF_PLAYERS)
    update_screen(board)
    RESULT = play_game(board, NUMBER_OF_PLAYERS, ICONS)
    display_result(board, RESULT, ICONS["PLAYERS"])

mainline()
