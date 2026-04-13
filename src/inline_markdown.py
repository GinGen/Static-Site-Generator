from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for old_node in old_nodes:
        # If it's not a TEXT node, we just pass it through untouched
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        # Split the text by the delimiter
        sections = old_node.text.split(delimiter)
        
        # If the length of sections is even, it means a delimiter was opened but never closed
        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid markdown: formatted section not closed. Delimiter: '{delimiter}'")
            
        # Build the new nodes based on their index
        for i in range(len(sections)):
            # If the string is empty, we don't need to create an empty node for it
            if sections[i] == "":
                continue
                
            # Even indexes are standard text, odd indexes are the new formatted type
            if i % 2 == 0:
                new_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(sections[i], text_type))
                
    return new_nodes

def extract_markdown_images(text):
    # Regex breakdown:
    # \!\[      -> matches the literal "!["
    # (.*?)     -> Capture group 1: matches any characters lazily (the alt text)
    # \]\(      -> matches the literal "]("
    # (.*?)     -> Capture group 2: matches any characters lazily (the URL)
    # \)        -> matches the literal ")"
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    # Regex breakdown:
    # (?<!!)    -> Negative lookbehind: ensures the match DOES NOT start with "!"
    # \[        -> matches the literal "["
    # (.*?)     -> Capture group 1: matches any characters lazily (the anchor text)
    # \]\(      -> matches the literal "]("
    # (.*?)     -> Capture group 2: matches any characters lazily (the URL)
    # \)        -> matches the literal ")"
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        
        # If there are no images, just add the node as-is and move on
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
            
        for image in images:
            image_alt = image[0]
            image_url = image[1]
            image_markdown = f"![{image_alt}]({image_url})"
            
            # Split the text exactly once based on this specific image markdown
            sections = original_text.split(image_markdown, 1)
            
            # If sections isn't exactly length 2, something went wrong with the split
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
                
            # Add the text before the image (if it's not empty)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
            # Add the image node
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            
            # Update original_text to be whatever is left after the image
            original_text = sections[1]
            
        # Don't forget to append any remaining text after the final image!
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
            
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
            
        for link in links:
            link_text = link[0]
            link_url = link[1]
            # The only difference from the image function is missing the "!"
            link_markdown = f"[{link_text}]({link_url})"
            
            sections = original_text.split(link_markdown, 1)
            
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
                
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            original_text = sections[1]
            
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
            
    return new_nodes

def text_to_textnodes(text):
    # Start with a single node containing the entire raw text
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Pass the list through every single extraction function
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes