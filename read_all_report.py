import os

def do_sth():
    for root, dirs, files in os.walk('.', topdown=False):
        # print(root, dirs, files)
        for name in files:
            print(os.path.join(root, name))
        for name in dirs:
            print(os.path.join(root, name))
        # for file in files:
        #     print(file)
        #     # zf.write('persist/excels/' + file)


if __name__ == '__mian__':
    do_sth()