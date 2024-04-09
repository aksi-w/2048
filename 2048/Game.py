import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel
from PyQt5.QtCore import Qt
from Logic import Game2048


def get_tile_color(value):
    colors = {
        2: "#b66fd1",
        4: "#a854c8",
        8: "#993cbd",
        16: "#8333a2",
        32: "#6d2b87",
        64: "#57226c",
        128: "#d1a6e2",
        256: "#471777",
        512: "#3c1159",
        1024: "#4f1c71",
        2048: "#280b3b"
    }
    return colors.get(value, "#ccc")


class Game2048UI(QWidget):
    def __init__(self):
        super().__init__()
        self.game = Game2048()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.labels = []
        for i in range(4):
            row = []
            for j in range(4):
                label = QLabel("")
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet("font-size: 36px; font-weight: bold; background-color: #ccc;")
                grid.addWidget(label, i, j)
                row.append(label)
            self.labels.append(row)

        self.setWindowTitle('2048')
        self.setGeometry(100, 100, 400, 500)
        self.setFocus()
        self.update_ui(self.game.board)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.game.board = self.game.move_tiles(self.game.board, "left")
        elif event.key() == Qt.Key_Right:
            self.game.board = self.game.move_tiles(self.game.board, "right")
        elif event.key() == Qt.Key_Up:
            self.game.board = self.game.move_tiles(self.game.board, "up")
        elif event.key() == Qt.Key_Down:
            self.game.board = self.game.move_tiles(self.game.board, "down")
        self.game.board = self.game.add_random_tile(self.game.board)
        self.update_ui(self.game.board)

    def update_ui(self, board):
        for i in range(4):
            for j in range(4):
                if board[i][j] == 0:
                    self.labels[i][j].setText("")
                    self.labels[i][j].setStyleSheet("background-color: #ccc;")
                else:
                    self.labels[i][j].setText(str(board[i][j]))
                    color = get_tile_color(board[i][j])
                    self.labels[i][j].setStyleSheet(
                        f"background-color: {color}; color: white; font-size: 36px; font-weight: bold;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Game2048UI()
    game.show()
    sys.exit(app.exec_())
