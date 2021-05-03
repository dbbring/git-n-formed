from discord import Embed


class PostItem(object):

    content = ''
    link = ''
    image = ''
    embed: Embed = None

    def __init__(self, content: str = '', link: str = '', image: str = '', embed: Embed = None) -> None:
        super().__init__()
        self.content = content
        self.link = link
        self.image = image
        self.embed = embed
        return


class AdItem(PostItem):

    def __init__(self, content: str = '', link: str = '', image: str = '', embed: Embed = None) -> None:
        super().__init__(content=content, link=link, image=image, embed=embed)
