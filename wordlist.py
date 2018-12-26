from collections import defaultdict

class Wordlist:
    def __init__(self,fn):
        self.words = {}
        with open(fn) as f:
            for w in f:
                w = w.strip()
                self.words[w] = ''.join(sorted(w))
        self.sorted_words = defaultdict(set)
        for k,v in self.words.items():
            self.sorted_words[v].add(k)
