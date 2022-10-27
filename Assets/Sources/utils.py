def log(*s: str): 
    for line in s: 
        print('\033[1m' + '\033[93m' + line + '\033[0m', end=' ')
    print()