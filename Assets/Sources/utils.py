import pandas as pd

def log(*s: str): 
    for line in s: 
        print('\033[1m' + '\033[93m' + line + '\033[0m', end=' ')
    print()

def print_as_table(d: dict): 
    if d is None: 
        return
    df = pd.DataFrame(index=d.keys(), data=[[d[k][0], d[k][1]] for k in d.keys()])
    print(df)

if __name__ == '__main__': 
    log('Put a single parameter in the function log(). ')
    log('Run on utils.py', 'This string is separated by a comma. If this statement works without any error, it means the function log() can take multiple string parameters. ')
    print(b'nana')
    print(bytes('nana', 'utf-8'))