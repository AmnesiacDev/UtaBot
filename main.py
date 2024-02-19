import datetime, pyrebase
from datetime import datetime as dt
import humanfriendly
import nextcord, math
from nextcord.ext import commands
import requests
import os as process
import Tickets, EmbedCreator, Logs
from nextcord.ext import tasks
from nextcord import Intents, Color, Interaction, SlashOption, ButtonStyle
from nextcord.ui import View, Button

intents = Intents.all()
intents.message_content = True

color_class = [Color.blue(), Color.red(), Color.green(), Color.magenta(), Color.dark_magenta(), Color.dark_grey(),
               Color.dark_green(), Color.dark_gold(), Color.orange(), Color.purple()]
conf = {
  "apiKey": process.getenv("FIREKEY"),
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
twitchPingImage = "https://media.discordapp.net/attachments/1200255898589872168/1200630104599036035/New_Project_3.png?ex=65c6e0eb&is=65b46beb&hm=dc866c53fbc9a6322847e13036bce238dd18896a4ca69535d4900cb3871e3e43&=&format=webp&quality=lossless"


twitchPingsChannel = 1179968880450478130
twitchPingRole = 1180322120853626921
TWITCH_CHANNEL_NAME = "its_bbananabread"
CLIENT_ID = process.getenv("TWITCH_KEY")
CHANNEL_ID = process.getenv("OAUTH_ID")
stream_id = 0

levelRole = [1200305361303908372, 1200305442740502548, 1200305503507587153, 1200305561313488947,
             1200639506127265804, 1200639591879811212, 1200639626650595438, 1200639671672242196,
             1200639708095586326, 1200639747538833579]


servers = db.child("Guild").get().val()
serverIdList = []
for id in servers:
    serverIdList.append(int(id))

serverId = tuple(serverIdList)

bot = commands.Bot(command_prefix='!', intents=intents, default_guild_ids=serverId)

async def check_twitch():
    url = f"https://api.twitch.tv/helix/streams?user_login={TWITCH_CHANNEL_NAME}"
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {CHANNEL_ID}"  # Replace with your new OAuth token
    }
    global stream_id
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


@bot.slash_command()
async def welcome_channel(interaction: Interaction, welcome_message: str, welcome_channel: str, welcome_image: str):
    if interaction.user.id in creatorId:

        welcomeCh = int(welcome_channel.replace("#", "").replace("<", "").replace(">", ""))
        db.child("Guild").child(interaction.guild.id).update({"welcome_ch": welcomeCh,
                                                              "welcome_mess": welcome_message,
                                                              "welcome_img": welcome_image})
        await interaction.response.send_message("Updated successfully")
    else:
        await interaction.response.send_message("You do not have permission to use this command")






@bot.slash_command()
async def bot_config(interaction: Interaction, message_logs: str = "",
                     punishment_logs: str = "", end_ticket_image: str = "", twitch_ping_image: str = "",
                     mod_role: str = "", level_channel: str = ""):
    global creatorId
    if interaction.user.id in creatorId or interaction.user.id == interaction.guild.owner_id:
        global endTicketImage, twitchPingImage

        if twitch_ping_image:
            twitchPingImage = twitch_ping_image

        if message_logs:
            messageLogs = int(message_logs.replace("#", "").replace("<", "").replace(">", ""))
            db.child("Guild").child(interaction.guild.id).update({"log_mess": messageLogs})

        if punishment_logs:
            punishmentLogs = int(punishment_logs.replace("#", "").replace("<", "").replace(">", ""))
            db.child("Guild").child(interaction.guild.id).update({"log_pun": punishmentLogs})

        if end_ticket_image:
            endTicketImage = end_ticket_image

        if mod_role:
            print(mod_role)
            modRole = int(mod_role.replace("@", "").replace("<", "").replace(">", "").replace("&", ""))
            db.child("Guild").child(interaction.guild.id).update({"mod_role": modRole})

        if level_channel:
            levelChannel = int(level_channel.replace("#", "").replace("<", "").replace(">", ""))
            db.child("Guild").child(interaction.guild.id).update({"level_channel": levelChannel})
        await interaction.response.send_message("Config has been set successfully")
    else:
        await interaction.response.send_message("You do not have permission to use this command")


@bot.slash_command()
async def create_ticket(interaction: Interaction,
                        color: int = SlashOption(name="color", choices={"Blue": 0, "Red": 1, "Green": 2, "Pink": 3,
                                                                        "Magenta": 4, "Gray": 5, "Dark green": 6,
                                                                        "Gold": 7, "Orange": 8, "Purple": 9}),
                        title: str = "", body: str = "", image: str = "",
                        thumbnail: str = "", footer: str = ""):
    global roleName
    global creatorId
    if interaction.user.id in creatorId:
        colorFinal = color_class[color]

        body = body.replace("%n", f'\n')
        ticket = Tickets.CreateTicketMenu()
        ticket.createEmbed(colorFinal, title, body, image, thumbnail, footer)

        await ticket.start(interaction=interaction)

    else:
        await interaction.response.send_message("No permission")


@bot.slash_command()
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




@bot.slash_command()
async def ban(interaction: Interaction, user_id: str, reason: str):

    caller = db.child("Users").child(interaction.user.id).get().val()
    for key, val in caller.items():
        if key == "mod":
            isMod = val

    if interaction.user.id in creatorId or isMod:
        finalID = await interaction.client.fetch_user(user_id)

        server = db.child("Guild").child(interaction.guild.id).get().val()
        for key, val in server.items():
            if key == "log_pun":
                punishmentLogs = val
        channel = interaction.guild.get_channel(int(punishmentLogs))
        await interaction.guild.ban(finalID, delete_message_seconds=None, delete_message_days=7,
                                    reason=reason)
        await interaction.response.send_message(f'User {finalID.name} has been banned for {reason}')
        embed = Logs.punishment_log(2, finalID, reason, "")
        await channel.send(embed = embed)


    else:
        await interaction.response.send_message("You do not have permission to use this command")


@bot.slash_command()
async def unban(interaction: Interaction, user_id: str, reason: str = ""):
    caller = db.child("Users").child(interaction.user.id).get().val()
    for key, val in caller.items():
        if key == "mod":
            isMod = val
    if interaction.user.id in creatorId or isMod:
        finalID = await interaction.client.fetch_user(user_id)
        server = db.child("Guild").child(interaction.guild.id).get().val()

        for key, val in server.items():
            if key == "log_pun":
                punishmentLogs = val
        channel = interaction.guild.get_channel(int(punishmentLogs))

        await interaction.guild.unban(finalID)
        await interaction.response.send_message(f'User {finalID.name} has been un-banned')
        embed = Logs.punishment_log(3, finalID, reason, "")
        await channel.send(embed=embed)
    else:
        await interaction.response.send_message("You do not have permission to use this command")


@bot.slash_command()
async def kick(interaction: Interaction, user_id: str, reason: str):
    caller = db.child("Users").child(interaction.user.id).get().val()
    for key, val in caller.items():
        if key == "mod":
            isMod = val

    if interaction.user.id in creatorId or isMod:
        finalID = await interaction.client.fetch_user(user_id)

        server = db.child("Guild").child(interaction.guild.id).get().val()

        for key, val in server.items():
            if key == "log_pun":
                punishmentLogs = val
        channel = interaction.guild.get_channel(int(punishmentLogs))

        await interaction.guild.kick(finalID, reason=reason)
        await interaction.response.send_message(f'User {finalID.name} has been kicked for {reason}')

        embed = Logs.punishment_log(1, finalID, reason, "")
        await channel.send(embed=embed)
    else:
        await interaction.response.send_message("You do not have permission to use this command")


@bot.slash_command()
async def mute(interaction: Interaction, user_id: str, reason: str, mute_duration: str = "12h"):
    caller = db.child("Users").child(interaction.user.id).get().val()
    for key, val in caller.items():
        if key == "mod":
            isMod = val
    if interaction.user.id in creatorId or isMod:
        memberList = interaction.guild.members
        time = humanfriendly.parse_timespan(mute_duration)
        finalID = await interaction.client.fetch_user(user_id)

        server = db.child("Guild").child(interaction.guild.id).get().val()

        for key, val in server.items():
            if key == "log_pun":
                punishmentLogs = val
        channel = interaction.guild.get_channel(int(punishmentLogs))

        for i in memberList:

            if i.id == finalID.id:
                await i.edit(timeout=nextcord.utils.utcnow() + datetime.timedelta(seconds=time))
                await interaction.response.send_message(f'User {i.name} has been muted for {reason}. Duration {time}')

                embed = Logs.punishment_log(0, finalID, reason, time)
                await channel.send(embed=embed)
    else:
        await interaction.response.send_message("You do not have permission to use this command")


@bot.slash_command()
async def unmute(interaction: Interaction, user_id: str, reason: str = ""):
    caller = db.child("Users").child(interaction.user.id).get().val()
    for key, val in caller.items():
        if key == "mod":
            isMod = val
    if interaction.user.id in creatorId or isMod:
        memberList = interaction.guild.members
        finalID = await interaction.client.fetch_user(user_id)

        server = db.child("Guild").child(interaction.guild.id).get().val()

        for key, val in server.items():
            if key == "log_pun":
                punishmentLogs = val
        channel = interaction.guild.get_channel(int(punishmentLogs))
        
        for i in memberList:

            if i.id == finalID.id:
                await i.edit(timeout=nextcord.utils.utcnow() + datetime.timedelta(seconds=1))
                await interaction.response.send_message(f'User {i.name} has been un-muted')

                embed = Logs.punishment_log(4, finalID, reason, "")
                await channel.send(embed=embed)
    else:
        await interaction.response.send_message("You do not have permission to use this command")


@bot.slash_command()
async def level(interaction: Interaction, type: int = SlashOption(name="type", choices={"Text": 0, "Audio": 1}), user: str = ""):
    global imgList
    finalUser = interaction.user.id
    if user:
        finalUser = user.replace("<", "").replace(">", "").replace("@", "")
    finalUser = db.child("Users").child(finalUser).get().val()
    if type == 0:
        emoji = "📔"
        for key, val in finalUser.items():
            if key == "exp":
                exp = val
            if key == "level":
                level = val
        nextLevel = round((4 * (level ** 3)) / 5)
        imgToUse = math.floor((exp / nextLevel) * 100)
        imgToUse = int(math.floor(imgToUse / 15))
        embed = EmbedCreator.createEmbed(color_class[1], f"Stats   -   {emoji}",
                                         f"Current Level: {level}\nCurrent Experience {exp}/{nextLevel}",
                                         imgList[imgToUse], "", "")
    else:
        emoji = "🔊"
        for key, val in finalUser.items():
            if key == "vexp":
                vexp = val
            if key == "vlevel":
                vlevel = val
        nextLevel = round((4 * (vlevel ** 3)) / 5)
        imgToUse = math.floor((vexp / nextLevel)*100)
        imgToUse = int(math.floor(imgToUse/15))
        embed = EmbedCreator.createEmbed(color_class[1], f"Stats   -   {emoji}",
                                         f"Current Level: {vlevel}\nCurrent Experience {vexp}/{nextLevel}",
                                         imgList[imgToUse], "", "")

    await interaction.response.send_message(embed=embed)


@bot.slash_command()
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


@bot.slash_command()
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



@bot.slash_command()
async def leaderboard(interaction: Interaction, type: int = SlashOption(name="type", choices={"Text": 0, "Audio": 1})):

    if type == 0:
        users = db.child("Users").order_by_child("level").limit_to_last(10).get().val()
        levelType = "level"
        emoji = "📔"
    else:
        users = db.child("Users").order_by_child("vlevel").limit_to_last(10).get().val()
        levelType = "vlevel"
        emoji = "🔊"
    stackKey = []
    for key, val in users.items():
        stackKey.append(key)

    bodyStr = ""
    for i in range(len(stackKey)):
        userId = stackKey.pop()
        myVal = db.child("Users").child(userId).get().val()
        v = ""
        for key, val in myVal.items():
            if key == levelType:
                v = val
        user = await interaction.client.fetch_user(userId)

        bodyStr += f"{str(i + 1)}- {user.name} - Level: {v}\n"

    embed = EmbedCreator.createEmbed(color_class[3], f"Leaderboard   -   {emoji}", bodyStr, "", "", "")
    await interaction.response.send_message(embed=embed)


@bot.event
async def on_ready():
    print(f'logged in as {bot.user.name} ({bot.user.id})')
    print("....................................")


@tasks.loop(minutes=5.0)
async def twitch_check():
    data = await check_twitch()
    try:
        id = data["data"][0]["id"]
    except:
        print("Stream is offline")
    global stream_id, twitchPingsChannel, TWITCH_CHANNEL_NAME, twitchPingImage

    if data != 0 and int(id) != stream_id:
        stream_id = int(id)
        guild = await bot.fetch_guild(serverId)
        channel = await guild.fetch_channel(twitchPingsChannel)

        linkButton = Button(label="Come watch my stream", url="https://www.twitch.tv/its_bbananabread", style=ButtonStyle.blurple)
        async def linkButton_callback(interaction):
            await interaction.response.send_message("works")

        linkButton.callback = linkButton_callback
        myView = View()
        myView.add_item(linkButton)
        embed = EmbedCreator.createEmbed(color_class[3], f"[LIVE]{data['data'][0]['user_name']}",
                                         f"{data['data'][0]['title']}", twitchPingImage,"",f"{data['data'][0]['game_name']}")
        await channel.send(embed=embed, view=myView, content=f"Hey guys, I'm live please check out my stream :) {guild.get_role(1180322120853626921).mention}")
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
        global levelRole

        server = db.child("Guild").child(msg.guild.id).get().val()
        for key, val in server.items():
            if key == "level_channel":
                levelChannel = int(val)

        user = db.child("Users").child(msg.author.id).get().val()
        for key, val in user.items():
            if key == "exp":
                exp = val
            if key == "level":
                level = val

        exp += 1
        #Booster exp boost
        memberRoles = msg.author.roles
        for memRole in memberRoles:
            if memRole.is_premium_subscriber():
                exp += 1

        nextLevel = round((4 * (level ** 3)) / 5)
        if exp >= nextLevel:
            exp = 0
            level += 1
            #embed = EmbedCreator.createEmbed(color_class[3], )
            await msg.guild.get_channel(levelChannel).send(
                f"Congratulations {msg.author.mention} You are now Level {level}")
        if level == 5:
            role = msg.guild.get_role(levelRole[0])
            if msg.author.get_role(levelRole[0]) is None:
                await msg.author.add_roles(role)
        elif level == 10:
            role = msg.guild.get_role(levelRole[1])
            if msg.author.get_role(levelRole[1]) is None:
                await msg.author.add_roles(role)
        elif level == 15:
            role = msg.guild.get_role(levelRole[2])
            if msg.author.get_role(levelRole[2]) is None:
                await msg.author.add_roles(role)
        elif level == 20:
            role = msg.guild.get_role(levelRole[3])
            if msg.author.get_role(levelRole[3]) is None:
                await msg.author.add_roles(role)
        elif level == 25:
            role = msg.guild.get_role(levelRole[4])
            if msg.author.get_role(levelRole[4]) is None:
                await msg.author.add_roles(role)
        elif level == 30:
            role = msg.guild.get_role(levelRole[5])
            if msg.author.get_role(levelRole[5]) is None:
                await msg.author.add_roles(role)
        elif level == 40:
            role = msg.guild.get_role(levelRole[6])
            if msg.author.get_role(levelRole[6]) is None:
                await msg.author.add_roles(role)
        elif level == 50:
            role = msg.guild.get_role(levelRole[7])
            if msg.author.get_role(levelRole[7]) is None:
                await msg.author.add_roles(role)
        elif level == 75:
            role = msg.guild.get_role(levelRole[8])
            if msg.author.get_role(levelRole[8]) is None:
                await msg.author.add_roles(role)
        elif level == 100:
            role = msg.guild.get_role(levelRole[9])
            if msg.author.get_role(levelRole[9]) is None:
                await msg.author.add_roles(role)
        db.child("Users").child(msg.author.id).update({"exp": exp, "level": level})

@bot.event
async def on_message_delete(msg):
    if not msg.author.bot:
        server = db.child("Guild").child(msg.guild.id).get().val()
        for key, val in server.items():
            if key == "log_mess":
                messageLogs = val

        channel = msg.guild.get_channel(messageLogs)
        await channel.send(embed=Logs.message_log(0, msg))


@bot.event
async def on_message_edit(before, after):
    if not before.author.bot and before.content.lower() != after.content.lower():

        server = db.child("Guild").child(before.guild.id).get().val()
        for key, val in server.items():
            if key == "log_mess":
                messageLogs = val

        channel = before.guild.get_channel(messageLogs)
        msg = (before, after)
        await channel.send(embed=Logs.message_log(1, msg))
      
@bot.event
async def on_member_join(member):
    if not member.bot:
        server = db.child("Guild").child(member.guild.id).get().val()
        for key, val in server.items():
            if key == "welcome_ch":
                welcomeChannel = val
            elif key == "welcome_mess":
                welcomeMessage = val
            elif key == "welcome_img":
                welcomeImage = val
        embed = EmbedCreator.createEmbed(Color.magenta(), f'Welcome to {member.guild.name}', welcomeMessage,
                                         welcomeImage, "", "")

        channel = member.guild.get_channel(welcomeChannel)
        users = db.child("Users").get().val()
        new = 1
        for id in users.items():
            if int(id[0]) == int(member.id):
                new = 0

        if new:
            db.child("Users").child(member.id).update(
                {"exp": 0, "level": 1, "mod": 0, "vexp": 0, "vlevel": 1, "vTime": "now"})
        await channel.send(f'{member.mention}', embed=embed)


@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None:
        print(f"user {member} joined {after.channel}")
        now = dt.now()
        db.child("Users").child(member.id).update({"vTime": str(now)})

    elif after.channel is None:
        current_time = dt.now()
        user = db.child("Users").child(member.id).get().val()
        for key, val in user.items():
            if key == "vTime":
                joinTime = dt.strptime(val, '%Y-%m-%d %H:%M:%S.%f')
            if key == "vexp":
                vexp = val
            if key == "vlevel":
                vlevel = val

        time_diff = current_time - joinTime
        exp = int(math.ceil(int(time_diff.total_seconds()) / 2.5))

        #Server booster exp boost
        memberRoles = member.roles
        for memRole in memberRoles:
            if memRole.is_premium_subscriber():
                exp = int(exp*2)

        nextLevel = round((4 * (vlevel ** 3)) / 5)
        if vexp + exp < nextLevel:
            vexp += exp
        while vexp + exp >= nextLevel:
            difference = abs(nextLevel - vexp)
            print(difference)
            exp -= difference
            vexp = exp
            vlevel += 1

            server = db.child("Guild").child(member.guild.id).get().val()
            for key, val in server.items():
                if key == "level_channel":
                    levelChannel = val
            channel = member.guild.get_channel(levelChannel)
            nextLevel = round((4 * (vlevel ** 3)) / 5)


        await channel.send(f"Congratulations {member.mention} your voice Level is now {vlevel}")
        db.child("Users").child(member.id).update({"vexp": vexp, "vlevel": vlevel, "vTime": "now"})
        print(f"user {member} left {before.channel}")

bot.run(process.getenv("TOKEN"))
