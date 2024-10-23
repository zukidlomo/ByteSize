from datetime import datetime
class Video:
    def __init__(self, name: str, tag: str):
        self.name = name
        self.tag = tag
        self.likes = 0
        self.views = 0
        self.last_viewed = None
    def add_like(self):
        self.likes += 1
    def view(self):
        self.views += 1
        self.last_viewed = datetime.now()
    def __repr__(self):
        return f"Video(name='{self.name}', tag='{self.tag}', likes={self.likes}, views={self.views})"