# Zugzwang
A console app to play a Zugzwang
## Rules
Each turn, place a piece. What piece you play moves through the cycle of pawn, knight, king, pawn, etc. If a piece is on the board, pick it up and place it in an empty space. Get three in a row to win.
## Software
Right now only works on Linux, sorry.
### Setup
1. Download the script
2. Open a terminal in the directory containing the script
3. sudo python3 -m pip install termcolor
4. python3 zugzwang.py
### To Play
Enter the number of players (0 to make bots fight)
Enter in each move you want to make, column then row (to the top middle space is ba)
### Log
The program saves moves data in a log file. From the same directory, run tail -f aiThoughts.log in the terminal to see it in real time. The AI will also justify its moves.
