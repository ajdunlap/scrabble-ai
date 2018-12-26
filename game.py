import random
import board
import greedy
import player
import wordlist

rack_size = 7
official_starting_tiles = "..EEEEEEEEEEEEAAAAAAAAAIIIIIIIIIOOOOOOOONNNNNNRRRRRRTTTTTTLLLLSSSSUUUUDDDDGGGBBCCMMPPFFHHVVWWYYKJXQZ"

class Game:
  def __init__(self, *, players, bd=None,wl=None):
    """players is a list of Players"""
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
    return max(self.players, key=lambda p: p.score)
    
  def run_turns(self,show_boards):
    ready_to_end = []
    #while True:
    for i in range(10):
      for p in self.players:
        move = p.get_move(self.bs)
        if move == 'pass':
          if p not in ready_to_end:
            ready_to_end.append(p)
            if len(ready_to_end) == len(self.players):
              return
        # TODO: Allow exchange
        p.score += self.bs.score(*move)
        self.bs.do_play(*move)
        for l in move[1]:
            if l.islower():
                l = '.'
            p.rack.remove(l)
        self.fill_rack(p)
        if show_boards:
          self.bs.show()
          for j,p in enumerate(self.players):
              print("Player ",j," score: ",p.score)
              print("       rack: ",''.join(p.rack))

wl = wordlist.Wordlist("words")
p1 = player.PlayerState(wl,greedy.greedy_strategy)
p2 = player.PlayerState(wl,greedy.greedy_strategy)
g = Game(players=[p1,p2])
g.run(True)
