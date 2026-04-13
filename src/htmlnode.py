class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementatedError("to_html method is not implemented")

    def props_to_html(self):
        if self.props is None:
            return "" 
        props_string = ""
        for key, value in self.props.items():
            props_string += f' {key}="{value}"'
            
        return props_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        # A leaf node absolutely must have a value
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        
        # If there is no tag, it's just raw text
        if self.tag is None:
            return self.value
            
        # Otherwise, render the full HTML tag using the parent's props_to_html method
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: parent node must have a tag")
        if self.children is None:
            raise ValueError("Invalid HTML: parent node must have children")
    
        # Create an empty string to hold the rendered children
        children_html = ""
        
        # Recursively call to_html() on every child
        for child in self.children:
            children_html += child.to_html()
            
        # Wrap the concatenated children in the parent's tags
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
    