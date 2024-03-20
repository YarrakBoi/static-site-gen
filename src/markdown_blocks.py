import re
from htmlnode import LeafNode, ParentNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ulist = "unordered_list"
block_type_olist = "ordered_list"

def markdown_to_blocks(markdown):
    new = []
    text_blocks = re.split("(?:\\n){2,}", markdown)
    for text in text_blocks:
        if text == "":
            continue
        new.append(text.strip())
    return new

def block_to_block_type(block):
    lines = block.split("\n")
    if re.match(r"#{1,6} ", block):
        return block_type_heading
    if block.startswith("```") and block.endswith("```"):
        return block_type_code
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("1. "):
        counter = 1
        for line in lines:
            if not line.startswith(f"{counter}. "):
                return block_type_paragraph
            counter += 1    
        return block_type_olist
    return block_type_paragraph

def text_to_child(text):
    textnodes = text_to_textnodes(text)
    children = []
    for node in textnodes:
        children.append(text_node_to_html_node(node))
    return children

def conv_paragraph_to_html(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    return ParentNode("p", text_to_child(paragraph))    

def conv_heading_to_html(block):
    hash_count = 0
    for char in block:
        if char == "#":
            hash_count += 1
        else:
            break
    if hash_count > 6:
        raise Exception("More than 6 level of heading")
    if hash_count + 1 > len(block):
        raise Exception("invalid heading format")
    children = text_to_child(block[hash_count+1:])
    return ParentNode(f"h{hash_count}",children)
    

def conv_code_to_html(block):
    if not block.startswith("```") and not block.endswith("```"):
        raise Exception("invalid syntax for code block")
    code = block[3:-3] # remove ```
    return ParentNode("pre", text_to_child(code))

def conv_quote_to_html(block):
    lines = block.split("\n")
    cleaned_line = []
    for line in lines:
        if not line.startswith(">"):
            raise Exception("Invalid syntax for quote")
        cleaned_line.append(line.lstrip(">").strip())
    children = text_to_child(" ".join(cleaned_line))
    return ParentNode("blockquote", children)

def conv_ulist_to_html(block):
    lines = block.split("\n")
    cleaned_line = []
    for line in lines:
        if line.startswith("-"):
            cleaned_line.append(line.lstrip("-").strip())
        elif line.startswith("*"):
            cleaned_line.append(line.lstrip("*").strip())
    child = []
    for line in cleaned_line:
        child.append(ParentNode("li",text_to_child(line)))
    return ParentNode("ul", child)

def conv_olist_to_html(block):
    lines = block.split("\n")
    cleaned_line = []
    for line in lines:
        cleaned_line.append(line[3:])
    child = []
    for line in cleaned_line:
        child.append(ParentNode("li",text_to_child(line)))
    return ParentNode("ol", child)

def markdown_to_html_node(md):
    blocks = markdown_to_blocks(md)
    child_list = []
    for block in blocks:
        if block_to_block_type(block) == "paragraph":
            child_list.append(conv_paragraph_to_html(block))
        if block_to_block_type(block) == "heading":
            child_list.append(conv_heading_to_html(block))
        if block_to_block_type(block) == "quote":
            child_list.append(conv_quote_to_html(block))
        if block_to_block_type(block) == "code":
            child_list.append(conv_code_to_html(block))
        if block_to_block_type(block) == "unordered_list":
            child_list.append(conv_ulist_to_html(block))
        if block_to_block_type(block) == "ordered_list":
            child_list.append(conv_olist_to_html(block))
    return ParentNode("div", child_list)

            
            

    



