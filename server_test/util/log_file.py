# log_file.py
# coding by Shinichiro Sonoda
# Nov. 4th 2020

# error log save
def log_file(message, log_file_name='test.log' ):
    try:
        with open( log_file_name, 'r') as f:
            data = f.read() + message
            f.close()
        with open( log_file_name, 'w') as f: 
            print(data, file=f)
            f.close()

    except FileNotFoundError as e:
        with open( log_file_name, 'w') as f: 
            print(message, file=f)
            f.close()

if __name__ == '__main__':
    log_file("test")
