#blank board 
# board = [
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0]
#     ]

# board from the "diabolical" section of a sudoku book 

board = [
    [0,0,3,6,0,0,0,2,0],
    [0,0,0,0,0,0,4,0,9],
    [7,0,0,0,0,1,0,6,0],
    [3,0,6,0,0,9,0,0,7],
    [0,0,0,0,2,0,0,0,0],
    [2,0,0,4,0,0,3,0,6],
    [0,3,0,7,0,0,0,0,2],
    [5,0,9,0,0,0,0,0,0],
    [0,1,0,0,0,5,8,0,0]
    ]

def possible(x,y,n):
    for i in range(0,9):
        if board[y][i] == n:
             return False
    for i in range(0,9):
        if board[i][x] == n:
            return False
    xi =  (x//3)*3
    yi = (y//3)*3
    
    for j in range (0,3):
        for k in range(0,3):
            if board [yi+j][xi+k] == n:
                return False

    return True




def solve():
    global board
    for x in range(9):
        for y in range(9):
            if board[y][x] == 0:
                for n in range(1,10):
                    if possible(x,y,n):
                        board[y][x] = n
                        solve()
                        board [y][x] = 0
                return
    for i in board:
        print(str(i)+'\n')


solve()
