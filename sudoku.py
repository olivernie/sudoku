#!/usr/bin/python3
import sys
import os

class sudoku():
    'A Sudoku Solver'
    _file_name = ""
    _is_loaded = False
    _orig_data = []
    _rslt_data = []
    _row_data = []
    _col_data  = []
    _sqr_data  = []
    _solver_array = []
    _row_solver = [ [] for _ in range(9) ]
    _col_solver = [ [] for _ in range(9) ]
    _sqr_solver = [ [] for _ in range(9) ]
    _is_done   = False
    DBG_ERROR    = 0
    DBG_WARN     = 1
    DBG_INFO     = 2
    DBG_DEBUG    = 3
    _debug_level = DBG_ERROR

    def log(self, level):
        return level <= self._debug_level;

    def set_log_level(self, level):
        if level > self.DBG_DEBUG:
            level = self.DBG_DEBUG

        if level < self.DBG_ERROR:
            level = self.DBG_ERROR

        self._debug_level = level

    def __init__(self):
        self.reset()

    def reset(self):
        self._is_done = False
        self._row_data = []
        self._col_data  = []
        self._sqr_data  = []
        self._solver_array = []
        self._row_solver   = [ [] for _ in range(9) ]
        self._col_solver   = [ [] for _ in range(9) ]
        self._sqr_solver   = [ [] for _ in range(9) ]
        self._orig_data = []
        self._rslt_data = []

    def load(self, file_name):
        if not os.path.isfile(file_name):
            print("Error: can't find %s." % file_name)
            return

        self._file_name = file_name
        try: 
            fd = open(file_name)
        except:
            print("Error: can't open %s." % file_name)
            return

        self._orig_data = []
        self._rslt_data = []
        for line in fd:
            row = []
            data = line.split(' ')
            for n in data:
                row.append(int(n))
            self._orig_data.append(row)
            self._rslt_data.append(row)

        fd.close()
        self._is_loaded = True

    '''
    clone:
      copy obj's rslt_data as myself's orig_data and rslt_data.
      obj is a sudoku instance.
    '''
    def clone(self, obj):
        if not isinstance(obj, sudoku):
            return None
         
        self.reset()
        self._file_name = obj._file_name
        if obj._is_loaded:
            for list in obj._rslt_data:
                self._orig_data.append(list.copy())
                self._rslt_data.append(list.copy())
            self._is_loaded = True
        #self.print_orig()
        #self.print_rslt()

    def print_matrix(self, data):
        r = 0
        for row in data:
            c = 0
            # print row
            for num in row:
                print("{n} {s}".format(n=str(num) if num != 0 else 'x', s=' ' if c==2 else ''), end='')
                c = (c + 1) % 3
            print()   # print newline
            if r == 2:
                print()   # print newline
            r = (r + 1)%3

    def print_orig(self):
        print("Original matrix:")
        self.print_matrix(self._orig_data)

    def print_rslt(self):
        print("\nResult matrix:")
        self.print_matrix(self._rslt_data)

    def print_data(self, data):
        for row in data:
            print(row)

    def print_row_data(self):
        print("Row data:")
        self.print_data(self._row_data)

    def print_col_data(self):
        print("Column data:")
        self.print_data(self._col_data)

    def print_sqr_data(self):
        print("Square data:")
        self.print_data(self._sqr_data)

    '''generate the solved number set for each row.'''
    def prepare_row(self):
        data = [ set() for _ in range(9) ]
        for row in range(9):
            for col in range(9):
                element = self._orig_data[row][col] 
                if element != 0:
                    data[row].add(element)
            #print("row %d" % row)
            #print(data[row])
        self._row_data = data

    '''generate the solved number set for each column.'''
    def prepare_column(self):
        data = [ set() for _ in range(9)]
        for col in range(9):
            for row in range(9):
                element = self._orig_data[row][col] 
                if element != 0:
                    data[col].add(element)
            #print("col %d" % col)
            #print(data[col])
        self._col_data = data

    '''
      prepare_square:
        generate the solved number set for each 3x3 square.
        self._sqr_data is the list of solved number set.
    '''
    def prepare_square(self):
        data = [ set() for _ in range(9)]
        sqr = 0
        # for every 3-row
        for row in range(0,9,3):
            # for every 3-col
            for col in range(0,9,3):
                # check 3x3 square
                for r in range(row, row+3):
                    for c in range(col, col+3):
                        element = self._orig_data[r][c] 
                        if element != 0:
                            data[sqr].add(element)
                #print("sqr %d" % sqr)
                #print(data[sqr])
                sqr += 1

        self._sqr_data = data

    '''
      prepare_solver_array:
        Generate the solver element array.
        Each solver element is a dict with format below.
          {
            'pos'       : (row, col, sqr), 
            'num'       : int, 
            'candidates': {candidate set}
          }
    '''
    def prepare_solver_array(self):
      for row in range(9):
        for col in range(9):
          sqr = int(col/3) + int(row/3)*3
          if self._orig_data[row][col] == 0:
              solver_element = {'pos': (row, col, sqr), 'num' : 9, 'candidates' : {1,2,3,4,5,6,7,8,9}}
              self._solver_array.append(solver_element)
              # prepare solver list for each row, col and sqr.
              self._row_solver[row].append(solver_element)
              self._col_solver[col].append(solver_element)
              self._sqr_solver[sqr].append(solver_element)
              #print(solver_element)

    def print_solver_array(self):
      for solver in self._solver_array:
        print(solver)

    def print_row_solver(self):
      for row in range(9):
        print("row %d:" % row)
        for solver in self._row_solver[row]:
          print(solver)

    def print_col_solver(self):
      for col in range(9):
        print("col %d:" % col)
        for solver in self._col_solver[col]:
          print(solver)

    def print_sqr_solver(self):
      for sqr in range(9):
        print("sqr %d:" % sqr)
        for solver in self._sqr_solver[sqr]:
          print(solver)

    ''' preprocess orig_data and generate column data. '''
    def preprocess(self):
      self.prepare_row()
      self.prepare_column()
      self.prepare_square()
      self.prepare_solver_array()

    '''
    update:
        Update the solved num to row, col and sqr.
        Update the solved num to _rslt_data.
        Delete the solver from solver array.
        Return the number of updated solvers
    '''
    def update(self):
        solved_list = []
        # look for the solved solver
        for solver in self._solver_array:
            row, col, sqr = solver['pos']

            if solver['num'] > 1:
                continue

            if solver['num'] <= 0:
                raise Exception("update err: solver (%d, %d, %d) is empty" % (row, col, sqr))

            val = solver['candidates'].pop()
            if val in self._row_data[row]:
                raise Exception("update err: %d is already in row %d" % (val, row))
            if val in self._col_data[col]:
                raise Exception("update err: %d is already in col %d" % (val, col))
            if val in self._sqr_data[sqr]:
                raise Exception("update err: %d is already in sqr %d" % (val, sqr))

            self._row_data[row].add(val)
            self._col_data[col].add(val)
            self._sqr_data[sqr].add(val)
            self._rslt_data[row][col] = val
            solved_list.append(solver)
        
        # remove the solved solver
        for solver in solved_list:
            row, col, sqr = solver['pos']
            self._solver_array.remove(solver)
            self._row_solver[row].remove(solver)
            self._col_solver[col].remove(solver)
            self._sqr_solver[sqr].remove(solver)

        return len(solved_list)

    '''
      Process 1:
        Remove candidates from solver element when the condidates are
        present in the same row, colunm and square.
        Return the number of solved solver.
    '''
    def process1(self):
        for solver in self._solver_array:
            row, col, sqr = solver['pos']
            candidates    = solver['candidates']
            present_num   = set()
            for n in candidates:
                # remove candidate which is present in row
                if n in self._row_data[row]:
                    present_num.add(n)
                    continue

                # remove candidate which is present in column
                if n in self._col_data[col]:
                    present_num.add(n)
                    continue

                # remove candidate which is present in square
                if n in self._sqr_data[sqr]:
                    present_num.add(n)
                    continue

            for n in present_num:
                candidates.remove(n)
                solver['num'] -= 1
                if self.log(self.DBG_INFO):
                  print("process1: change (%d,%d,%d)" % (row, col, sqr))

            #solver['candidates'] = candidates
            #print(solver)

        # update the solved num to row, col, sqr and result array
        solved_num = self.update()
        if self.log(self.DBG_INFO): print("process1: %d solved" % solved_num)
        return solved_num

    '''
      lookup_uniq_candidate
        Search each solver_list, find the solver which has the
        unique candidate in the solver_list. Assign the unique
        number to that solver.
    '''
    def lookup_uniq_candidate(self, solver_array):
        for solver_list in solver_array:
            appearance = {i:0 for i in range(1,10)}       # initial a dict with key from 1 to 9.
            last_solver= {i:None for i in range(1,10)}
            for solver in solver_list:
                candidates = solver['candidates']
                for n in candidates:
                    appearance[n] += 1
                    last_solver[n] = solver
             
            if self.log(self.DBG_DEBUG): print(appearance)

            for i in range(1,10):
                if appearance[i] == 1:
                    last_solver[i]['candidates'] = {i}
                    last_solver[i]['num'] = 1
                    if self.log(self.DBG_DEBUG): print(last_solver[i])

    '''
    process2:
        Look for the unique candidate in each row, col and square.
        process2 _MUST_ be called only after process1 returns 0.
    '''
    def process2(self):
        if self.log(self.DBG_DEBUG): print("lookup uniq candidate in row solvers")
        self.lookup_uniq_candidate(self._row_solver)
        if self.log(self.DBG_DEBUG): print("lookup uniq candidate in col solvers")
        self.lookup_uniq_candidate(self._col_solver)
        if self.log(self.DBG_DEBUG): print("lookup uniq candidate in sqr solvers")
        self.lookup_uniq_candidate(self._sqr_solver)
        
        # update the solved num to row, col, sqr and result array
        solved_num = self.update()
        if self.log(self.DBG_INFO): print("process2: %d solved" % solved_num)
        return solved_num

    def debug(self):
      self.print_solver_array()
      self.print_row_data()
      self.print_col_data()
      self.print_sqr_data()
      self.print_rslt()

    '''
      solving:
        start the algorithm until both process1 and process2 return 0
        (1) success of convergence when solver_array is empty;
        (2) fail when solver_array is not empty.

        preprocess() must be called before run().
    '''
    def solving(self):
        try:
            while True:
                # run process1 until it returns 0
                while self.process1() != 0:
                    pass
                
                # process2
                if self.process2() == 0:
                    break
        except:
            # there is conflict
            return -1
        
        if len(self._solver_array) == 0:
            self._is_done = True
        
        if self._is_done:
            if self.log(self.DBG_INFO): print("Sudoku is solved:")
            return 1
        else:
            if self.log(self.DBG_INFO): print("Sudoku is unsolved:")
            return 0

    def set_value(self, row, col, val):
        self._orig_data[row][col] = val
        self._rslt_data[row][col] = val

    '''
      guess:
        guess is a recursive function.
        Pick a solver with least number of candidates. For each candidate
        in the picked solver, do:
        (1) clone a new sudoku instance S. Let S._orig_data to be current rslt_data and the candiate.
        (2) call S.solving(). Sudoku is solved when S.solving returns 1.
        (3) call S.guess() if S.solving returns 0.
    '''
    def guess(self, depth):
        num_of_candidate = 9
        # lookup the solver with least candidates
        for s in self._solver_array:
            if num_of_candidate > s['num']:
                num_of_candidate = s['num']
                solver = s
    
        if self.log(self.DBG_DEBUG): print(s)

        # try each candidate in the solver
        ret = -1
        row, col, sqr = solver['pos']
        for candidate in solver['candidates']:
            print("{s}".format(s = '  '*depth), end='')
            print("Guess: (%d, %d) = %d" % (row, col, candidate))
            S = sudoku()
            S.clone(self)
            S.set_value(row, col, candidate)
            S.preprocess()
            ret = S.solving()
            if ret == -1: 
                print("{s}Found conflict".format(s = '  '*(depth+1)))

            elif ret == 0:
                # unsolved, continue guess()
                ret = S.guess(depth+1)

            elif ret == 1:
                # solved
                S.print_rslt()
                break

        return ret
    
