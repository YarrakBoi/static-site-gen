import os
import shutil

def copy_directory(source, dest):
    shutil.rmtree(dest) # make it idempotent
    os.mkdir(dest)
    file_list = os.listdir(source)
    if not file_list:
        return 0
    recursion_copy(source, dest, file_list)
    
def recursion_copy(source,dest,file_list):
    if not file_list:
        return 0
    file = file_list.pop()
    curr = os.path.join(source, file) 
    if os.path.exists(curr) == True and os.path.isfile(curr):
        shutil.copy(curr, os.path.join(dest, file))
        print(f"copied file is {file}")
    elif os.path.exists(curr) == True and os.path.isdir(curr):
        new_dir = os.path.join(dest,file)
        os.mkdir(new_dir)
        recursion_copy(curr, new_dir, os.listdir(curr))
    recursion_copy(source, dest, file_list)
    
    
    