class CellCounts:
    def __init__(self):
        self.code_no = 0
        self.figure_no = 0
        self.table_no = 0

    def get_code_no(self):
        return self.code_no

    def next_code_no(self):
        '''
            increments code cell number
            returns next code cell numer
        '''
        # global code_no
        self.code_no += 1
        return self.code_no

    def get_figure_no(self):
        return self.figure_no

    def next_figure_no(self):
        '''
            increments figure number
            returns next figure numer
        '''
        # global figure_no
        self.figure_no += 1
        return self.figure_no

    def get_table_no(self):
        return self.table_no

    def next_table_no(self):
        '''
            increments table number
            returns next table numer
        '''
        # global table_no
        self.table_no += 1
        return self.table_no

