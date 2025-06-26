from dotenv import load_dotenv
import os
import discord
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime

from dotenv import load_dotenv
import os
import discord
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime

# Φόρτωση μεταβλητών περιβάλλοντος
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# Ονόματα ρόλων κατά έτος
YEARS = {
    "0": "Θα γίνω πρωτοετής",
    "1": "1ο έτος",
    "2": "2ο έτος",
    "3": "3ο έτος",
    "4": "4ο έτος",
    "5": "5ο έτος",
    "6": "6ο έτος",
}

PIN_CHANNEL_NAME = "🎓-επιλογή-έτους"

# Το καρφιτσωμένο μήνυμα με τις οδηγίες
PINNED_MESSAGE = (
    "**Οδηγίες για επιλογή έτους φοιτητή**\n\n"
    "	Επιλέγετε το ακαδημαϊκό έτος που είχατε μέχρι και την εξεταστική του Ιουνίου 2025.\n"
    "		Για παράδειγμα, όσοι ολοκληρώνουν τώρα το 3ο έτος, επιλέγουν το 3.\n"
    "		Αν είστε νέος φοιτητής που δεν έχετε ξεκινήσει ακόμα, επιλέγετε το 0 που σημαίνει **\"Θα γίνω πρωτοετής\"**.\n"
    "		Την 1η Οκτωβρίου, το bot θα προάγει αυτόματα όσους έχουν τον ρόλο \"Θα γίνω πρωτοετής\" στο 1ο έτος και τους υπόλοιπους στα επόμενα έτη αντίστοιχα.\n"
    "	Η επιλογή γίνεται μόνο μία φορά. Μετά μόνο οι admins μπορούν να αλλάξουν το έτος.\n"
    "Καλή συνέχεια! 🎓"
)

@bot.event
async def on_ready():
    print(f"Bot συνδέθηκε ως {bot.user}")
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    promote_years.start()
    await send_or_pin_instructions()

async def send_or_pin_instructions():
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("Δεν βρέθηκε το guild!")
        return
    channel = discord.utils.get(guild.text_channels, name=PIN_CHANNEL_NAME)
    if not channel:
        print(f"Δεν βρέθηκε το κανάλι '{PIN_CHANNEL_NAME}'")
        return

    # Έλεγχος αν υπάρχει ήδη καρφιτσωμένο μήνυμα με το κείμενο μας
    pinned_messages = await channel.pins()
    for msg in pinned_messages:
        if msg.content == PINNED_MESSAGE:
            print("Το μήνυμα οδηγιών είναι ήδη καρφιτσωμένο.")
            return

    # Στέλνουμε το μήνυμα και το καρφιτσώνουμε
    message = await channel.send(PINNED_MESSAGE)
    await message.pin()
    print(f"Το μήνυμα οδηγιών στάλθηκε και καρφιτσωθηκε στο κανάλι '{PIN_CHANNEL_NAME}'.")

# Slash command: /set_year
@tree.command(name="set_year", description="Διάλεξε το έτος σου (μία φορά)", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(year="Το έτος στο οποίο ήσουν το ακαδημαϊκό έτος μέχρι Ιούνιο 2025")
async def set_year(interaction: discord.Interaction, year: str):
    member = interaction.user
    guild = interaction.guild

    # Έλεγχος αν έχει ήδη ρόλο έτους
    if any(role.name in YEARS.values() for role in member.roles):
        await interaction.response.send_message("Έχεις ήδη διαλέξει έτος. Μόνο admin μπορεί να το αλλάξει.", ephemeral=True)
        return

    if year not in YEARS:
        await interaction.response.send_message("Μη έγκυρη επιλογή.", ephemeral=True)
        return

    role_name = YEARS[year]
    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
        role = await guild.create_role(name=role_name)

    await member.add_roles(role)
    await interaction.response.send_message(f"Επιλέχθηκε το **{role_name}**.", ephemeral=True)

# Admin command: /admin_change_year
@tree.command(name="admin_change_year", description="Admin: Αλλαγή έτους χρήστη", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(user="Ο χρήστης", year="Νέο έτος")
async def admin_change_year(interaction: discord.Interaction, user: discord.Member, year: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Μόνο διαχειριστές μπορούν να το κάνουν αυτό.", ephemeral=True)
        return

    if year not in YEARS:
        await interaction.response.send_message("Μη έγκυρη επιλογή.", ephemeral=True)
        return

    # Αφαίρεση παλιών ρόλων
    await user.remove_roles(*[r for r in user.roles if r.name in YEARS.values()])
    new_role = discord.utils.get(user.guild.roles, name=YEARS[year])
    if not new_role:
        new_role = await user.guild.create_role(name=YEARS[year])
    await user.add_roles(new_role)

    await interaction.response.send_message(f"Ο χρήστης {user.mention} τώρα έχει τον ρόλο **{YEARS[year]}**.")

# Αυτόματη προαγωγή κάθε 1 Οκτωβρίου
@tasks.loop(hours=24)
async def promote_years():
    now = datetime.utcnow()
    if now.month == 10 and now.day == 1:
        guild = bot.get_guild(GUILD_ID)
        if not guild:
            print("Δεν βρέθηκε το guild για προαγωγή.")
            return
        for member in guild.members:
            for i in range(1, 6):
                role = discord.utils.get(guild.roles, name=f"{i}ο έτος")
                next_role = discord.utils.get(guild.roles, name=f"{i+1}ο έτος")
                if role in member.roles:
                    await member.remove_roles(role)
                    if not next_role:
                        next_role = await guild.create_role(name=f"{i+1}ο έτος")
                    await member.add_roles(next_role)
            # Προαγωγή από "Θα γίνω πρωτοετής" στο 1ο έτος
            future_role = discord.utils.get(guild.roles, name=YEARS["0"])
            role_1 = discord.utils.get(guild.roles, name=YEARS["1"])
            if future_role in member.roles:
                await member.remove_roles(future_role)
                if not role_1:
                    role_1 = await guild.create_role(name=YEARS["1"])
                await member.add_roles(role_1)

bot.run(TOKEN)