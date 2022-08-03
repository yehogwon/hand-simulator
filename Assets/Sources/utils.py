def log(s: str): 
    print ('\033[1m' + '\033[93m' + s + '\033[0m')

if __name__ == '__main__': 
    log('Run on utils.py')
    print(b'nana')
    print(bytes('nana', 'utf-8'))