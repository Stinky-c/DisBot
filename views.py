import disnake

class LinkView(disnake.ui.View):
    '''
    Takes list of tuples to add buttons addcordingly
    `[("Label","Link"),("label2","link2")]`
    or a singular tuple following the same scheme
    `("label","link")`
    '''
    def __init__(self, link:tuple=None,links:list=None):
        super().__init__()
        if link:
            self.add_item(disnake.ui.Button(label=link[0],url=link[1],style=disnake.ButtonStyle.link))
        if links:
            for i in links:  
                self.add_item(disnake.ui.Button(label=i[0],url=i[1],style=disnake.ButtonStyle.link))