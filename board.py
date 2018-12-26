from ansi.colour import fg,bg
import itertools
import copy

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
    def __init__(self,board,played_letters = None):
        self.board = board
        if played_letters:
            self.played_letters = played_letters
        else:
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

    def next_open(self,f,r,c):
        while True:
            r,c = f(r,c)
            if r < 0 or c < 0 or r >= self.board.width or c >= self.board.height:
                return False
            elif self.played_letters[r][c] == ' ':
                return (r,c)

    def go_up(self,r,c):
        return (r-1,c)

    def go_down(self,r,c):
        return (r+1,c)

    def go_left(self,r,c):
        return (r,c-1)

    def go_right(self,r,c):
        return (r,c+1)

    def next_open_up(self,r,c):
        return self.next_open(self.go_up,r,c)

    def next_open_down(self,r,c):
        return self.next_open(self.go_down,r,c)

    def next_open_left(self,r,c):
        return self.next_open(self.go_left,r,c)

    def next_open_right(self,r,c):
        return self.next_open(self.go_right,r,c)

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
        for dirs in [(self.next_open_up,self.next_open_down,"vertical"),(self.next_open_left,self.next_open_right,"horizontal")]:
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
                        to_add = (dirs[2],squares)
                        if to_add not in squaress:
                            squaress.append(to_add)

    def get_word_in_direction(self,direction,r0,c0):
        go_back = go_forward = None
        if direction == "vertical":
            go_back = self.go_up
            go_forward = self.go_down
        elif direction == "horizontal":
            go_back = self.go_left
            go_forward = self.go_right
        else:
            print(direction)
            assert False
        r = r0
        c = c0
        while True:
            v = go_back(r,c)
            if v:
                rr,cc = v
                if self.played_letters[rr][cc] != ' ':
                    r = rr
                    c = cc
                else:
                    break
        rv = []
        while True:
            rv.append(self.played_letters[r][c])
            v = go_forward(r,c)
            if v:
                rr,cc = v
                if self.played_letters[rr][cc] != ' ':
                    r = rr
                    c = cc
                else:
                    break
        return ''.join(rv)

    def make_proposal(self,squares):
        new_board = BoardState(self.board,copy.deepcopy(self.played_letters))
        for j,(r,c) in enumerate(squares):
            new_board.played_letters[r][c] = str(j)
        return new_board

    def get_words_produced(self,direction,squares):
        proposed_board = self.make_proposal(squares)
        main_word = proposed_board.get_word_in_direction(direction,*squares[0])
        cross_words = []
        other_direction = "horizontal" if direction == "vertical" else "vertical"
        for sq in squares:
            word = proposed_board.get_word_in_direction(other_direction,*sq)
            if len(word) > 1:
                cross_words.append(word)
        return main_word,cross_words

    def get_places_to_play_not_first_turn(self,rack_size):
        squaress = []
        for r0,c0 in itertools.product(range(self.board.height),range(self.board.width)):
            if self.played_letters[r0][c0] == ' ' and any(self.played_letters[r][c] != ' ' for r,c in self.adjacent_squares(r0,c0)):
                self.get_places_to_play_from_start(rack_size,r0,c0,squaress)
        return squaress

    def get_places_to_play_first_turn(self,rack_size):
        squaress = []
        self.get_places_to_play_from_start(rack_size,self.board.starting_square[0],self.board.starting_square[1],squaress)
        return squaress

    def get_places_to_play(self,rack_size):
        if self.played_letters[self.board.starting_square[0]][self.board.starting_square[1]] == ' ':
            return self.get_places_to_play_first_turn(rack_size)
        else:
            return self.get_places_to_play_not_first_turn(rack_size)

bs = BoardState(make_official_scrabble_board())
bs.do_play([(7,7),(7,8),(7,9),(7,10)],"ECHO")
l = bs.get_places_to_play(7)
x = l[100]
