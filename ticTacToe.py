# The purpose of this program is to play a game of tic tac toe.

# Define quit condition that a user can use to end the program right away
def does_player_want_quit(userInput):
    if str(userInput).upper() == "QUIT":
        exit()

# The purpose of this function is to print an introduction message.
def display_introduction():
    introduction_message = "_______________\n" + "| TIC-TAC-TOE |\n" + "|   by l3oxy  |\n" + "|_____________|\n"
    print(introduction_message)
    print("\nEnter 'QUIT' at any time to quit.")

# Have all players choose their icons (e.g. X, O, 7, etc), then return the list.
def pick_icons(number_of_players):
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

    return(player_icons)

# Construct the game board, and return it.
def construct_board(icons_open):
    # Define variables
    board = []
    board_rows = 3
    board_columns = 3

    # Construct the board using the variables above
    for current_row in range(board_rows):
        board.append([])
        for current_column in range(board_columns):
            board[current_row].append(icons_open)

    # Return the board back to the function that calls this function
    return(board)

# Display the current board
def display_board(in_board):
    for row in in_board:
        for spot in row:
            print(spot, end=" ")
        print("\n")

# The purpose of this function is to verify 
def verify_coordinate_input(in_value):
    does_player_want_quit(in_value)
    test_value = int(in_value)
    if test_value in [0, 1, 2]:
        good_value = test_value
        #print("VALID: " + str(in_value) + " -> " + str(good_value)) #DEBUG
        return(good_value)
    else:
        #print("NOT VALID: " + str(in_value)) #DEBUG
        return("Fail")


# The purpose of this function is to prompt for a coordinate, verify if it ...
# meets the requirements, and if so, return it as an int.
def get_coordinate(axis):
    # Prepare prompt
    message = "Enter " + axis + " (0-2): "

    # Enter loop, asking for input, testing it, and repeating until tests successfully.
    verification_result = "Fail"
    while verification_result == "Fail":
        verification_result = verify_coordinate_input(input(message))
    verified_input = verification_result
    return(verified_input)


# The purpose of this function is to place an X/O (depending on who the player is).
def pick(in_board, icons_open, row, col):
    response = "[" + str(row) + "][" + str(col) + "] "

    if in_board[row][col] == icons_open:
        # Spot is open.
        in_board[row][col] = "X" #FIXME: This should be the real players icon
        display_board(in_board)
        return(in_board)
    else:
        # Spot is taken.
        print(response + "is already occupied by " + str(in_board[row][col]))
        display_board(in_board)
        return(False)

# The purpose of this function is to prompt the player (whose turn it is) to
# choose the location for their next icon placement. Then place it there.
def play_turn(board, icons_open):
    # Define variables
    board_update = False

    # Get the coordinates for the next icon placement, and call the function to place them.
    while board_update is False:
        row = get_coordinate("row")
        col = get_coordinate("column")
        board_update = pick(board, icons_open, row, col)

    # Return the now update board
    return(board_update)


# Detect if a player has won horizontaly
# If a player has won horizontaly, return the victor's icon
# If no player has won horizontaly, return False
def victory_horizontal(board, icons_players):
    winner = False

    for row in board:
        icon_left = row[0]
        icon_mid = row[1]
        icon_right = row[2]

        # Test that the left icon is a player (in contrast to being open/unused)
        if icon_left in icons_players:
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
def victory_verticle(board, icons_players):
    total_number_of_columns = 3
    winner = False

    for column in range(total_number_of_columns):
        icon_top = board[0][column]
        icon_middle = board[1][column]
        icon_bottom = board[2][column]

        if icon_top in icons_players:
            if icon_middle == icon_top:
                if icon_bottom == icon_top:
                    winner = icon_top
                    return(winner)

    # This only happens if there is no winner
    return(False)

# Detect if a player has won diagonaly
# If a player has won diagonaly, then return the victor's icon
# If no player has won diagonaly, then return False
def victory_diagonaly():
    #FIXME
    return(False)


# The purpose of this function is to test if either player has won.
# If there is a winner, return the winner's icon.
# If there is not a winner, return False.
def has_anyone_won(board, icons_players, icons_open):
    winner_horizontal = victory_horizontal(board, icons_players)

    if winner_horizontal in icons_players:
        return(winner_horizontal)
    else:
        winner_verticle = victory_verticle(board, icons_players)

        if winner_verticle in icons_players:
            return(winner_verticle)
        else:
            return(False)


# The purpose of this function is to test if there are any spots available.
def any_spots_available(board, icons_open):
    for row in board:
        for spot in row:
            if spot == icons_open:
                return(True)

    print("NO MORE SPOTS")
    return(False)

# The purpose of this function is to test if the game is complete or not.
# If complete and a player won, return victor's icon
# If complete and a tie, return True
# If not complete, return False
def is_game_complete(board, icons_players, icons_open):
    winner = has_anyone_won(board, icons_players, icons_open)

    if winner in icons_players:
        game_winner = winner
        return(game_winner)
    else:
        if any_spots_available(board, icons_open):
            return(False)
        else:
            return(True)

# Go back and forst between all players, having each take a turn until the complete ends.
def play_game(board, icons_players, icons_open):
    current_player = 0
    number_of_players = 2 # FIXME: This should be somewhere else I think.
    game_completion_status = False

    while game_completion_status == False:
        # Let current_player play their turn
        play_turn(board, icons_open)

        # Rotate current player
        current_player += 1
        if current_player >= number_of_players:
            current_player = 0

        # Check if game is complete
        game_completion_status = is_game_complete(board, icons_players, icons_open)

    return(game_completion_status)

def display_result(result):
    1+1
    #game_complete = is_game_complete(board, player_icons, icons_open)
    #while game_complete == False:
    #    play_turn(current_player)
    #    game_complete = is_game_complete(board, player_icons, icons_open)
    #
    #if game_complete in icons_players:
    #    print("Congratulations!\nThe winner is " + str(game_complete))
    #    exit()
    #elif game_complete:
    #    print("That's a Tie! Good Game!")
    #    exit()
    #else:
    #    print("Error: Game ended but cannot determine result")
    #    exit()
    #print("display_result() line 209 about somehting FIXME") #FIXME

# The purpose of this function is to be the mainline/controller function.
def mainline():
    # Define variables
    game_winner = False
    number_of_players = 2
    icons_open = "_"

    #
    display_introduction()
    player_icons = pick_icons(number_of_players)
    board = construct_board(icons_open)
    display_board(board)
    result = play_game(board, player_icons, icons_open)

    #display_result(result) # Wait until display_result is functional before calling it here.

mainline()
