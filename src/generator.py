import os
import shutil
import re
from markdown_blocks import markdown_to_html_node
from htmlnode import HTMLNode

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
    if os.path.isfile(curr):
        shutil.copy(curr, os.path.join(dest, file))
        print(f"copied file is {file}")
    elif os.path.isdir(curr):
        new_dir = os.path.join(dest,file)
        os.mkdir(new_dir)
        recursion_copy(curr, new_dir, os.listdir(curr))
    recursion_copy(source, dest, file_list)
    
def extract_title(md):
    f = open(md)
    text = f.read()
    title = re.match(r"(?m)^#(?!#)(.*)", text)
    if title is None:
        raise Exception("No title could not be found")
    else:
        
        return title.group().lstrip("#").strip()

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")
    html_title = extract_title(from_path)
    from_file = open(from_path)
    og_file_content = from_file.read()
    from_file.close()
    template_file = open(template_path)
    template_file_content = template_file.read()
    template_file.close()
    og_html = markdown_to_html_node(og_file_content).to_html()
    cleaned_html = re.sub(r"<h1>(.*)<\/h1>", "", og_html)
    template_file_content = template_file_content.replace("{{ Title }}", html_title)
    template_file_content = template_file_content.replace("{{ Content }}", cleaned_html)
    
    if not os.path.exists(dest_path):
        print(f"created new dir : {dest_path}")
        os.makedirs(dest_path, exist_ok=True)
    
    with open(dest_path + "/index.html", "w+") as f:
        f.write(template_file_content)
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    path_list = os.listdir(dir_path_content)
    if not path_list:
        return 0
    for path in path_list:
        full_path = os.path.join(dir_path_content,path)
        if os.path.isfile(full_path):
            generate_page(full_path, template_path, dest_dir_path)
        elif os.path.isdir(full_path):
            new_dir = os.path.split(full_path)[-1]
            generate_pages_recursive(full_path, template_path, dest_dir_path+ "/" + new_dir)


    
    
    
    
    
    
    
    