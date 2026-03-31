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
        if rand_init == rand_final and col_init == col_final:
            return False

        culoare_piesa = self.board[rand_init][col_init][0]
        piesa_destinatie = self.board[rand_final][col_final]
        if piesa_destinatie != "" and piesa_destinatie.startswith(culoare_piesa):
            return False

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
                        if col_final == 2 and self.board[7][0] == "wR":
                            if self.board[7][1] == "" and self.board[7][2] == "" and self.board[7][3] == "":
                                if (not self.estePatratAtacat(7, 4, "w") and
                                        not self.estePatratAtacat(7, 3,"w") and not self.estePatratAtacat(
                                        7, 2, "w")):
                                    return True
                            # ROCADA MICA
                        elif col_final == 6 and self.board[7][7] == "wR":
                            if self.board[7][5] == "" and self.board[7][6] == "":
                                if (not self.estePatratAtacat(7, 4, "w") and
                                        not self.estePatratAtacat(7, 5,"w") and not self.estePatratAtacat(
                                        7, 6, "w")):
                                    return True
                    return False
                return False

                # ROCADA PENTRU NEGRU
            elif culoare_piesa == "b":
                if rand_init == 0 and col_init == 4:  # si n-a mai mutat regele si nu e in sah etc
                    if rand_final == 0:
                        # ROCADA MARE
                        if col_final == 2 and self.board[0][0] == "bR":
                            if self.board[0][1] == "" and self.board[0][2] == "" and self.board[0][3] == "":
                                if (not self.estePatratAtacat(0, 4, "b") and
                                        not self.estePatratAtacat(0, 3,"b") and not self.estePatratAtacat(
                                        0, 2, "b")):
                                    return True
                            # ROCADA MICA
                        elif col_final == 6 and self.board[0][7] == "bR":
                            if self.board[0][5] == "" and self.board[0][6] == "":
                                if (not self.estePatratAtacat(0, 4, "b") and
                                        not self.estePatratAtacat(0, 5,"b") and not self.estePatratAtacat(
                                        0, 6, "b")):
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

    def getKingPos(self, culoare):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == f"{culoare}K":
                    return i,j
        return -1, -1

    def esteSah(self, culoare):
        rand_rege, col_rege = self.getKingPos(culoare)
        for i in range(8):
            for j in range(8):
                piesa = self.board[i][j]
                if piesa != "" and not piesa.startswith(culoare):
                    if self.esteMutareValida(i, j, rand_rege, col_rege):
                        return True
        return False

    def faraMutariValide(self, culoare):
        # parcurg toate mutarile posibile de pe tabla
        for rand_init in range(8):
            for col_init in range(8):
                piesa = self.board[rand_init][col_init]

                if piesa != "" and piesa.startswith(culoare):
                    for rand_final in range(8):
                        for col_final in range(8):
                            if self.esteMutareValida(rand_init, col_init, rand_final, col_final):
                                piesa_destinatie = self.board[rand_final][col_final]

                                self.board[rand_final][col_final] = piesa
                                self.board[rand_init][col_init] = ""

                                totSah = self.esteSah(culoare)

                                self.board[rand_final][col_final] = piesa_destinatie
                                self.board[rand_init][col_init] = piesa

                                if not totSah:
                                    return False
        return True

    def esteMat(self, culoare):
        return self.esteSah(culoare) and self.faraMutariValide(culoare)

    def estePat(self, culoare):
        return (not self.esteSah(culoare)) and self.faraMutariValide(culoare)

    def estePatratAtacat(self, rand, col, culoare_aparator):
        culoare_atacator = "b" if culoare_aparator == "w" else "w"
        for i in range(8):
            for j in range(8):
                piesa = self.board[i][j]

                if piesa != "" and piesa.startswith(culoare_atacator):
                    if(piesa[1] == "K"):
                        if abs(rand - i) <= 1 and abs(rand - j) <= 1:
                            return True
                        else:
                            if self.esteMutareValida(i,j,rand,col):
                                return True
        return False

    def proceseazaRocada(self, piesa, rand_init, col_init, rand_final, col_final):
        if piesa.endswith("K") and abs(col_final - col_init) == 2:
            if col_final == 6:
                # Rocada Mica
                self.board[rand_final][5] = self.board[rand_final][7]
                self.board[rand_final][7] = ""
            elif col_final == 2:
                # Rocada Mare
                self.board[rand_final][3] = self.board[rand_final][0]
                self.board[rand_final][0] = ""
