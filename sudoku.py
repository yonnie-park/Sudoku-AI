#!/usr/bin/env python
#coding:utf-8

'''
Jessie Park
jp3645
'''



"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import numpy as np
import sys
import time
import statistics

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

def board_to_arr(board):
    board_arr = np.array(list(board.values())).reshape((9,9))
    return board_arr


def is_complete(board):
    for i in range(9):
        for j in range(9):
            if(board[ROW[i] + COL[j]] == 0):
                return False
    return True

def check_domain(var, board):
    possible = set([1,2,3,4,5,6,7,8,9])
    board_arr = board_to_arr(board)

    row = ROW.index(var[0])
    col = COL.index(var[1])

    possible = possible - set(board_arr[row]) - set(board_arr.T[col]) - set(board_arr[row//3*3:row//3*3+3, col//3*3:col//3*3+3].flatten())

    return possible

def select_var(board):
    min_len = float("inf")
    select_domain = None

    for var in board:
        if board[var] == 0:
            domain = check_domain(var, board)
            if len(domain) < min_len:
                min_len = len(domain)
                select_domain = (var, domain)

    return select_domain

def backtracking(board):
    if(is_complete(board)):
        return board

    var, domain = select_var(board)
    
    for value in list(domain):
        board[var] = value
        res = backtracking(board)
        if res and is_complete(res):
            return res
        else:
            board[var] = 0

    return False

if __name__ == '__main__':

    if len(sys.argv) > 1:
    # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        sudoku = sys.argv[1]
        if len(sudoku) != 81:
            print("Error: sudoku must be of length 81")
        else:
            board = { ROW[r] + COL[c]: int(sudoku[9*r+c]) for r in range(9) for c in range(9)}
            print_board(board)
            start_time = time.time()
            solved_board = backtracking(board)
            end_time = time.time()

            print_board(solved_board)

            out_filename = 'output.txt'
            outfile = open(out_filename, "w")
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')
        
    else: #read from input source
        src_filename = 'sudokus_start.txt'
        end_filename = 'sudokus_finish.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
            
            finishfile = open(end_filename, "r")
            sudoku_finish = finishfile.read()
        except:
            print("Error reading the sudoku file")
            exit()

        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        num_boards_solved=0
        running_time_stat=[]
    
        for line, correct_line in zip(sudoku_list.split("\n"), sudoku_finish.split("\n")):
            start_time = time.time()
            if len(line) < 9:
                continue

            board = { ROW[r] + COL[c]: int(line[9*r+c]) for r in range(9) for c in range(9)}

            print_board(board)
            solved_board = backtracking(board)
            str_board=board_to_string(solved_board)

            assert(correct_line == str_board)
            num_boards_solved += 1
            
            outfile.write(str_board)
            outfile.write('\n')
            end_time = time.time()
            running_time_stat.append(end_time - start_time)
            
        max_runningtime=str(max(running_time_stat))
        min_runningtime=str(min(running_time_stat))
        mean_runningtime=str(statistics.mean(running_time_stat))
        std_runningtime=str(statistics.stdev(running_time_stat))
        print("Solved " + str(num_boards_solved) + " number of boards")
        print("Max Running time stat is " + max_runningtime)
        print("Min Running time stat is " + min_runningtime)
        print("Mean Running time stat is " + mean_runningtime)
        print("Standard deviation Running time stat is " + std_runningtime)

    
    print("Finishing all boards in file.")
    
