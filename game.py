import random
import Board

rack_size = 7
official_starting_tiles = "..EEEEEEEEEEEEAAAAAAAAAIIIIIIIIIOOOOOOOONNNNNNRRRRRRTTTTTTLLLLSSSSUUUUDDDDGGGBBCCMMPPFFHHVVWWYYKJXQZ"

class Game:
  def __init__(self, *, players, board=None):
    """players is a list of Players"""
    self.players = players
    self.board = board
    if self.board is None:
      self.board = Board.make_official_scrabble_board()
    self.remaining_tiles = random.shuffle(starting_tiles)
    for p in self.players:
      fill_rack(p)
    # Determine turn order by sorting by the first letter they got
    self.players.sort(key=lambda p: p.rack[0])

  def fill_rack(self, player):
    num_needed = rack_size - len(player.rack)
    assert num_needed >= 0
    if num_needed > len(self.remaining_tiles):
      num_needed = len(self.remaining_tiles)
    player.rack += self.remaining_tiles[:num_needed]
    del self.remaining_tiles[:num_needed]
    
  def run(show_boards=False):
    run_turns(show_boards)
    return max(self.players, key=lambda p: p.score)
    
  def run_turns(show_boards):
    ready_to_end = []
    while True:
      for p in self.players:
        move = p.get_move(self.board)
        if move == 'pass':
          if p not in ready_to_end:
            ready_to_end.append(p)
            if len(ready_to_end) == len(self.players):
              return
        # TODO: Allow exchange
        p.score += self.board.score(move)
        self.board.apply(move)
        fill_rack(p)
        if show_boards:
          self.board.show()
