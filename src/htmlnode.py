

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag #representing html tag ("p", "a")
        self.value = value #representing the value of the HTML tag (text inside a paragraph)
        self.children = children # list of HTMLNode representing the children of this node
        self.props = props #dictionary of key-value pairs, representing the attributes of the HTML tag
        #<a> tag might have {"href": :"google.com"}
        # all optional
        # None tag = raw text
        # None vlaue = have children
        # None children = have value
        # None props = wont have any attribute
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is None:
            return None
        final = ""
        for k,v in self.props.items():
            final += f" {k}=\"{v}\""
        return final

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
                    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError("leafnode has no value")
        if self.tag is None:
            return self.value
        html_props = self.props_to_html()
        if html_props is None:
            html_props = ""
        return f"<{self.tag}{html_props}>{self.value}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is not provided")
        if self.children is None:
            raise ValueError("No child on parent node")
        final_string = ""
        for child in self.children:
            final_string += child.to_html()
            
        return f"<{self.tag}>{final_string}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, {self.children}, {self.props})"


    