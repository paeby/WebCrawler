'''
 A page is composed of its static assets. It contains the style sheets, scripts and images. 
 The children of a page are the links to other pages accessible from this page.
'''
class Page:
    def __init__(self, n):
        self.name = n
        self.children = []
        self.style_sheets = []
        self.scripts = []
        self.images = []
    def get_str(self):
        s = '########   '+self.name+'   ########\n\n'
        s += '||Number of links: ' + str(len(self.children)) +'\n'
        for c in self.children:
            s += '\t - '+ c + '\n'
        s += '\n||Number of CSS stylesheets: ' + str(len(self.style_sheets)) +'\n'
        for f in self.style_sheets:
            s += '\t - '+ f + '\n'
        s += '\n||Number of scripts: ' + str(len(self.scripts)) +'\n'
        for f in self.scripts:
            s += '\t - '+ f + '\n'
        s += '\n||Number of images: ' + str(len(self.images)) +'\n'
        for f in self.images:
            s += '\t - '+ f + '\n'   
        s += '\n\n\n'
        return s