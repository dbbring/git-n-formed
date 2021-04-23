from discord import Embed


class PostItem(object):

    content = ''
    link = ''
    image = ''
    embed: Embed = None

    def __init__(self, content='', link='', image='', embed=None) -> None:
        super().__init__()
        self.content = content
        self.link = link
        self.image = image
        self.embed = embed
        return
