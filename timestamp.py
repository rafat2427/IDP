import os.path

yourpath="Hello"
parent_dir = os.path.abspath(os.path.join(yourpath, os.pardir))
path = os.path.join(parent_dir, yourpath)

try:
    os.makedirs(path, exist_ok = True)
    print("Directory '%s' created successfully" % yourpath)
except OSError as error:
    print("Directory '%s' can not be created" % yourpath) 
