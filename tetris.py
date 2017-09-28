import sys
import random

from PySide2 import QtGui, QtCore, QtWidgets


class Communicate(QtCore.QObject):
    info_msg = QtCore.Signal(str)


class Tetris(QtWidgets.QMainWindow):
    def __init__(self):
        super(Tetris, self).__init__()
        self.setGeometry(300, 300, 180, 480)
        self.setWindowTitle('Tetris')

        self.board = Board(self)
        self.info_board = InfoFrame(self)

        self.setup_ui()

        self.board.msg.info_msg[str].connect(self.info_board.print_msg)
        self.center()

        self.board.start()

    def setup_ui(self):
        main_widget = QtWidgets.QWidget()
        # main_widget.setContentsMargins(1, 1, 1, 1)
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(1, 1, 1, 1)

        board_frame = QtWidgets.QFrame()
        board_frame.setContentsMargins(0, 0, 0, 0)
        board_frame.setFixedSize(182, 382)
        board_frame.setFrameStyle(QtWidgets.QFrame.Panel)

        board_layout = QtWidgets.QHBoxLayout()
        board_layout.setContentsMargins(0, 0, 0, 0)

        board_layout.addWidget(self.board)
        board_frame.setLayout(board_layout)
        layout.addWidget(board_frame)
        layout.addWidget(self.info_board)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def center(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


class Board(QtWidgets.QFrame):
    width = 10
    height = 22
    block_size = 20
    speed = 300

    def __init__(self, parent):
        super(Board, self).__init__(parent)

        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.timer = QtCore.QBasicTimer()
        self.paint_event = 0
        self.timer_event = 0

        self.current_piece = Piece()
        self.next_piece = Piece()

        self.msg = Communicate()

    def start(self):
        self.msg.info_msg.emit('Board started')
        self.new_piece()
        self.timer.start(Board.speed, self)

    def new_piece(self):
        pass

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        rect = self.contentsRect()

        # self.draw_pice()
        # self.paint_event += 1
        self.msg.info_msg.emit('Paint Event ' + str(rect.height()))
        pass
    #
    # def timerEvent(self, event):
    #     # self.timer_event += 1
    #     # self.msg.info_msg.emit('Timer Event ' + str(self.timer_event))
    #     pass


class InfoFrame(QtWidgets.QWidget):
    def __init__(self, parent):
        super(InfoFrame, self).__init__(parent)
        self.info = QtWidgets.QTextEdit()
        self.text = ""
        self.setup_ui()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(1, 1, 1, 1)
        info_frame = QtWidgets.QFrame()
        info_frame.setFrameStyle(QtWidgets.QFrame.Panel)

        info_layout = QtWidgets.QVBoxLayout()
        info_layout.setContentsMargins(1, 1, 1, 1)
        info_layout.setAlignment(QtCore.Qt.AlignTop)

        self.info.setMinimumHeight(50)
        self.info.setReadOnly(1)

        info_frame.setLayout(info_layout)
        info_layout.addWidget(self.info)

        main_layout.addWidget(info_frame)

        self.setLayout(main_layout)

    def print_msg(self, msg):
        self.text = self.text + msg + '\n'
        self.info.setText(self.text)


class Piece(object):
    # pieces order: none, I, Z, S, T, L, J, O
    pieces_loc = ((0, 0, 0, 0),
              (1, 3, 5, 7),
              (2, 4, 5, 7),
              (3, 5, 4, 6),
              (3, 5, 4, 7),
              (2, 3, 5, 7),
              (3, 5, 7, 6),
              (2, 3, 4, 5))

    def __init__(self):
        self.block_loc = []
        self.tetromino = Tetrominoes.no_piece
        self.set_piece(self.tetromino)

    def set_piece(self, tetromino):
        self.block_loc = Piece.pieces_loc[tetromino]
        self.tetromino = tetromino

    def set_random_piece(self):
        self.set_piece(random.randint(1, 7))


class Tetrominoes(object):
    # no_piece added to make it more 'natural' the indexing of the pieces from 1 to 7
    no_piece = 0
    i_piece = 1
    z_piece = 2
    s_piece = 3
    t_piece = 4
    l_piece = 5
    j_piece = 6
    o_piece = 7

def main():
    app = QtWidgets.QApplication(sys.argv)
    t = Tetris()
    t.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()