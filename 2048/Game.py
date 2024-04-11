import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton, QDialog, QVBoxLayout
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


class RulesWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Правила игры 2048')
        self.setGeometry(200, 200, 100, 100)

        layout = QVBoxLayout()
        self.setLayout(layout)

        rules_label = QLabel("Правила игры 2048:\n\n"
                             "1. Используйте стрелки на клавиатуре, чтобы перемещать плитки.\n"
                             "2. Когда две плитки с одинаковым значением касаются, они объединяются в одну, "
                             "суммируясь.\n"
                             "3. Цель - получить плитку со значением 2048.\n"
                             "---------------------------------------------\n"
                             "НАЖМИТЕ ОК, ЧТОБЫ ПЕРЕЙТИ К ИГРЕ")
        layout.addWidget(rules_label)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.close_rules_and_show_game)
        layout.addWidget(ok_button)

    def close_rules_and_show_game(self):
        self.close()
        self.game_window = Game2048UI()
        self.game_window.show()


class Game2048UI(QWidget):
    def __init__(self):
        super().__init__()
        self.game = Game2048()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        self.setStyleSheet("background-color: #7c29d0;")
        self.score_label = QLabel("Очки за игру: 0")
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        grid.addWidget(self.score_label, 0, 0, 1, 4)
        self.labels = []
        for i in range(4):
            row = []
            for j in range(4):
                label = QLabel("")
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet("font-size: 36px; font-weight: bold; background-color: #ccc; color: white;")
                grid.addWidget(label, i + 1, j)
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

        if self.game.has_won():
            self.show_win_dialog()
        elif self.game.has_lost():
            self.show_lose_dialog()

    def show_win_dialog(self):
        win_dialog = QDialog(self)
        win_dialog.setWindowTitle("Вы выиграли!")
        layout = QVBoxLayout()
        win_dialog.setLayout(layout)
        win_label = QLabel("Поздравляем! Вы собрали плитку 2048 и выиграли.")
        layout.addWidget(win_label)
        ok_button = QPushButton("Ок")
        ok_button.clicked.connect(win_dialog.close)
        layout.addWidget(ok_button)
        win_dialog.exec_()

    def show_lose_dialog(self):
        lose_dialog = QDialog(self)
        lose_dialog.setWindowTitle("Вы проиграли!")
        layout = QVBoxLayout()
        lose_dialog.setLayout(layout)
        lose_label = QLabel("К сожалению, вы проиграли. Больше нет возможных ходов.")
        layout.addWidget(lose_label)
        ok_button = QPushButton("Ок")
        ok_button.clicked.connect(lose_dialog.close)
        layout.addWidget(ok_button)
        lose_dialog.exec_()


    def update_ui(self, board):
        for i in range(4):
            for j in range(4):
                if board[i][j] == 0:
                    self.labels[i][j].setText("")
                    self.labels[i][j].setStyleSheet("background-color: #ccc; color: white;")
                else:
                    self.labels[i][j].setText(str(board[i][j]))
                    color = get_tile_color(board[i][j])
                    self.labels[i][j].setStyleSheet(
                        f"background-color: {color}; color: white; font-size: 36px; font-weight: bold;")
        self.score_label.setText(f"Очки за игру: {self.game.score()}")

    def show_rules_window(self):
        rules_window = RulesWindow()
        rules_window.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    rules_window = RulesWindow()
    rules_window.show()
    sys.exit(app.exec_())
