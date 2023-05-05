import json
import sys
import pickle
import os

from .models import AbstractGameVariant

class Jenga(AbstractGameVariant):

    def __init__(self):
        name = "Jenga"
        desc="Regular - 15 pieces"
        status = "stable"
        gui_status = 'v2'

        #Change upon COMMIT
        self.DIRECTORY = "data/"
        self.FILENAME = "JengaOutput.txt"

        super(Jenga, self).__init__(name, desc, status=status, gui_status=gui_status)

    def start_position(self):
        #{AutoGUI}_{Player Turn A or B}_{Random int}_{Random int}_{JENGA BOARD representation (Max Length)}
        return "R_A_0_0_" + "J"*15

    def stat(self, position):
        try:
            response = ""

            with open(self.DIRECTORY + self.FILENAME, "r") as JengaDatabaseFile:
                data = JengaDatabaseFile.readlines()
                for line in data:
                    if line == "":
                        break

                    #Parsed_Line formatting to be changed
                    parsed_Lines = line.split(" ")
                    if parsed_Lines[2].strip("\n") == position.split("_")[4]:
                        response = {
                            "position": position,
                            "positionValue": parsed_Lines[1],
                            "remoteness": int(parsed_Lines[0]),
                        }
                        break
                
                JengaDatabaseFile.close()

            if response == "":
                print("Error: Could not find position -> " + position )

            return response
        except IOError:
            print("Error: Could not read JengaDatabaseFile")

    def next_stats(self, position):
        response = []
        moves = GenerateMoves(position.split("_")[4])
        for move in moves:
            if self.get_player(position) == "A":
                response_dict = self.stat("R_B_0_0_" + DoMove(position.split("_")[4], move))
                response_dict.update({"move": "A_-_" + str(move)})
                response.append(response_dict)
            else:
                response_dict = self.stat("R_A_0_0_" + DoMove(position.split("_")[4], move))
                response_dict.update({"move": "A_-_" + str(move)})
                response.append(response_dict)
                
        return response

    def get_player(self, position_str):
        position = position_str.split('_')
        return position[1]
    

################### Jenga Encoded File ##########################

######################################################
# Name: Nakul Srikanth
# 
# Game: Jenga
# 
# Description:
# Players remove pieces from tower and 
# add them to the top of the pile. Player without 
# any legal moves left loses. The topmost finished 
# level and above are unaccesible for moves.
#
#######################################################

def isPrimative(board):
    if (GenerateMoves(board) != []):
        return False
    return True

def DoMove(board, move):
    if (not isPrimative(board) and all([board[move + m] == 'J' for m in getAdjacent(move)])):
        return board[:move] + "X" + board[move+1:] + "J"
    else:
        return board
    

def PrimativeValue(board):
    if isPrimative(board):
        return "L"
    else:
        return "Not Primative"

def GenerateMoves(board):
    returnLst = []
    for k in range(((len(board) // 3) - 1) * 3):
        if board[k] == 'J' and all([board[k + m] == 'J' for m in getAdjacent(k)]):
            returnLst.append(k)

    return returnLst

def getAdjacent(move):
    index = move % 3
    if(index == 0):
        return [1]
    elif(index == 1):
        return [-1, 1]
    else:
        return [-1]
    
###################### Solver ###################################

"""
######################################################
# Name: Nakul Srikanth
# 
# Game: Jenga
# 
# Description:
# Players remove pieces from tower and 
# add them to the top of the pile. Player without 
# any legal moves left loses. The topmost finished 
# level and above are unaccesible for moves.
#
#######################################################


import Jenga

pieces = 9
board = "J"*pieces

myDict = {}

def Solver(board):
    board_primative = Jenga.PrimativeValue(board)
    if (board_primative != "Not Primative"): 
        myDict[board] = (board_primative, 0)
        return (board_primative, 0)
    else:
        moves = Jenga.GenerateMoves(board)
        primatives_list = []
        for move in moves:
            new_board = Jenga.DoMove(board, move)
            if new_board in myDict.keys():
                primatives_list.append(myDict[new_board])
            else:
                primatives_list.append(Solver(new_board))
        if ("Lose" in [m for (m, n) in primatives_list]):
            min_remote = 99999999999999
            for item in primatives_list:
                k, v = item
                if k == "Lose" and v < min_remote:
                    min_remote = v
            min_remote += 1
            myDict[board] = ("Win", min_remote)
            return ("Win", min_remote)
        else:
            max_remote = -1
            for item in primatives_list:
                k, v = item
                if k == "win" and v > max_remote:
                    max_remote = v
            max_remote += 1
            myDict[board] = ("Lose", max_remote)
            return ("Lose", max_remote)

def test():
    Solver(board)

    myFile = open("JengaOutput1.txt", 'w')

    for k, v in myDict.items():
        val, remoteness = v
        myFile.write(str(remoteness) + " " + val + " ")
        myFile.write(str(k))
        myFile.write("\n")

    myFile.close()

    return myDict

test()

"""