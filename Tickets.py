import nextcord
from nextcord.ext import menus
import random
import EmbedCreator
from nextcord import Embed, Color, Interaction, User


def endEmbed():
    return EmbedCreator.createEmbed(Color.magenta(), "End Ticket", "",
                                    "https://cdn.discordapp.com/attachments/1158507268950724699/1162785703160197230/878ec4d4b0e58c00402790ede80b8bcc.jpg?ex=653d3393&is=652abe93&hm=ed66083355a94384ca3b76de4bf770fa4402ec32a86364d3dd8147412ceb1286&",
                                    "", "")


class EndTicketMenu(menus.ButtonMenu):
    channelName = ""
    userName = User

    def setName(self, name, user):
        self.channelName = name
        self.userName = user

    async def send_initial_message(self, ctx, channel):
        finalEmbed = endEmbed()

        for i in self.interaction.guild.channels:
            if i.name == self.channelName:
                await i.send(embed=finalEmbed, view=self)

        return await self.interaction.original_message()

    @nextcord.ui.button(label="End Ticket", style=4)
    async def end_ticket(self, button, interaction):
        for i in self.interaction.guild.channels:
            if i.name == self.channelName:
                await i.delete()


class CreateTicketMenu(menus.ButtonMenu):
    finalEmbed = Embed

    def createEmbed(self, colorFinal, title, body, image, thumbnail, footer):
        embed = EmbedCreator.createEmbed(colorFinal, title, body, image, thumbnail, footer)
        self.finalEmbed = embed

    async def send_initial_message(self, ctx, channel):
        await channel.send(embed=self.finalEmbed, view=self)
        await self.interaction.send("‎ ")
        return await self.interaction.original_message()

    @nextcord.ui.button(label="Open a Ticket", style=1)
    async def ticket(self, button, interaction):
        number = random.randrange(1, 100)
        channelList = self.interaction.guild.channels

        for i in channelList:
            chNumber = i.name.replace("ticket-", "")
            print(chNumber)
            while str(number) == chNumber:
                number = random.randrange(1, 100)

        guild = self.interaction.guild
        channelName = f'ticket-{number}'
        overwrites = {
            self.interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            self.interaction.user: nextcord.PermissionOverwrite(read_messages=True),
        }
        await guild.create_text_channel(name=channelName, category=self.message.channel.category, overwrites=overwrites)
        end = EndTicketMenu()
        end.setName(channelName, self.interaction.user)

        await end.start(interaction=Interaction)
