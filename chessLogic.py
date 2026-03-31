class Board:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
    def getPiece(self, row, col):
        return self.board[row][col]

    def esteMutareValida(self, rand_init, col_init, rand_final, col_final):
        piesa = self.board[rand_init][col_init][1]
        culoare_piesa = self.board[rand_init][col_init][0]

        if piesa == "N":
            diff_rand = abs(rand_final - rand_init)
            diff_col = abs(col_final - col_init)
            if (diff_rand == 2 and diff_col == 1) or (diff_rand == 1 and diff_col == 2):
                return True
            return False

        elif piesa == "R":
            if rand_final == rand_init:
                pas = 1 if col_final > col_init else -1
                for j in range(col_init + pas, col_final, pas):
                    if self.board[rand_init][j] != "":
                        return False
                return True
            elif col_final == col_init:
                pas = 1 if rand_final > rand_init else -1
                for i in range(rand_init + pas, rand_final, pas):
                    if self.board[i][col_init] != "":
                        return False
                return True
            return False

        elif piesa == "B":
            diff_rand = abs(rand_final - rand_init)
            diff_col = abs(col_final - col_init)

            if diff_rand == diff_col and diff_rand > 0:
                pas_rand = 1 if rand_final > rand_init else -1
                pas_col = 1 if col_final > col_init else -1

                for i in range(1, diff_rand):
                    rand_curent = rand_init + (i * pas_rand)
                    col_curent = col_init + (i * pas_col)
                    if self.board[rand_curent][col_curent] != "":
                        return False
                return True
            return False


        elif piesa == "Q":
            if rand_init == rand_final:
                pas = 1 if col_final > col_init else -1
                for j in range(col_init + pas, col_final, pas):
                    if self.board[rand_init][j] != "":
                        return False
                return True

            elif col_init == col_final:
                pas = 1 if rand_final > rand_init else -1
                for i in range(rand_init + pas, rand_final, pas):
                    if self.board[i][col_init] != "":
                        return False
                return True

            elif abs(rand_final - rand_init) == abs(col_final - col_init) and abs(rand_final - rand_init) > 0:
                diff = abs(rand_final - rand_init)
                pas_rand = 1 if rand_final > rand_init else -1
                pas_col = 1 if col_final > col_init else -1

                for i in range(1, diff):
                    if self.board[rand_init + i * pas_rand][col_init + i * pas_col] != "":
                        return False
                return True
            return False


        elif piesa == "K":
            if (abs(rand_final - rand_init) < 2) and (abs(col_final - col_init) < 2):
                return True
            elif culoare_piesa == "w":
                # ROCADA PENTRU ALB
                if rand_init == 7 and col_init == 4:  # si n-a mai mutat regele si nu e in sah etc
                    if rand_final == 7:
                        # ROCADA MARE
                        if col_final == 2 and len(self.board[7][0]) > 1 and self.board[7][0][1] == "R":
                            self.board[7][3] = self.board[7][0]
                            self.board[7][0] = ""
                            return True
                        # ROCADA MICA
                        elif col_final == 6 and len(self.board[7][7]) > 1 and self.board[7][7][1] == "R":
                            self.board[7][5] = self.board[7][7]
                            self.board[7][7] = ""
                            return True
                    return False
                return False

                # ROCADA PENTRU NEGRU
            elif culoare_piesa == "b":
                if rand_init == 0 and col_init == 4:  # si n-a mai mutat regele si nu e in sah etc
                    if rand_final == 0:
                        # ROCADA MARE
                        if col_final == 2 and len(self.board[0][0]) > 1 and self.board[0][0][1] == "R":
                            self.board[0][3] = self.board[0][0]
                            self.board[0][0] = ""
                            return True
                        # ROCADA MICA
                        elif col_final == 6 and len(self.board[0][7]) > 1 and self.board[0][7][1] == "R":
                            self.board[0][5] = self.board[0][7]
                            self.board[0][7] = ""
                            return True
                    return False
                return False


        elif piesa == "P":
            if culoare_piesa == "w":
                # MERS IN FATA CATE 1
                if rand_final == rand_init - 1 and col_final == col_init and self.board[rand_final][col_final] == "":
                    return True
                # PRIMA MUTARE CATE 2
                elif rand_init == 6 and rand_final == rand_init - 2 and col_final == col_init:
                    if self.board[rand_init - 1][col_init] == "" and self.board[rand_final][col_final] == "":
                        return True
                # CAPTURARE
                elif rand_final == rand_init - 1 and abs(col_final - col_init) == 1:
                    if self.board[rand_final][col_final] != "" and self.board[rand_final][col_final].startswith("b"):
                        return True
                return False

                # EN PASSANT

            # ANALOG PENTRU NEGRU
            elif culoare_piesa == "b":
                if rand_final == rand_init + 1 and col_final == col_init and self.board[rand_final][col_final] == "":
                    return True
                elif rand_init == 1 and rand_final == rand_init + 2 and col_final == col_init:
                    if self.board[rand_init + 1][col_init] == "" and self.board[rand_final][col_final] == "":
                        return True
                elif rand_final == rand_init + 1 and abs(col_final - col_init) == 1:
                    if self.board[rand_final][col_final] != "" and self.board[rand_final][col_final].startswith("w"):
                        return True
                return False


