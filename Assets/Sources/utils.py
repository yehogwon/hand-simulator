import pandas as pd

def log(s: str): 
    if s is None:
        return
    print ('\033[1m' + '\033[93m' + s + '\033[0m')

def print_as_table(d: dict): 
    if d is None: 
        return
    df = pd.DataFrame(index=d.keys(), columns=['x', 'y', 'z'], data=[[d[k][0], d[k][1], d[k][2]] for k in d.keys()])
    print(df)

if __name__ == '__main__': 
    log('Run on utils.py')
    print(b'nana')
    print(bytes('nana', 'utf-8'))