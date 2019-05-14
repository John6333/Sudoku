import pdb

class SudokuData():
    def __init__(self):
        self.data = list(range(1,10))
        self.clean = False

    def set(self, i):
        if (i<1) or (i>9) or (type(i) is not int):
            print('Illegal number')
            return
        self.data = [i]
        self.clean=True

    def remove(self, value):
        if value not in self.data:
            return True
        if self.clean:
            return False
        self.data.remove(value)
        return True

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return self.data.__str__()

    def get_str(self, index):
        str_list = [f'{self.data[i-1]:d}' for i in index if i-1<self.__len__()]
        info = ''.join(str_list)
        info = f'{info:<3}'
        return info

class Sudoku():
    def __init__(self):
        self.size = 9
        self.data = [SudokuData() for i in range(self.size*self.size)]

    def get_row(self, index):
        start = (index-1)*self.size
        row = [self.data[i] for i in range(start, start+9)]
        return row

    def get_col(self, index):
        col = [self.data[(index-1)+i*self.size] for i in range(self.size)]
        return col

    def get_cell(self, cell_pos):
        row = cell_pos[0]-1
        col = cell_pos[1]-1
        cell = [self.data[row*27+i*9+col*3+j] for i in range(3) for j in range(3)]
        return cell

    def rowcol_to_position(self, row, col):
        pos1 = ((row-1)//3+1, (col-1)//3+1)
        pos2 = ((row-1)%3 +1, (col-1)%3 +1)
        return pos1, pos2

    def position_to_rowcol(self, pos1, pos2):
        row = (pos1[0]-1)*3 + pos2[0]
        col = (pos1[1]-1)*3 + pos2[1]
        return row, col

    def index_to_position(self, index):
        row = index//9 + 1
        col = index%9  + 1
        return self.rowcol_to_position(row, col)

    def position_to_index(self, pos1, pos2):
        row, col = self.position_to_rowcol(pos1, pos2)
        index = (row-1)*9 + col-1
        return index

    def __str__(self):
        top_rule = '='*(3*9+8+2*3) + '\n'
        mid_rule = '  ' + '='*11 + '  ' + '='*11 + '  ' + '='*11  + '\n'
        hline    = '  ' + '-'*11 + '  ' + '-'*11 + '  ' + '-'*11  + '\n'
        info = top_rule
        for i in range(9):
            row = self.get_row(i+1)
            for j in range(3):
                row_str = '  '
                for k in range(9):
                    row_str += row[k].get_str([j*3+1,j*3+2,j*3+3])
                    row_str += '  ' if (k+1)%3==0 else ' '
                row_str += '\n'
                info += row_str
                info += mid_rule if (j==2 and (i+1)%3==0) else ''
        return info

    def get_data(self, cell_pos, pos):
        index = self.position_to_index(cell_pos, pos)
        return self.data[index]

    def set_value(self, value, cell_pos=None, pos=None, row=None, col=None):
        assert all([cell_pos, pos]) or all([row, col])
        if cell_pos is None:
            cell_pos, pos = self.rowcol_to_position(row, col)
        self.get_data(cell_pos, pos).set(value)
        if row is None:
            row, col = self.position_to_rowcol(cell_pos, pos)
        row_data = self.get_row(row)
        success = [data.remove(value) for i,data in enumerate(row_data) if (i+1)!=col]
        if not all(success):
            return False
        col_data = self.get_col(col)
        success = [data.remove(value) for i,data in enumerate(col_data) if (i+1)!=row]
        if not all(success):
            return False
        cell_data = self.get_cell(cell_pos)
        index = (pos[0]-1)*3 + pos[1]
        success = [data.remove(value) for i,data in enumerate(cell_data) if (i+1)!=index]
        if not all(success):
            return False
        return True

    def check_update_row(self):
        updated = False
        success = True
        for i in range(9):
            row_data = self.get_row(i+1)
            # check by value
            for val in range(1,10):
                idx = [j for j,data in enumerate(row_data) if val in data.data]
                if len(idx)==1:
                    pos1, pos2 = self.rowcol_to_position(i+1, idx[0]+1)
                    if self.get_data(pos1, pos2).clean==False:
                        print(f'row: {pos1} {pos2} {val}')
                        success = self.set_value(val, pos1, pos2)
                        updated = True
                        if not success:
                            return updated, success
        return updated, success

    def check_update_col(self):
        updated = False
        success = True
        for i in range(9):
            col_data = self.get_col(i+1)
            # check by value
            for val in range(1,10):
                idx = [j for j,data in enumerate(col_data) if val in data.data]
                if len(idx)==1:
                    pos1, pos2 = self.rowcol_to_position(idx[0]+1, i+1)
                    if self.get_data(pos1, pos2).clean==False:
                        print(f'col: {pos1} {pos2} {val}')
                        success = self.set_value(val, pos1, pos2)
                        updated = True
                        if not success:
                            return updated, success
        return updated, success

    def check_update_cell(self):
        updated = False
        success = True
        for i in range(1,4):
            for j in range(1,4):
                cell_data = self.get_cell((i,j))
                for val in range(1,10):
                    idx = [j for j,data in enumerate(cell_data) if val in data.data]
                    if len(idx)==1:
                        pos1 = (i,j)
                        pos2 = (idx[0]//3+1, idx[0]%3+1)
                        if self.get_data(pos1, pos2).clean==False:
                            print(f'cell: {pos1} {pos2} {val}')
                            success = self.set_value(val, pos1, pos2)
                            updated = True
                            if not success:
                                return updated, success
        return updated, success

    def solve(self):
        while True:
            updated1, success1 = self.check_update_row()
            updated2, success2 = self.check_update_col()
            updated3, success3 = self.check_update_cell()
            if not any([updated1, updated2, updated3]):
                break
            if not all([success1, success2, success3]):
                print('Illegal State!')
                return False
        solved = all([data.clean for data in self.data])
        return True, solved

    def clone(self):
        sudoku = Sudoku()
        for data_src, data_dest in zip(self.data, sudoku.data):
            data_dest.data = data_src.data.copy()
            data_dest.clean = data_src.clean
        return sudoku

    def clone_from(self, sudoku):
        for data_src, data_dest in zip(sudoku.data, self.data):
            data_dest.data = data_src.data.copy()
            data_dest.clean = data_src.clean

    def get_closest_to_clean_data(self, start=0):
        min_len = 9
        out = None
        index = None
        for idx, data in enumerate(self.data):
            if idx<start:
                continue
            if data.clean:
                continue
            if len(data)<min_len:
                out = data
                min_len = len(data)
                index = idx
            if len(out) ==2:
                break
        return out, index

    def trial(self, pos1, pos2, val):
        success = True
        sudoku = self.clone()
        while success:
            success = sudoku.set_value(val, pos1, pos2)
            if not success:
                return False, None
            success, solved = sudoku.solve()
            if not success:
                return False, None
            if solved:
                return True, sudoku
            # success and not solved, continue trial
            data, index = sudoku.get_closest_to_clean_data()
            new_pos1, new_pos2  = sudoku.index_to_position(index)
            results = [sudoku.trial(new_pos1, new_pos2, new_val) for new_val in data.data]
            feasible = [r[0] for r in results]
            if not any(feasible):
                return False, None
            else:
                result = [r for r in results if r[0]]
                return result[0]

    def solve_by_trial(self):
        start = 0
        while start<9*9:
            data, index = self.get_closest_to_clean_data(start)
            pos1, pos2 = self.index_to_position(index)
            possible_val_list = data.data.copy()
            for val in data.data:
                print(f'Trying {pos1} {pos2} {val}')
                sudoku_temp = self.clone()
                feasible, result = sudoku_temp.trial(pos1, pos2, val)
                if feasible:
                    self.clone_from(result)
                    return True
                else:
                    possible_val_list.remove(val)
                    if len(possible_val_list)==1:
                        self.set_value(possible_val_list[0], pos1, pos2)
                        print(f'trial: {pos1} {pos2} {possible_val_list[0]}')
                        success, solved = self.solve()
                        return solved
            start = index+1

    def set_from_matrix(self, M):
        [self.set_value(M[i][j], row=i+1, col=j+1) for i in range(9) for j in range(9) if (M[i][j] in [1,2,3,4,5,6,7,8,9])]

if __name__=='__main__':
    sudoku = Sudoku()
    M1= [[0,0,7,0,1,0,0,0,0],
         [0,3,0,8,0,0,9,0,0],
         [9,8,0,5,4,3,0,0,7],
         [0,0,0,0,0,6,8,7,1],
         [0,0,0,0,0,5,0,0,0],
         [0,0,0,0,9,1,6,5,0],
         [3,0,0,0,0,4,5,0,8],
         [1,0,0,0,0,0,3,0,0],
         [0,0,0,0,0,0,0,0,0]]
    M2= [[0,0,0,0,1,5,0,6,0],
         [6,0,4,0,7,0,0,0,0],
         [0,0,9,0,0,0,7,0,0],
         [0,0,0,0,0,0,5,4,0],
         [2,0,0,0,9,0,0,0,1],
         [0,0,0,6,0,3,0,0,9],
         [0,0,0,0,5,0,0,0,3],
         [4,1,2,0,0,0,0,0,0],
         [7,0,0,0,0,0,2,0,0]]
    sudoku.set_from_matrix(M1)

    print(sudoku)
    while True:
        _,solved = sudoku.solve()
        if solved:
            break
        solved = sudoku.solve_by_trial()
        if solved:
            break
    print(sudoku)
