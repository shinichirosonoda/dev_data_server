import glob

def file_check(file_name):
    if len(glob.glob(file_name)) > 0:
        return True
    else:
        return False
 

if __name__ == '__main__':
    print(file_check("./test"))
