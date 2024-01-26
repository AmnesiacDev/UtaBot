
from nextcord import Embed


def createEmbed(color, title, body, image, thumbnail, footer):
    embed = Embed(color=color, title=title)
    embed.set_image(image)
    embed.set_thumbnail(thumbnail)

    embed.add_field(name= "", value=f'{body}'.format(body)
                    , inline=False)
    embed.set_footer(text=footer)
    return embed
