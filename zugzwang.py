import os
from random import randint
import random
import logging
import time
from termcolor import colored

numToSpaces = {0:"a",1:"b",2:"c"}
turn = 0

def playerToColor(p):
	if(p==1):
		return "White"
	if(p==2):
		return "Black"
	else:
		return ""

def printMove(player, name, move, reason):
	logging.debug(" Turn "+str(turn).rjust(3)+": "+ playerToColor(player) + " "+name+" moved to ("+numToSpaces[move[1]]+","+numToSpaces[move[0]]+") "+reason)		

def increment(currentMove, i):
	if(i>0):
		currentMove = currentMove + 1
		if(currentMove == 7):
			currentMove = 1
		return increment(currentMove, i-1)
	elif(i==0):
		return currentMove
	elif(i < 0):
		currentMove = currentMove - 1
		if(currentMove == 0):
			currentMove = 6
		return increment(currentMove, i+1)

class AI:
	logging.basicConfig(filename='aiThoughts.log', filemode='w', level=logging.DEBUG)
	toMove = [-1,-1]
	winLines = [[[0,0],[0,1],[0,2]],	#Top Row
		    [[1,0],[1,1],[1,2]],	#Middle Row
		    [[2,0],[2,1],[2,2]],	#Bottom Row
		    [[0,0],[1,0],[2,0]],	#Left Col
		    [[0,1],[1,1],[2,1]],	#Middle COl
		    [[0,2],[1,2],[2,2]],	#Right Col
		    [[0,0],[1,1],[2,2]],	#TL to BR diagonal
		    [[0,2],[1,1],[2,0]]]	#TR to BL diagonal
	name=""
	def move(self, g):	
		if(self.iCanWinThisTurn(g)):
			#Win if able			
			if(g.player(g.board[self.toMove[0]][self.toMove[1]]) == -1 and self.toMove[0] != -1):
				printMove(g.player(g.currentMove),"AI ",self.toMove, "to win")	
				return self.toMove[0], self.toMove[1]

		if(self.opponentCanWinNextTurn(g)):
			#Block opponent win if able			
			if(g.board[self.toMove[0]][self.toMove[1]] == 0 and self.toMove[0] != -1):
				printMove(g.player(g.currentMove),"AI ",self.toMove, "to block opponent win")	
				return self.toMove[0], self.toMove[1]

		if(self.zugzwang(g)):
			#Set up Zugzwang
			#place into line with currentMove-2 and currentMove+1
			if(g.board[self.toMove[0]][self.toMove[1]] == 0 and self.toMove[0] != -1):
				printMove(g.player(g.currentMove),"AI ",self.toMove, "to setup Zugzwang")	
				return self.toMove[0], self.toMove[1]

		if(self.iCanBlockAZugzwang(g)):
			#Block Zugwang
			if(g.board[self.toMove[0]][self.toMove[1]] == 0 and self.toMove[0] != -1):
				printMove(g.player(g.currentMove),"AI ",self.toMove, "to block opponent Zugzwang setup")	
				return self.toMove[0], self.toMove[1]
		#If no better option, random placement		
		valid = False
		while(not valid):
			self.toMove = [randint(0,2), randint(0,2)]
			if(g.board[self.toMove[0]][self.toMove[1]] == 0):
				valid = True
		printMove(g.player(g.currentMove),"AI ",self.toMove, "randomly")	
		return self.toMove[0], self.toMove[1]

	def iCanWinThisTurn(self, g):
		me = g.player(g.currentMove)
		#Store opponent placement
		if(me == 1):
			op = 2
		elif(me == 2):
			op = 1
		#See if I am about to win a line
		for line in self.winLines:
			players = [0, 0, 0]
			for i in line:
				player = g.player(g.board[i[0]][i[1]])
				if(player==-1):
					#Assign spot to move to blank spot in line
					self.toMove = [i[0],i[1]]
					player = 0
				if(g.board[i[0]][i[1]] != g.currentMove):
					players[player] = players[player] + 1
			if(players[me] == 2 and self.toMove in line):
				return True
		return False

	def zugzwang(self, g):
		me = g.player(g.currentMove)
		#Store opponent placement
		if(me == 1):
			op = 2
		elif(me == 2):
			op = 1
		#See if I am about to win a line
		for line in self.winLines:
			pieces = 0
			for i in line:
				piece = g.board[i[0]][i[1]]
				if(piece == 0):
					#Assign spot to move to blank spot in line
					self.toMove = [i[0],i[1]]
					player = 0
				if(g.board[i[0]][i[1]] == increment(g.currentMove,-2) or g.board[i[0]][i[1]] == increment(g.currentMove,1)):
					pieces = pieces + 1
			if(pieces == 2 and self.toMove in line):
				return True
		return False

	def iCanBlockAZugzwang(self, g):
		me = g.player(g.currentMove)
		#Store opponent placement
		if(me == 1):
			op = 2
		elif(me == 2):
			op = 1
		#See if I am about to win a line
		for line in self.winLines:
			pieces = 0
			for i in line:
				piece = g.board[i[0]][i[1]]
				if(piece == 0):
					#Assign spot to move to blank spot in line
					self.toMove = [i[0],i[1]]
					player = 0
				if(g.board[i[0]][i[1]] == increment(g.currentMove,-1) or g.board[i[0]][i[1]] == increment(g.currentMove,2)):
					pieces = pieces + 1
			if(pieces == 2 and self.toMove in line):
				return True
		return False		

	def opponentCanWinNextTurn(self, g):
		me = g.player(g.currentMove)
		#Store opponent placement
		if(me == 1):
			op = 2
		elif(me == 2):
			op = 1
		#See if opponent is about to win a line
		for line in self.winLines:
			players = [0, 0, 0]
			for i in line:
				player = g.player(g.board[i[0]][i[1]])
				if(player==-1):
					#Assign spot to move to blank spot in line
					self.toMove = [i[0],i[1]]
					player = 0
				if(g.board[i[0]][i[1]] != increment(g.currentMove,1)):
					players[player] = players[player] + 1
			if(players[op] == 2 and self.toMove in line):
				return True
		return False

class Game:
	board = [[0,0,0],[0,0,0],[0,0,0]]
	pieces = {0: " ",1: "P", 2: "P", 3: "N", 4: "N",5: "K",6: "K"}
	realPieces = {0: "P", 1: "P", 2: "N", 3: "N",4: "K",5: "K"}
	spaces = {"a": 0, "b":1, "c":2}
	currentMove = 1
	placement = [0, [-1,-1], [-1,-1], [-1,-1], [-1,-1], [-1,-1], [-1,-1]]

	def printablePiece(self,pieceNum):
		colors = {1:'red',2:'blue'}
		if(pieceNum == 0):
			return self.pieces[pieceNum]
		return colored(self.pieces[pieceNum], colors[self.player(pieceNum)])

	def printableRealPiece(self,realPieceNum):
		colors = {0:'red',1:'blue'}
		return colored(self.realPieces[realPieceNum], colors[realPieceNum % 2])
		

	def drawBoard(self):
		pieces = self.pieces
		board = self.board
		b1 = "    a   b   c     Placing: " + self.printableRealPiece((self.currentMove-1) % 6) + " | "
		for i in range(0,5):
			b1 = b1 + self.printableRealPiece((self.currentMove+i) % 6) + " "
		b1 = b1+"\n"
		b2 = " a  "+self.printablePiece(board[0][0])+" ¦ "+self.printablePiece(board[0][1])+ " ¦ "+self.printablePiece(board[0][2]) + "\n"
		b3 = "   ---+---+---         White:  ("+colored("X",'red')+")\n"
		b4 = " b  "+self.printablePiece(board[1][0])+" ¦ "+self.printablePiece(board[1][1])+ " ¦ "+self.printablePiece(board[1][2]) + "\n"
		b5 = "   ---+---+---         Black:  ("+colored("X",'blue')+")\n"	
		b6 = " c  "+self.printablePiece(board[2][0])+" ¦ "+self.printablePiece(board[2][1])+ " ¦ "+self.printablePiece(board[2][2]) + "\n"
		print(b1 + b2 + b3 + b4 + b5 + b6)

	def turn(self, ai = False):
		if(not ai):
			move = input("Move " + self.printablePiece(self.currentMove) + " to: ")
			c = self.spaces[move[0]]
			r = self.spaces[move[1]]
			if(self.board[r][c] != 0):
				print("Invalid Move: space occupied")
				return False
			else:
				printMove(self.player(self.currentMove),"Hmn",[r,c], "")	
		else:
			ai = AI()
			r, c = ai.move(self)
				
		oldR = self.placement[self.currentMove][0]
		oldC = self.placement[self.currentMove][1]
		if(oldR != -1):
			self.board[oldR][oldC] = 0
		self.board[r][c]=self.currentMove
		self.placement[self.currentMove][0] = r
		self.placement[self.currentMove][1] = c

		self.currentMove = self.currentMove + 1
		if(self.currentMove == 7):
			self.currentMove = 1
		return True
	
	def checkForWin(self):
		winner = -1
		#Check rows
		for row in self.board:
			if(self.player(row[0]) == self.player(row[1]) == self.player(row[2])):
				if(self.player(row[0]) != -1):
					winner = self.player(row[0])
		#Check cols
		for i in range(0,3):
			if(self.player(self.board[0][i]) == self.player(self.board[1][i]) == self.player(self.board[2][i])):
				if(self.player(self.board[0][i]) != -1):
					winner = self.player(self.board[0][i])
		#Check diagonals
			if(self.player(self.board[0][0]) == self.player(self.board[1][1]) == self.player(self.board[2][2])):
				if(self.player(self.board[1][1]) != -1):
					winner = self.player(self.board[1][1])
			if(self.player(self.board[0][2]) == self.player(self.board[1][1]) == self.player(self.board[2][0])):
				if(self.player(self.board[1][1]) != -1):
					winner = self.player(self.board[1][1])
		return winner

	def player(self, piece):
		p = piece % 2
		if(piece == 0):
			return -1
		if(p == 0):
			return 2
		return p

os.system("clear")
players = input("1 or 2 players? ")
os.system("clear")
if(players=="2"):
	game = Game()
	game.drawBoard()
	while(game.checkForWin() == -1):
		if(game.turn()):
			os.system("clear")
			game.drawBoard()
	print(playerToColor(game.checkForWin()),"wins!!!")
elif(players=="1"):
	game = Game()
	game.drawBoard()
	turnBool = random.choice([True, False])
	ai = 0
	if(turnBool):
		print("AI Goes first")
		ai = 1
	else:
		print("You go first!")
		ai = 2
	while(game.checkForWin() == -1):
		turn = turn + 1
		if(game.turn(turnBool)):
			os.system("clear")
			game.drawBoard()
			turnBool = not turnBool
	if(game.checkForWin()==ai):
		print("AI Wins!!!")
	else:
		print("You Win!!!")
elif(players=="0"):
	delay = int(input("Enter time delay in s: "))
	game = Game()
	game.drawBoard()
	while(game.checkForWin() == -1):
		time.sleep(delay)
		turn = turn + 1
		print("Turn: ", turn)
		if(game.turn(True)):
			game.drawBoard()
	print(playerToColor(game.checkForWin()),"wins!!!")
