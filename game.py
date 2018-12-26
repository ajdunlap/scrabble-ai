import random
import board
import greedy
import player
import wordlist
import sys

rack_size = 7
official_starting_tiles = "..EEEEEEEEEEEEAAAAAAAAAIIIIIIIIIOOOOOOOONNNNNNRRRRRRTTTTTTLLLLSSSSUUUUDDDDGGGBBCCMMPPFFHHVVWWYYKJXQZ"

class Game:
  def __init__(self, *, players, bd=None,wl=None,seed = None):
    """players is a list of Players"""
    if not seed:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    print (seed)
    self.players = players
    self.wordlist = wl
    if self.wordlist is None:
        self.wordlist = wordlist.Wordlist("words")
    self.board = bd
    if self.board is None:
      self.board = board.make_official_scrabble_board()
    self.bs = board.BoardState(self.board)
    self.remaining_tiles = list(official_starting_tiles)
    random.shuffle(self.remaining_tiles)
    for p in self.players:
      self.fill_rack(p)
    # Determine turn order by sorting by the first letter they got
    self.players.sort(key=lambda p: p.rack[0])

  def fill_rack(self, player):
    num_needed = rack_size - len(player.rack)
    assert num_needed >= 0
    if num_needed > len(self.remaining_tiles):
      num_needed = len(self.remaining_tiles)
    player.add_to_rack(self.remaining_tiles[:num_needed])
    del self.remaining_tiles[:num_needed]
    
  def run(self,show_boards=False):
    self.run_turns(show_boards)
    for j,p in enumerate(self.players):
        p.score -= sum(board.letter_scores[t] for t in p.rack)
    self.show_board_and_scores()
    return max(self.players, key=lambda p: p.score)
    
  def run_turns(self,show_boards):
    ready_to_end = []
    while True:
      for p in self.players:
        move = p.get_move(self.bs)
        if move == 'pass':
          if p not in ready_to_end:
            ready_to_end.append(p)
            if len(ready_to_end) == len(self.players):
              return
        else:
            ready_to_end = []
            # TODO: Allow exchange
            p.score += self.bs.score(*move)
            self.bs.do_play(*move)
            print (move[1])
            for l in move[1]:
                if l.islower():
                    l = '.'
                print (l)
                print (p.rack)
                p.rack.remove(l)
            self.fill_rack(p)
            if not p.rack: # rack is empty after trying to refill it
                           # i.e. you just went out
                for op in self.players:
                    if op is not p:
                        p.score += sum(board.letter_scores[t] for t in op.rack)
                return
            if show_boards:
                self.show_board_and_scores()
  def show_board_and_scores(self):
        self.bs.show()
        for j,p in enumerate(self.players):
            print("Player ",j," score: ",p.score)
            print("       rack: ",''.join(p.rack))


#import pdb
#pdb.set_trace()
wl = wordlist.Wordlist("words")
p1 = player.PlayerState(wl,greedy.greedy_strategy)
p2 = player.PlayerState(wl,greedy.greedy_strategy)
g = Game(players=[p1,p2])
g.run(True)
