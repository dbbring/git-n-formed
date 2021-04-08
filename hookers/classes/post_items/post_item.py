class PostItem(object):

    content = ''
    link = ''
    image = ''

    def __init__(self, content='', link='', image='') -> None:
        super().__init__()
        self.content = content
        self.link = link
        self.image = image
        return
