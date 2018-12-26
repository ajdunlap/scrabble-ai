import itertools

class PlayerState:
    def __init__(self,wl,strategy,rack = [],score = 0):
        self.strategy = strategy
        self.rack = sorted(rack) # should always be sorted
        self.score = score
        self.wordlist = wl

    def get_move(self,bs):
        return self.strategy(self,bs)

    def all_racks(self):
        alphabet = list("abcdefghijklmnopqrstuvwxyz")
        j = 0
        while self.rack[j] == '.':
            j += 1
        for x in itertools.combinations_with_replacement(alphabet,j):
            yield ''.join(sorted(list(x) + list(self.rack[j:])))

    def add_to_rack(self,letters):
        self.rack += letters
        self.rack.sort()

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
                            proposal = [x for j,x in enumerate(proposal) if not main_pattern[j].isalpha()]
                            lcs = [l for l in effective_rack if l.islower()]
                            lc_options = []
                            for l in lcs:
                                lc_options.append([j for j,x in enumerate(proposal) if x == l.upper()])
                            for opts in itertools.product(*lc_options):
                                if len(set(opts)) < len(opts):
                                    continue
                                else:
                                    prop_list = list(proposal)
                                    for j in opts:
                                        prop_list[j] = prop_list[j].lower()
                                    yield ''.join(prop_list)

    def generate_board_possibilities(self,wl,bs):
        l = bs.get_places_to_play(len(self.rack))
        for x in l:
            main_word,cross_words = bs.get_words_produced(*x)
            main_word = main_word[0]
            cross_words = [cw[0] for cw in cross_words]
            for possibility in self.generate_place_possibilities(wl,main_word,cross_words):
                yield x[1],possibility

    def generate_scored_possibilities(self,wl,bs):
        return ((z,bs.score(*z)) for z in self.generate_board_possibilities(wl,bs))
