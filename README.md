# sudoku
A sudoku solver in python.

# test cases
```
./main.py test/easy1.txt
./main.py test/hard48.txt
```
# input file
9 x 9 matrix with unsolved number represented by 0.

# output
```
./main.py test/hard48.txt
Original matrix:
X 9 8  X 6 X  X X X
X X X  9 X 7  X X 3
3 X X  X X 4  X 6 X

2 X X  5 X X  X 8 X
X 4 X  X 9 X  X 3 X
X 1 X  X X 3  X X 2

X 6 X  2 X X  X X 1
5 X X  6 X 9  X X X
X X X  X 4 X  2 5 X

Guess: (0, 5) = 1
  Found conflict
Guess: (0, 5) = 5

Result matrix:
1 9 8  3 6 5  4 2 7
4 5 6  9 2 7  8 1 3
3 7 2  8 1 4  5 6 9

2 3 9  5 7 6  1 8 4
8 4 7  1 9 2  6 3 5
6 1 5  4 8 3  9 7 2

7 6 4  2 5 8  3 9 1
5 2 1  6 3 9  7 4 8
9 8 3  7 4 1  2 5 6
```
