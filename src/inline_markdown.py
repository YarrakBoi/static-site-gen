from textnode import TextNode,text_type_bold,text_type_code,text_type_image,text_type_italic,text_type_link,text_type_text
import re 

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not node.text_type == text_type_text:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0 and node.text.count(delimiter) > 1:
            raise Exception(f"Invalid Markdown syntax, not closed {node.text.count(delimiter)}")
        split_text = node.text.split(delimiter)
        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(split_text[i], text_type_text))
            else:
                new_nodes.append(TextNode(split_text[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not node.text_type == text_type_text:
            new_nodes.append(node)
            continue
        image_link = extract_markdown_images(node.text)
        if not image_link:
            new_nodes.append(node)
            continue
        split_text = re.split(r"!(\[.*?\]\(.*?\))", node.text)
        for text in split_text:
            if text == "":
                continue
            if text.startswith("[") and text.endswith(")"):
                if len(image_link) >= 1:
                    image_tup = image_link.pop(0)
                    new_nodes.append(TextNode(image_tup[0], text_type_image, image_tup[1]))
                    continue
            else:
                new_nodes.append(TextNode(text,text_type_text))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not node.text_type == text_type_text:
            new_nodes.append(node)
            continue
        image_link = extract_markdown_links(node.text)
        if not image_link:
            new_nodes.append(node)
            continue
        split_text = re.split(r"(?<!\!)(\[.*?\]\(.*?\))", node.text)
        for text in split_text:
            if text == "":
                continue
            if text.startswith("[") and text.endswith(")"):
                if len(image_link) >= 1:
                    image_tup = image_link.pop(0)
                    new_nodes.append(TextNode(image_tup[0], text_type_link, image_tup[1]))
                    continue
            else:
                new_nodes.append(TextNode(text,text_type_text))
    return new_nodes                                
            

def text_to_textnodes(text):
    base_node = [TextNode(text, text_type_text)]
    base_node = split_nodes_delimiter(base_node, "**", text_type_bold)
    base_node = split_nodes_delimiter(base_node, "*", text_type_italic)
    base_node = split_nodes_delimiter(base_node, "`", text_type_code)
    base_node = split_nodes_image(base_node)
    base_node = split_nodes_link(base_node)
    return base_node





