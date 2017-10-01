import string

values = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
game_over = 0
player_char = {}
game_round = 0


def get_cell(index):
    return values[index]


def draw_board():
    for row in range(6):
        row_txt = ''
        if row % 2 == 0:
            for i in range(7):
                if i%2 == 0:
                    row_txt += '| '
                else:
                    column_index = i / 2
                    row_index = row / 2
                    value_index = 3 * row_index + column_index
                    value = get_cell(value_index)
                    row_txt += value + ' '
        else:
            row_txt += '-' * 13
        print row_txt


def play(player):
    global game_round
    print '------' + player + '------'
    row = get_row()
    col = get_column()
    valid = valid_cell(row,col)
    while not valid:
        print 'Position is not empty'
        row = get_row()
        col = get_column()
        valid = valid_cell(row, col)

    if game_round == 0:
        val = get_value()
        set_player_char(val)

    game_round += 1
    index = 3 * int(row) + int(col)
    values[index] = player_char[player]
    return row, col, player_char[player]


def get_row():
    row = raw_input('Row: ')
    valid = validate_number(row)
    while not valid:
        print ' Enter a number from 0 to 2'
        row = raw_input('Row: ')
        valid = validate_number(row)
    return row


def get_column():
    col = raw_input('Column: ')
    valid = validate_number(col)
    while not valid:
        print ' Enter a number from 0 to 2'
        col = raw_input('Column: ')
        valid = validate_number(col)
    return col


def get_value():
    val = raw_input('Value (X or O): ')
    valid = validate_char(val)
    while not valid:
        print 'Enter X or O'
        val = raw_input('Value (X or O): ')
        valid = validate_char(val)
    return val


def set_player_char(val):
    global player_char
    if val == 'X':
        player_char['player1'] = 'X'
        player_char['player2'] = 'O'
    else:
        player_char['player1'] = 'O'
        player_char['player2'] = 'X'


def validate_number(val):
    if val.isdigit():
        if int(val) in range(3):
            return True
    return False


def validate_char(val):
    if val.isalpha():
        if str(val) in ['X', 'O']:
            return True
    return False


def valid_cell(row,col):
    index = 3 * int(row) + int(col)
    if values[index] == ' ':
        return True
    return False


def check_game_over():
    global game_over
    if game_round == 9:
        game_over = 1


def win_check(row,col,val):
    if check_row_list(row):
        return 1
    # col_list = get_col_list(row)
    # diag_list = get_diag_list(row,col)
    return 0


def check_row_list(row):

    row_list = []
    for i in range(3):
        index = 3 * int(row) + i
        val = values[index]
        if val != ' ':
            row_list.append(val)

    if len(row_list) == 3:
        if len(list(set(row_list))) == 1:
            print 'Game Over'
            draw_board()
            return 1
    return 0


def main():
    while not game_over:
        row, col, val = play('player1')
        if win_check(row, col, val):
            break
        row, col, val = play('player2')
        if win_check(row, col, val):
            break

        draw_board()
        check_game_over()


main()


