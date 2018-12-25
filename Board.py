from ansi.colour import fg,bg
import itertools

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
    def do_play(self,squares,letters):
        # TODO: include validation logic
        for (r,c),letter in zip(squares,letters):
            self.played_letters[r][c] = letter
    def show(self,highlight = []):
        for r,row in enumerate(self.played_letters):
            for c,letter in enumerate(row):
                if (r,c) in highlight:
                    f = bg.yellow
                elif (r,c) in self.board.triple_word_scores:
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
    def next(self,f,g,r,c):
        while True:
            r = f(r)
            c = g(c)
            if r < 0 or c < 0 or r >= self.board.width or c >= self.board.height:
                return False
            elif self.played_letters[r][c] == ' ':
                return (r,c)
    def next_up(self,r,c):
        return self.next(lambda r: r-1, lambda c: c,r,c)
    def next_down(self,r,c):
        return self.next(lambda r: r+1, lambda c: c,r,c)
    def next_left(self,r,c):
        return self.next(lambda r: r, lambda c: c-1,r,c)
    def next_right(self,r,c):
        return self.next(lambda r: r, lambda c: c+1,r,c)
    def adjacent_squares(self,r,c):
        rv = []
        if r > 0:
            rv.append((r-1,c))
        if r < self.board.height-1:
            rv.append((r+1,c))
        if c > 0:
            rv.append((r,c-1))
        if c < self.board.width-1:
            rv.append((r,c+1))
        return rv

    def get_places_to_play_from_start(self,rack_size,r0,c0,squaress):
        for dirs in [(self.next_up,self.next_down),(self.next_left,self.next_right)]:
            for back in range(0,rack_size):
                r = r0
                c = c0
                back_failed = False
                back_squares = [(r,c)]
                for b in range(back):
                    v = dirs[0](r,c)
                    if v:
                        (r,c) = v
                        back_squares.append(v)
                    else:
                        back_failed = True
                        break
                if back_failed:
                    break
                for forward in range(0,rack_size-back):
                    squares = back_squares.copy()
                    r = r0
                    c = c0
                    forward_failed = False
                    for f in range(forward):
                        v = dirs[1](r,c)
                        if v:
                            (r,c) = v
                            squares.append(v)
                        else:
                            forward_failed = True
                            break
                    if forward_failed:
                        break
                    else:
                        squares.sort()
                        if squares not in squaress:
                            squaress.append(squares)

    def get_places_to_play_not_first_turn(self,rack_size):
        squaress = []
        for r0,c0 in itertools.product(range(self.board.height),range(self.board.width)):
            if self.played_letters[r0][c0] == ' ' and any(self.played_letters[r][c] == ' ' for r,c in self.adjacent_squares(r0,c0)):
                self.get_places_to_play_from_start(rack_size,r0,c0,squaress)
        return squaress

    def get_places_to_play_first_turn(self,rack_size):
        squaress = []
        self.get_places_to_play_from_start(rack_size,self.board.starting_square[0],self.board.starting_square[1],squaress)
        return squaress

    def get_places_to_play(self,rack_size):
        if self.played_letters[self.starting_square[0]][self.starting_square[1]] == ' ':
            return self.get_places_to_play_first_turn(rack_size)
        else:
            return self.get_places_to_play_not_first_turn(rack_size)
