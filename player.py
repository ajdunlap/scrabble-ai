import itertools

class PlayerState:
    def __init__(self,rack = []):
        self.rack = sorted(rack) # should always be sorted
        self.score = 0

    def all_racks(self):
        alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        j = 0
        while self.rack[j] == '.':
            j += 1
        for x in itertools.combinations_with_replacement(alphabet,j):
            yield ''.join(sorted(list(x) + list(self.rack[j:])))

    def generate_possibilities(self,wordlist,main_pattern,side_patterns):
        num_to_play = len([x for x in main_pattern if not x.isalpha()])
        on_board = [x for x in main_pattern if x.isalpha()]
        for effective_rack in self.all_racks():
            for to_play in itertools.combinations(effective_rack,num_to_play):
                for proposal in wordlist.sorted_words[''.join(sorted(list(to_play)+list(on_board)))]:
                    matching = {}
                    for p,q in zip(main_pattern,proposal):
                        if p.isalpha():
                            if p != q:
                                break
                        else:
                            matching[p] = q
                    else:
                        for pattern in [main_pattern] + side_patterns:
                            resolved = ''.join(matching[p] if not p.isalpha() else p for p in pattern)
                            if resolved not in wordlist.words:
                                break
                        else:
                            yield ''.join(x for j,x in enumerate(proposal) if not main_pattern[j].isalpha())
