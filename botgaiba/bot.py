import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configuration des intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True # Indispensable pour détecter les nouveaux membres

# Initialisation du bot
bot = commands.Bot(command_prefix='+', intents=intents)

# Salon de bienvenue (Remplacez l'ID par celui de votre salon)
WELCOME_CHANNEL_ID = 123456789012345678 

class LinkView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="Site ↗️", url="https://votre-site.com", style=discord.ButtonStyle.link))
        self.add_item(discord.ui.Button(label="Vidéo ↗️", url="https://youtube.com", style=discord.ButtonStyle.link))
        self.add_item(discord.ui.Button(label="Connect ↗️", url="https://votre-serveur.com", style=discord.ButtonStyle.link))
        self.add_item(discord.ui.Button(label="Documentation ↗️", url="https://docs.votre-site.com", style=discord.ButtonStyle.link))

class RulesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Accepter le règlement", style=discord.ButtonStyle.success, emoji="✅")
    async def accept_rules(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "Merci d'avoir accepté le règlement !",
            ephemeral=True
        )

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')
    print('------')

@bot.event
async def on_member_join(member):
    # On récupère le salon de bienvenue
    # Si l'ID est incorrect, on cherche le premier salon textuel disponible
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if not channel:
        for ch in member.guild.text_channels:
            if "bienvenue" in ch.name.lower() or "welcome" in ch.name.lower():
                channel = ch
                break
    
    if channel:
        # Création du mini embed de bienvenue
        member_count = member.guild.member_count
        
        e = discord.Embed(
            title="👋 BIENVENUE !",
            description=f"Salut {member.mention} ! Bienvenue sur **{member.guild.name}**.\n\n"
                        f"Nous sommes maintenant **{member_count}** membres !",
            color=0x57F287 # Vert Discord
        )
        
        # On peut aussi ajouter l'avatar du membre en miniature
        e.set_thumbnail(url=member.display_avatar.url)
        
        await channel.send(content=f" {member.mention} !", embed=e)

@bot.command()
async def embed(ctx, sub_cmd: str = None):
    try:
        await ctx.message.delete()
    except:
        pass

    color = 0x57F287 # Vert Discord

    if sub_cmd == "reg":
        # RÈGLEMENT - UN SEUL EMBED - FORMATAGE PRO
        rules_text = (
            "__***Règlement officiel du serveur***__\n\n"
            "> ## **I. 📜 DISPOSITIONS GÉNÉRALES**\n"
            "*Bienvenue sur notre plateforme.* En rejoignant cette communauté, vous vous engagez à respecter les règles énoncées ci-dessous. Le non-respect de ces dispositions pourra entraîner des sanctions allant de l'avertissement au bannissement définitif.\n\n"
            "> ## **II. 💡 PROPRIÉTÉ INTELLECTUELLE**\n"
            "• __**Pas de leak**__ : Toute forme de partage, de distribution ou de revente de contenus privés, payants ou appartenant à des tiers (`leaks`) est strictement prohibée. *Nous prônons le respect du travail des créateurs.*\n\n"
            "> ## **III. 🤝 COMPORTEMENT & ÉTHIQUE**\n"
            "• __**Respect mutuel**__ : La courtoisie est de mise. Les insultes, le harcèlement, la toxicité ou toute forme de discrimination ne seront pas tolérés. *Tout le monde est ici pour passer un bon moment.*\n\n"
            "> ## **IV. 🛡️ SÉCURITÉ & MODÉRATION**\n"
            "• __**Utilisation du MENTEUR**__ : Il est formellement interdit d'utiliser l'outil `MENTEUR` à l'encontre de l'administration. Toute tentative d'abus se soldera par un __**bannissement immédiat et définitif**__. 😂\n\n"
            "> ## **V. ✅ ACCEPTATION**\n"
            "En cliquant sur le bouton ci-dessous, vous confirmez avoir pris connaissance du règlement et vous engagez à le respecter dans son intégralité.\n\n"
            "---"
        )
        
        e = discord.Embed(
            title="📜 RÈGLEMENT DU SERVEUR",
            description=rules_text,
            color=color
        )
        e.set_footer(text="Lisez attentivement avant d'accepter • " + discord.utils.utcnow().strftime("%d/%m/%Y"))
        
        await ctx.send(embed=e, view=RulesView())
        return

    else:
        # PRÉSENTATION - UN SEUL EMBED - FORMATAGE PRO
        presentation_text = (
            "__***Informations et Accès Prime***__\n\n"
            "> ## **🌀 BIENVENUE CHEZ LOOP**\n"
            "*Voici nos liens afin de tout __découvrir__ sur la base __Prime__.*\n\n"
            "> ## **🌐 SITE WEB**\n"
            "**Découvrez** notre site web __complet__ avec guide d'installation, documentation, `patch notes` & autres!\n\n"
            "> ## **🎬 PRÉSENTATION**\n"
            "Voici la vidéo de __présentation__ de la base __Prime__.\n\n"
            "> ## **🎮 SERVEUR TEST**\n"
            "Avoir un __aperçu__ in-game de la base via notre serveur de test.\n\n"
            "> ## **📚 DOCUMENTATION**\n"
            "L'__immense__ documentation pour tout connaître de __Prime__ sur le bout des doigts.\n\n"
            "---"
        )

        e = discord.Embed(
            title="LOOP - PRIME",
            description=presentation_text,
            color=color
        )
        e.set_footer(text="Système automatisé LOOP • 2026")
        
        await ctx.send(embed=e, view=LinkView())

if __name__ == "__main__":
    bot.run(TOKEN)