from textnode import TextNode
from generator import copy_directory

def main():
    copy_directory("static", "public")
    
main()