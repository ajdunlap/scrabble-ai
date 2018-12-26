def greedy_strategy(p,board):
    options = p.generate_scored_possibilities(p.wordlist,board)
    return max(options,key=lambda x:x[1])[0]
