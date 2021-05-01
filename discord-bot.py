import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import configparser
import psycopg2

# import config variables

config = configparser.ConfigParser()
config.read('config.ini')

prefix = config['DISCORD']['prefix']
bot = commands.Bot(command_prefix=prefix)
TOKEN = config['DISCORD']['token']
server = config['DISCORD']['server_name']

#PostgreSQL config
phost = config['postgresql']['host']
pdatabase = config['postgresql']['database']
puser = config['postgresql']['user']
ppassword = config['postgresql']['password']

#Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        host=phost,
        database=pdatabase,
        user=puser,
        password=ppassword)
except:
    print('Error while connecting to PostgreSQL')
finally:
    if conn is not None:
        print('Connected to PostgreSQL')
        tname = config['postgresql']['table']
        tschema = config['postgresql']['schema']
        cur = conn.cursor()
        cur.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '" + tschema + "' AND TABLE_NAME = '" + tname + "';")
        x = cur.fetchone()
        if x is None:
            cur.execute("CREATE TABLE " + tname + " ( UserID bigint, Nick varchar(255), Messages int, Points int, Reputation int );")
        else:
            print('table exists!')
        conn.commit()
        cur.close()

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# Function to convert list to string
def list_to_string(s):
    str1 = ""

    for ele in s:
        str1 += " " + ele

    return str1

#User send message
@bot.event
async def on_message(message):
    if message.author.bot is False:
        author = str(message.author.id)
        author_nick = str(message.author)
        if conn is not None:
            cur = conn.cursor()
            cur.execute("SELECT * FROM " + tname + " WHERE UserID = '" + author + "';")
            x = cur.fetchone()
            if x is None:
                cur.execute("INSERT INTO " + tname + " (UserID, Nick, Messages, Points, Reputation) VALUES ('" + author + "', '" + author_nick + "', '1', '1', '0');")
            else:
                cur.execute("UPDATE " + tname + " SET Messages = Messages + 1, Points = Points + 1 WHERE UserID = '" + author + "';")

            conn.commit()
            cur.close()

    await bot.process_commands(message)

@bot.command(name="top", pass_context=True)
async def _top(ctx, type):
    if conn is not None:
        if type == 'aktywnosc':
            embed_var = discord.Embed(title="Top Aktywnych", description="", color=0xffff00)
            for x in range(10):
                cur = conn.cursor()
                cur.execute("SELECT Nick, Messages FROM " + tname + " ORDER BY greatest(Messages) DESC Limit 1 Offset " + str(x) + ";")
                y = cur.fetchone()
                text = str(y)
                text = text.replace("('","")
                text = text.replace(")", "")
                text = text.replace("',", " | ")
                text = text + " wiadomości"
                if y is None:
                    break
                x2 = x + 1
                embed_var.add_field(name=f"#{x2}", value=text, inline=False)
                cur.close()
            await ctx.channel.send(embed=embed_var)


@bot.command(name="kick", pass_context=True)
@has_permissions(manage_roles=True, ban_members=True)
async def _kick(ctx, member: discord.Member, *text):
    reason = list_to_string(text)

    embed_var = discord.Embed(title=f"{member.display_name} Zostal wyrzucony", description=f"{reason}", color=0xffff00)
    embed_var_for_member = discord.Embed(title=f"Zostales wyrzucony z {server}", description=f"{reason}",
                                         color=0xffff00)

    await ctx.message.delete()

    # try send message to member
    try:
        await member.send(embed=embed_var_for_member)
    except:
        print(f'nie udalo sie wyslac wiadomosci do {member}')

    await ctx.channel.send(embed=embed_var)
    await member.kick(reason=reason)


@bot.command(name="ban", pass_context=True)
@has_permissions(manage_roles=True, ban_members=True)
async def _ban(ctx, member: discord.Member, *text):
    reason = list_to_string(text)

    embed_var = discord.Embed(title=f"{member.display_name} Zostal zbanowany", description=f"{reason}", color=0xff0000)
    embed_var_for_member = discord.Embed(title=f"Zostales zbanowany na {server}", description=f"{reason}",
                                         color=0xff0000)

    await ctx.message.delete()

    # try send message to member
    try:
        await member.send(embed=embed_var_for_member)
    except:
        print(f'nie udalo sie wyslac wiadomosci do {member}')

    await ctx.channel.send(embed=embed_var)
    await member.ban(reason=reason)


@bot.command(name="say", pass_context=True)
@has_permissions(manage_roles=True, ban_members=True)
async def _say(ctx, *text):
    args = list_to_string(text)

    embed_var = discord.Embed(description=f"{args}", color=0x000000)

    await ctx.message.delete()
    await ctx.channel.send(embed=embed_var)


@bot.command(name="clear", pass_context=True)
@has_permissions(manage_roles=True, ban_members=True)
async def _clear(ctx, number = 5):

    await ctx.message.delete()

    await ctx.channel.purge(limit=number)

bot.run(TOKEN)
