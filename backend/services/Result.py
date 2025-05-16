'''
Object to represent a result.
'''
class Result:
    def __init__(self, title="", display_name="", top_thread=None, top_comment=None):
        self.title = title
        self.display_name = display_name
        self.top_thread = top_thread
        self.top_comment = top_comment