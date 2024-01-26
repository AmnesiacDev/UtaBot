
import nextcord
from nextcord import Embed, Color


def message_log(statType, msg):

    if statType == 0:
        color = Color.red()
        status = "Message Deleted"
        message = msg
        stamp = "Message"
    else:
        color = Color.yellow()
        status = "Message Edited"
        message = msg[0]
        stamp = "Message Before"

    embed = Embed(color=color, title=status)

    content = message.content
    channel = message.channel
    msgId = message.id
    msgUrl = message.jump_url
    author = message.author
    attachments = message.attachments

    everything = f'**Channel:** {channel.mention}\n**Author:** {author.name} - {author.mention}\n**Message ID:** {msgId} - {msgUrl}'

    embed.add_field(name="", value='>>> {}'.format(everything)
                    , inline=True)
    date = str(nextcord.utils.utcnow().date())
    time = f'{str(nextcord.utils.utcnow().hour)}:{str(nextcord.utils.utcnow().minute)}:{str(nextcord.utils.utcnow().second)}'

    embed.set_footer(text=f'{date} at {time}')
    embed.set_author(name=message.author.name, icon_url=message.author.avatar)

    if content:
        while True:

            embed.add_field(name=stamp, value='> {}'.format(content), inline=False)

            if statType == 1:
                content = msg[1].content
                stamp = "Message After"
                statType = 0
            else:
                break
    url = ''
    if attachments:
        for i in range(len(attachments)):
            url += f'{attachments[i].url}\n'

        embed.add_field(name="Attachment(s)", value='>>> {}'.format(url)
                        , inline=False)

    return embed


def punishment_log(statType, user, reason, duration):
    if statType == 0:
        Punishment = "Mute"
        color = Color.yellow()
    elif statType == 1:
        Punishment = "Kick"
        color = Color.orange()
    elif statType == 2:
        Punishment = "Ban"
        color = Color.red()
    elif statType == 3:
        Punishment = "Un-ban"
        color = Color.green()
    elif statType == 4:
        Punishment = "Un-mute"
        color = Color.blue()

    embed = Embed(color=color, title=Punishment)
    everything = f'**Name:** {user.name} - {user.mention}'
    if duration:
        everything = f'{everything}\n **Duration:** {duration}'
    everything = f'{everything}\n**Reason:** {reason}'
    embed.add_field(name="", value='>>> {}'.format(everything))

    date = str(nextcord.utils.utcnow().date())
    time = f'{str(nextcord.utils.utcnow().hour)}:{str(nextcord.utils.utcnow().minute)}:{str(nextcord.utils.utcnow().second)}'

    embed.set_footer(text=f'{date} at {time}')

    embed.set_author(name=user.name, icon_url=user.avatar)
    return embed

