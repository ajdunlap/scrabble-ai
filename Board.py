from ansi.colour import fg,bg

class Board:
    def __init__(self,height,width,double_letter_scores,
            double_word_scores,triple_letter_scores,triple_word_scores,
            starting_square):
        self.height = height
        self.width = width
        self.double_letter_scores = double_letter_scores
        self.double_word_scores = double_word_scores
        self.triple_letter_scores = triple_letter_scores
        self.triple_word_scores = triple_word_scores
        self.starting_square = starting_square

def make_official_scrabble_board():
    triple_word_scores = [(0,0),(0,7),(0,14),(7,0),(7,14)]
    double_letter_scores = [(0,3),(0,11),(2,6),(2,8),(3,0),(3,7),(3,14),(6,2),(6,6),(6,8),(6,12),(7,3),(7,11)]
    double_word_scores = [(1,1),(7,7),(1,13),(2,2),(2,12),(3,3),(3,11),(4,4),(4,10)]
    triple_letter_scores = [(1,5),(1,9),(5,1),(5,5),(5,9),(5,13)]
    for l in [triple_word_scores,double_letter_scores,double_word_scores,triple_letter_scores]:
        tmp_l = l[:]
        for j,(r,c) in enumerate(tmp_l):
            tmp_l[j] = (14-r,c)
        l.extend(tmp_l)
    return Board(15,15,set(double_letter_scores),set(double_word_scores),set(triple_letter_scores),set(triple_word_scores),(7,7))

class BoardState:
    def __init__(self,board):
        self.board = board
        self.played_letters = []
        for r in range(self.board.height):
            self.played_letters.append([' ']*self.board.width)
    def doPlay(self,squares,letters):
        # TODO: include validation logic
        for (r,c),letter in zip(squares,letters):
            self.played_letters[r][c] = letter
    def show(self):
        for r,row in enumerate(self.played_letters):
            for c,letter in enumerate(row):
                if (r,c) in self.board.triple_word_scores:
                    f = bg.red
                elif (r,c) in self.board.double_word_scores:
                    f = bg.magenta
                elif (r,c) in self.board.triple_letter_scores:
                    f = bg.blue
                elif (r,c) in self.board.double_letter_scores:
                    f = bg.cyan
                else:
                    f = lambda x: x
                if letter == ' ':
                    print_letter = '\u3000'
                else:
                    print_letter = chr(0xff00 + ord(letter)-ord('A')+ord("!"))
                print(f(print_letter),end="")
            print()
