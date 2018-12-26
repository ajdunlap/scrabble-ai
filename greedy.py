def greedy_strategy(p,board):
    options = p.generate_scored_possibilities(p.wordlist,board)
    try:
        return max(options,key=lambda x:x[1])[0]
    except ValueError:
        return 'pass'
