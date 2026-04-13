from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")

    # Heading: 1 to 6 hash characters followed by a space
    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return BlockType.HEADING

    # Code: Starts with ``` and ends with ```
    if len(block) >= 6 and block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Quote: Every line must start with a > character
    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE

    # Unordered List: Every line must start with a "- "
    is_ul = True
    for line in lines:
        if not line.startswith("- "):
            is_ul = False
            break
    if is_ul:
        return BlockType.UNORDERED_LIST

    # Ordered List: Every line starts with "1. ", "2. ", etc.
    is_ol = True
    for i, line in enumerate(lines):
        expected_start = f"{i + 1}. "
        if not line.startswith(expected_start):
            is_ol = False
            break
    if is_ol:
        return BlockType.ORDERED_LIST

    # Fallback to normal paragraph
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    # Split the raw string by double newlines
    raw_blocks = markdown.split("\n\n")
    
    final_blocks = []
    for block in raw_blocks:
        # Strip leading and trailing whitespace
        stripped_block = block.strip()
        
        # Only add the block if it's not entirely empty
        if stripped_block != "":
            final_blocks.append(stripped_block)
            
    return final_blocks