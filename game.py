from board import Board,NotValidMoveException
def main():
    board = Board()
    while not board.check()[0]:
        try:
            print('Make a move: ')
            board.make_move('x')
            print()
        except (ValueError,NotValidMoveException) as e:
            print(e)
            print('That was not a valid move.')
            continue
        if board.check()[0]:
            print('You have won!')
            return board.check()[1]
        print('Computer made a move: ')
        board.computer_move()
        if board.check()[0]:
            print('Computer have won!')
            return board.check()[1]

main()