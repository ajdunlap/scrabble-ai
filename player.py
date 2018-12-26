import itertools

class PlayerState:
    def __init__(self,rack = []):
        self.rack = sorted(rack) # should always be sorted
        self.score = 0

    def all_racks(self):
        alphabet = list("abcdefghijklmnopqrstuvwxyz")
        j = 0
        while self.rack[j] == '.':
            j += 1
        for x in itertools.combinations_with_replacement(alphabet,j):
            yield ''.join(sorted(list(x) + list(self.rack[j:])))

    def generate_place_possibilities(self,wordlist,main_pattern,side_patterns):
        num_to_play = len([x for x in main_pattern if not x.isalpha()])
        on_board = [x for x in main_pattern if x.isalpha()]
        for effective_rack in self.all_racks():
            for to_play in itertools.combinations(effective_rack,num_to_play):
                for proposal in wordlist.sorted_words[''.join(sorted(map(lambda x: x.upper(),list(to_play)+list(on_board))))]:
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

    def generate_board_possibilities(self,wl,bs):
        l = bs.get_places_to_play(len(self.rack))
        for x in l:
            bs.show(x[1])
            main_word,cross_words = bs.get_words_produced(*x)
            main_word = main_word[0]
            cross_words = [cw[0] for cw in cross_words]
            for possibility in self.generate_place_possibilities(wl,main_word,cross_words):
                yield x[1],possibility
