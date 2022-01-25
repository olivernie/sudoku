#!/usr/bin/python3

import sys
from sudoku import sudoku

S=sudoku()
S.load(sys.argv[1])
S.print_orig()
S.preprocess()
if S.solving() == 0:
    if S.guess(0) == -1:
        S.print_rslt()
else:
    # solved
    S.print_rslt()

