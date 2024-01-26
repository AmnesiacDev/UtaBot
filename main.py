import datetime, pyrebase, config
import humanfriendly
import nextcord, math
from nextcord.ext import commands
import requests
import Tickets, EmbedCreator, Logs
from nextcord.ext import tasks
from nextcord import Intents, Color, Interaction, SlashOption

intents = Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

color_class = [Color.blue(), Color.red(), Color.green(), Color.magenta(), Color.dark_magenta(), Color.dark_grey(),
               Color.dark_green(), Color.dark_gold(), Color.orange(), Color.purple()]
conf = {
  "apiKey": "AIzaSyB58KL2jN6ABvd4K_uu9xU2bJAMcGGQUiw",
  "authDomain": "thebread-2.firebaseapp.com",
  "databaseURL": "https://thebread-2-default-rtdb.firebaseio.com/",
  "projectId": "thebread-2",
  "storageBucket": "thebread-2.appspot.com",
  "messagingSenderId": "1020569653651",
  "appId": "1:1020569653651:web:3a4cc6a64444a2501b1866",
  "measurementId": "G-SJGQ08VR4H"
}

imgList = ["https://media.discordapp.net/attachments/1200255898589872168/1200256881126559844/0_-removebg-preview.png?ex=65c58554&is=65b31054&hm=ad6759f65dd3149070d6769e159e7256baa9a4e334c56a215fafcbe54d048b71&=&format=webp&quality=lossless",
           "https://media.discordapp.net/attachments/1200255898589872168/1200256880895852595/15_-removebg-preview.png?ex=65c58554&is=65b31054&hm=09cc5e97bdab904b203f237afc8e74581676218cd938ac3ebe4e7916e441f41f&=&format=webp&quality=lossless",
           "https://media.discordapp.net/attachments/1200255898589872168/1200256881856368720/30_-removebg-preview.png?ex=65c58554&is=65b31054&hm=433a1c672cdaf0e5b97a7e13ff2308b251819f6767dc2913410d5e2de9c2e5ae&=&format=webp&quality=lossless",
           "https://media.discordapp.net/attachments/1200255898589872168/1200256882078650398/50_-removebg-preview.png?ex=65c58554&is=65b31054&hm=c27dd16d983c1503b10bd3674b5fe88439f5778a27b0650c3e99c865b6809d3d&=&format=webp&quality=lossless",
           "https://media.discordapp.net/attachments/1200255898589872168/1200256881344647178/80_-removebg-preview.png?ex=65c58554&is=65b31054&hm=7b8267b83e37e07c787c1c88aa39f8e5185ad92a8dc05c7d149a891b76e08947&=&format=webp&quality=lossless",
           "https://media.discordapp.net/attachments/1200255898589872168/1200256881608884334/90_-removebg-preview.png?ex=65c58554&is=65b31054&hm=bad235fbe8289d90ecc7697f4c73dc11772490373c78be1a2c7e3347bf729661&=&format=webp&quality=lossless",
           "https://media.discordapp.net/attachments/1200255898589872168/1200256882317721660/97_-removebg-preview.png?ex=65c58554&is=65b31054&hm=3a2b82f6d99ec0d14a70b3bb03e87e13ae3c2afe68c6d155f644b0ba773c1549&=&format=webp&quality=lossless"]
firebase = pyrebase.initialize_app(conf)
db = firebase.database()

print(db.child("Users").get().val())

endTicketImage = ""
roleName = ""
twitchPingImage = ""

welcomeImage = ""
welcomeMessage = ""
welcomeChannel = ""


messageLogs = ""
punishmentLogs = ""


TWITCH_CHANNEL_NAME = "its_bbananabread"
CLIENT_ID = "wulmh9v3jhdwgnlf53qisql36m62dg"
CHANNEL_ID = "boub7atx4rbdbstn8klrufp6ovz2qa"

async def check_twitch():
    url = f"https://api.twitch.tv/helix/streams?user_login={TWITCH_CHANNEL_NAME}"
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {CHANNEL_ID}"  # Replace with your new OAuth token
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    if "data" in data and data["data"]:
        return data
    else:
        return 0


creatorId = [991043009070125166, 409794671418802177]
serverId = 1086626877034221598
levelChannel = 1200293742322655353
modRole = 1187465633462489119


@bot.slash_command(guild_ids=[serverId])
async def welcome_channel(interaction: Interaction, welcome_message: str, welcome_channel: str, welcome_image: str):
    global welcomeChannel, welcomeImage, welcomeMessage
    if interaction.user.id in creatorId:
        welcomeMessage, welcomeImage = welcome_message, welcome_image
        welcomeChannel = welcome_channel.replace("#", "").replace("<", "").replace(">", "")
        await interaction.response.send_message("Updated successfully")
    else:
        await interaction.response.send_message("You do not have permission to use this command")


@bot.slash_command(guild_ids=[serverId])
async def test(interaction: Interaction):
    model = Tickets.EndReason()
    await interaction.response.send_modal(model)


@bot.slash_command(guild_ids=[serverId])
async def bot_config(interaction: Interaction, message_logs: str = "",
                     punishment_logs: str = "", end_ticket_image: str = "", twitch_ping_image: str = ""):
    global creatorId
    if interaction.user.id == interaction.guild.owner_id or interaction.user.id == creatorId:
        global endTicketImage, messageLogs, punishmentLogs, twitchPingImage

        if twitch_ping_image:
            twitchPingImage = twitch_ping_image

        if message_logs:
            messageLogs = message_logs.replace("#", "").replace("<", "").replace(">", "")

        if punishment_logs:
            punishmentLogs = punishment_logs.replace("#", "").replace("<", "").replace(">", "")

        if end_ticket_image:
            endTicketImage = end_ticket_image

        await interaction.response.send_message("Config has been set successfully")
    else:
        await interaction.response.send_message("You do not have permission to use this command")


@bot.slash_command(guild_ids=[serverId])
async def create_ticket(interaction: Interaction,
                        color: int = SlashOption(name="color", choices={"Blue": 0, "Red": 1, "Green": 2, "Pink": 3,
                                                                        "Magenta": 4, "Gray": 5, "Dark green": 6,
                                                                        "Gold": 7, "Orange": 8, "Purple": 9}),
                        title: str = "", body: str = "", image: str = "",
                        thumbnail: str = "", footer: str = ""):
    global roleName
    global creatorId
    for i in interaction.guild.roles:
        if i.name == roleName or interaction.user.id == interaction.guild.owner_id or interaction.user.id == creatorId:
            ender = False
            if i in interaction.user.roles or interaction.user.id == interaction.guild.owner_id:

                colorFinal = color_class[color]

                body = body.replace("%n", f'\n')
                ticket = Tickets.CreateTicketMenu()
                ticket.createEmbed(colorFinal, title, body, image, thumbnail, footer)

                await ticket.start(interaction=interaction)

            else:
                await interaction.response.send_message("No permission")
            break
    if ender:
        await interaction.response.send_message("No permission")


@bot.slash_command(guild_ids=[serverId])
async def create_embed(interaction: Interaction,
                       color: int = SlashOption(name="color", choices={"Blue": 0, "Red": 1, "Green": 2, "Pink": 3,
                                                                       "Magenta": 4, "Gray": 5, "Dark green": 6,
                                                                       "Gold": 7, "Orange": 8, "Purple": 9}),
                       title: str = "", body: str = "", image: str = "",
                       thumbnail: str = "", footer: str = ""):
    try:
        colorFinal = color_class[color]

        body = body.replace("%n", f'\n')

        embed = EmbedCreator.createEmbed(colorFinal, title, body, image, thumbnail, footer)

        await interaction.response.send_message(embed=embed)

    except:
        print("something went wrong")




@bot.slash_command(guild_ids=[serverId])
async def ban(interaction: Interaction, user_id: str, reason: str):
    if interaction.user.id in creatorId:
        finalID = await interaction.client.fetch_user(user_id)
        await interaction.guild.ban(finalID, delete_message_seconds=None, delete_message_days=7,
                                    reason=reason)
        await interaction.response.send_message(f'User {finalID.name} has been banned for {reason}')
    else:
        await interaction.response.send_message("You do not have permission to use this command")


@bot.slash_command(guild_ids=[serverId])
async def unban(interaction: Interaction, user_id: str):
    if interaction.user.id in creatorId:
        finalID = await interaction.client.fetch_user(user_id)
        await interaction.guild.unban(finalID)
        await interaction.response.send_message(f'User {finalID.name} has been un-banned')
    else:
        await interaction.response.send_message("You do not have permission to use this command")



@bot.slash_command(guild_ids=[serverId])
async def kick(interaction: Interaction, user_id: str, reason: str):
    if interaction.user.id in creatorId:
        finalID = await interaction.client.fetch_user(user_id)
        await interaction.guild.kick(finalID, reason=reason)
        await interaction.response.send_message(f'User {finalID.name} has been banned for {reason}')
    else:
        await interaction.response.send_message("You do not have permission to use this command")


@bot.slash_command(guild_ids=[serverId])
async def mute(interaction: Interaction, user_id: str, reason: str, mute_duration: str = "12h"):
    if interaction.user.id in creatorId:
        memberList = interaction.guild.members
        time = humanfriendly.parse_timespan(mute_duration)
        finalID = await interaction.client.fetch_user(user_id)
        for i in memberList:

            if i.id == finalID.id:
                await i.edit(timeout=nextcord.utils.utcnow() + datetime.timedelta(seconds=time))
                await interaction.response.send_message(f'User {i.name} has been muted for {time}')
    else:
        await interaction.response.send_message("You do not have permission to use this command")


@bot.slash_command(guild_ids=[serverId])
async def unmute(interaction: Interaction, user_id: str):
    if interaction.user.id in creatorId:
        memberList = interaction.guild.members
        finalID = await interaction.client.fetch_user(user_id)
        for i in memberList:

            if i.id == finalID.id:
                await i.edit(timeout=nextcord.utils.utcnow() + datetime.timedelta(seconds=1))
                await interaction.response.send_message(f'User {i.name} has been un-muted')
    else:
        await interaction.response.send_message("You do not have permission to use this command")


@bot.slash_command(guild_ids=[serverId])
async def level(interaction: Interaction, user: str = ""):
    global imgList
    finalUser = interaction.user.id
    if user:
        finalUser = user.replace("<", "").replace(">", "").replace("@", "")
    finalUser = db.child("Users").child(finalUser).get().val()

    for key, val in finalUser.items():
        if key == "exp":
            exp = val
        if key == "level":
            level = val
    nextLevel = round((4 * (level ** 3)) / 5)
    imgToUse = math.floor(exp/nextLevel)
    embed = EmbedCreator.createEmbed(color_class[1], "Stats",
                                     f"Current Level: {level}\nCurrent Experience {exp}/{nextLevel}",
                                     imgList[imgToUse], "", "")
    await interaction.response.send_message(embed=embed)


@bot.slash_command(guild_ids=[serverId])
async def mod(interaction: Interaction, user_id: str):
    global creatorId, modRole
    if interaction.user.id in creatorId:
        role = interaction.guild.get_role(modRole)
        user = interaction.guild.get_member(int(user_id))
        await user.add_roles(role)
        db.child("Users").child(user_id).update({"mod": 1})
        await interaction.response.send_message(f"{user.mention} has become a mod successfully")
    else:
        await interaction.response.send_message("You do not have permission to use this command")


@bot.slash_command(guild_ids=[serverId])
async def unmod(interaction: Interaction, user_id: str):
    global creatorId, modRole
    if interaction.user.id in creatorId:
        role = interaction.guild.get_role(modRole)
        user = interaction.guild.get_member(int(user_id))
        await user.remove_roles(role)
        db.child("Users").child(user_id).update({"mod": 0})
        await interaction.response.send_message(f"{user.mention} is no longer a mod")
    else:
        await interaction.response.send_message("You do not have permission to use this command")


@bot.slash_command(guild_ids=[serverId])
async def leaderboard(interaction: Interaction):
    users = db.child("Users").order_by_child("level").limit_to_last(10).get().val()
    stackKey = []
    for key, val in users.items():
        stackKey.append(key)

    bodyStr = ""
    for i in range(len(stackKey)):
        userId = stackKey.pop()
        myVal = db.child("Users").child(userId).get().val()
        v = ""
        for key, val in myVal.items():
            if key == "level":
                v = val
        user = await interaction.client.fetch_user(userId)

        bodyStr += f"{str(i+1)}- {user.name} - Level: {v}\n"

    embed = EmbedCreator.createEmbed(color_class[3], "Leaderboard", bodyStr,"","","")
    await interaction.response.send_message(embed=embed)


@bot.event
async def on_ready():
    print(f'logged in as {bot.user.name} ({bot.user.id})')
    print("....................................")


@tasks.loop(seconds=1.0)
async def twitch_check():
    if await check_twitch() != 0:
        print("pog")
    else:
        print("dog")


@twitch_check.after_loop
async def after_slow_count():
    print('done!')


twitch_check.start()
@bot.event
async def on_message(msg):
    await check_twitch()
    if not msg.author.bot:
        global levelChannel
        user = db.child("Users").child(msg.author.id).get().val()
        for key, val in user.items():
            if key == "exp":
                exp = val
            if key == "level":
                level = val

        exp +=1
        nextLevel = round((4 * (level ** 3)) / 5)
        if exp >= nextLevel:
            exp = 0
            level += 1
            await msg.guild.get_channel(levelChannel).send(f"Congratulations {msg.author.mention} You are now Level {level}")
        db.child("Users").child(msg.author.id).update({"exp": exp, "level": level})


@bot.event
async def on_message_delete(msg):
    if not msg.author.bot:
        global messageLogs
        for i in msg.guild.channels:
            if i.id == int(messageLogs):
                channel = i
        await channel.send(embed=Logs.message_log(0, msg))


@bot.event
async def on_message_edit(before, after):
    if not before.author.bot and before.lower() != after.lower():
        global messageLogs
        for i in before.guild.channels:
            if i.id == int(messageLogs):
                channel = i
        msg = (before, after)
        await channel.send(embed=Logs.message_log(1, msg))


@bot.event
async def on_member_join(member):
    if not member.bot:
        global welcomeChannel, welcomeImage, welcomeMessage
        embed = EmbedCreator.createEmbed(Color.magenta(), f'Welcome to {member.guild.name}', welcomeMessage,
                                         welcomeImage, "", "")
        channel = member.guild.get_channel(welcomeChannel)
        await channel.send(f'{member.mention}', embed=embed)



@bot.event
async def on_member_remove(member):
    if not member.bot:
        global goodbyeChannel, goodbyeImage, goodbyeMessage
        embed = EmbedCreator.createEmbed(Color.magenta(), f'User {member.name.mention} has left', goodbyeMessage,
                                         goodbyeImage, "", "")
        for i in member.guild.channels:

            if i.id == int(goodbyeChannel):
                print("in if")
                channel = i
                await channel.send(f'{member.mention}', embed=embed)


bot.run(config.TOKEN)