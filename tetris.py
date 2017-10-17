import sys
import random

from PySide2 import QtGui, QtCore, QtWidgets


class Communicate(QtCore.QObject):
    info_msg = QtCore.Signal(str)


class Tetris(QtWidgets.QMainWindow):
    def __init__(self):
        super(Tetris, self).__init__()
        self.setWindowTitle('Tetris')

        self.board = Board(self)
        self.info_board = InfoFrame(self)

        self.setup_ui()

        self.board.msg.info_msg[str].connect(self.info_board.print_msg)

        self.setFixedSize(300, self.board.frameRect().height())
        self.center()

        self.board.start()

    def setup_ui(self):
        main_widget = QtWidgets.QWidget()
        # main_widget.setContentsMargins(1, 1, 1, 1)
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(1, 1, 1, 1)

        board_frame = QtWidgets.QFrame()
        board_frame.setContentsMargins(0, 0, 0, 0)
        board_frame.setFrameStyle(QtWidgets.QFrame.Panel)
        board_frame.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

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
    block_size = 15
    speed = 400

    def __init__(self, parent):
        super(Board, self).__init__(parent)
        self.setFixedSize(Board.width * Board.block_size, Board.height * Board.block_size)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.timer = QtCore.QBasicTimer()
        self.paint_event = 0
        self.timer_event = 0

        self.x = 0
        self.y = 0
        self.current_piece = Piece()
        # self.next_piece = Piece()

        self.msg = Communicate()

    def start(self):
        self.msg.info_msg.emit('Board started')
        self.new_piece()
        self.timer.start(Board.speed, self)

    def new_piece(self):
        self.current_piece.set_random_piece()
        self.msg.info_msg.emit('Piece is ' + str(self.current_piece.num))

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        for b in self.current_piece.blocks:
            block_x = self.x + (b % 2) * Board.block_size
            block_y = self.y - (b / 2 - 3) * Board.block_size
            self.draw_block(painter, block_x, block_y)
        # self.paint_event += 1
        # self.msg.info_msg.emit('Paint Event ' + str(rect.height()))
        # print ('Board top {0}, square height {1}'.format(board_top, square_height))
        pass

    def timerEvent(self, event):
        self.y += Board.block_size
        self.update()
        # QtWidgets.QFrame.timerEvent(self, event)

    def draw_block(self, painter, x, y):
        color_table = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        color = QtGui.QColor(color_table[self.current_piece.num])
        # print ('piece num {0}, x: {1}, y: {2}'.format(self.current_piece.num, x, y))
        painter.fillRect(x - 1, y - 1, Board.block_size, Board.block_size, color)
        painter.fillRect(x - 1, y - 1, Board.block_size, Board.block_size, color)


        painter.setPen(color.lighter())
        painter.drawLine(x, y + Board.block_size - 1, x, y)
        painter.drawLine(x, y, x + Board.block_size - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + Board.block_size - 1, x + Board.block_size - 1, y + Board.block_size - 1)
        painter.drawLine(x + Board.block_size - 1, y + Board.block_size - 1, x + Board.block_size - 1, y + 1)


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
    # tuple containing the blocks. the pieces will fit inside a 2 X 4 grid, cell count starts top left with 0.
    # pieces order: I, Z, S, T, L, J, O
    pieces = ((1, 3, 5, 7),
              (2, 4, 5, 7),
              (3, 5, 4, 6),
              (3, 5, 4, 7),
              (2, 3, 5, 7),
              (3, 5, 7, 6),
              (2, 3, 4, 5))

    def __init__(self):
        self.blocks = []
        self.num = 0

    def set_piece(self, num):
        self.blocks = Piece.pieces[num]
        self.num = num

    def set_random_piece(self):
        self.set_piece(random.randint(0, 6))


def main():
    app = QtWidgets.QApplication(sys.argv)
    t = Tetris()
    t.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()