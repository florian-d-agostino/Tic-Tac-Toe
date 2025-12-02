
player = "O"
board = [
    ["","",""],
    ["","",""],
    ["","",""]
]

def draw():
    for i in range(3):
        row = board[i]
        print(" | ".join(row))
        if i < 2:
            print("------")

def play():
    answer_row = int(input("Votre choix de ligne : "))
    answer_colum = int(input("Votre choix de colonne : "))
    board[answer_row][answer_colum] = player

def win():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == player:
            return True
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] == player:
            return True
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[2][0] == board[1][1] == board[0][2] == player:
        return True
    
    return False

def full():
    for i in board:
        if "" in i:
            return False
    return True


        

while True:
    draw()
    play()
    if win():
        print("Bravo")
        break
    if full():
        print("Match nul")
        break
    player = "X" if player == "O" else "O"


            
