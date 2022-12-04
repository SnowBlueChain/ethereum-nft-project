import os
import json
import discord
import datetime
import requests
from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import Button, View
from discord.commands import Option
from discord.commands import slash_command


class collection(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def collection_name_autocomplete(self: discord.AutocompleteContext):
        with open('collection_name_autocomplete.json','r') as of:
            collection_name_data = json.load(of)
        return collection_name_data.keys()

    @slash_command(name='collection', description='Check collection information from Opensea, LooksRare and X2Y2')
    async def collection(
        self,
        ctx: discord.ApplicationContext,
        collection: Option(str, 'Specify the collection slug', autocomplete=collection_name_autocomplete)
    ):
        #----------------------------------------------------------------------------------------------------------------------------------------------------------------
        with open('collection_name_autocomplete.json','r') as of:
            collection_name_data = json.load(of)
        if collection in collection_name_data:
            collection = collection_name_data[collection]
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        opensea_button = Button(label='OpenSea', style=discord.ButtonStyle.primary, emoji='<:opensea:1048240029371224104>')
        looksrare_button = Button(label='LooksRare', style=discord.ButtonStyle.success, emoji='<:looksgreen:1048239565233729546>')
        x2y2_button = Button(label='X2Y2', style=discord.ButtonStyle.secondary, emoji='<:x2y2:1048239487148359731>')
        return_button = Button(label='EXIT', style=discord.ButtonStyle.danger)
        git_book = Button(label='GitBook', style=discord.ButtonStyle.link, emoji='<:gitbook:1047912317427400704>')
        git_book.url = "https://kizmeow.gitbook.io/kizmeow-nft-discord-bot/information/faq"
        git_book.custom_id = None
        invite = Button(label='Kizmeow Support Server', style=discord.ButtonStyle.link, emoji='<:kizmeow:1047912736224448562>')
        invite.url = 'https://discord.gg/PxNF9PaSKv'
        invite.custom_id = None
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        load_dotenv()
        url = f'https://api.modulenft.xyz/api/v2/eth/nft/collection?slug={collection}'
        headers = {
            'accept': 'application/json',
            'X-API-KEY': os.getenv('MODULE_API_KEY')
        }
        r = requests.get(url, headers=headers).json()
        if r['error'] != None:
            view = View(timeout=None)
            view.add_item(git_book)
            view.add_item(invite)
            embed = discord.Embed(title='[ERROR]',
                                  description=f'`{r["error"]["message"]}`\n\nOther possible reasons:\nhttps://kizmeow.gitbook.io/kizmeow-nft-discord-bot/information/faq\nJoin support server to report the problem.\nhttps://discord.gg/PxNF9PaSKv',
                                  color=0xFFA46E)
            await ctx.respond(embed=embed, view=view, ephemeral=True)
            return

        collection_name = 'no data' if r['data']['name'] == None else r['data']['name']
        collection_slug = 'no data' if r['data']['slug'] == None else r['data']['slug']
        description = 'no data' if r['data']['description'] == None else r['data']['description']
        external_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' if r['data']['socials']['external_url'] == None else r['data']['socials']['external_url']
        discord_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' if r['data']['socials']['discord_url'] == None else r['data']['socials']['discord_url']
        twitter_username = 'no data' if r['data']['socials']['twitter_username'] == None else r['data']['socials']['twitter_username']
        image_url = 'https://imgur.com/aSSH1jL' if r['data']['images']['image_url'] == None else r['data']['images']['image_url']
        banner_image_url = 'https://tenor.com/view/glitch-discord-gif-gif-20819419' if r['data']['images']['banner_image_url'] == None else r['data']['images']['banner_image_url']
        collection_create_date = '757371600' if r['data']['createdDate'] == None else r['data']['createdDate']
        collection_create_date = datetime.datetime.fromisoformat(collection_create_date)
        collection_create_date = str(int(collection_create_date.timestamp()))

        async def initial_embed():
            view = View(timeout=None)
            view.add_item(opensea_button)
            view.add_item(looksrare_button)
            view.add_item(x2y2_button)

            embed = discord.Embed(title='', color=0xFFA46E)
            embed.set_image(url=banner_image_url)
            embed.add_field(name='Description', value=f'{description}...', inline=False)
            embed.add_field(name='Created', value=f'<t:{collection_create_date}:R>', inline=False)
            embed.add_field(name='_ _', value=f'[Website]({external_url})║[Discord]({discord_url})║[Twitter](https://twitter.com/{twitter_username})', inline=False)
            embed.set_author(name=f'{collection_name}', url=f'https://opensea.io/collection/{collection_slug}', icon_url=image_url)
            embed.set_footer(text='Data provided by Kizmeow NFT Bot', icon_url='https://user-images.githubusercontent.com/80938768/204983971-d7cf0e40-f4ce-4737-ba07-85ed62112dab.png')
            embed.timestamp = datetime.datetime.now()

            return (embed, view)

        (embed, view) = await initial_embed()
        await ctx.defer()
        await ctx.respond(embed=embed, view=view)

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        async def marketplace_embed(marketplace_name):
            load_dotenv()
            url = f'https://api.modulenft.xyz/api/v2/eth/nft/stats?slug={collection}&marketplace={marketplace_name}'
            headers = {
                'accept': 'application/json',
                'X-API-KEY': os.getenv('MODULE_API_KEY')
            }

            r = requests.get(url, headers=headers).json()
            if r['error'] != None:
                view = View(timeout=None)
                view.add_item(git_book)
                view.add_item(invite)
                embed = discord.Embed(title='[ERROR]',
                                      description=f'`{r["error"]["message"]}`\n\nOther possible reasons:\nhttps://kizmeow.gitbook.io/kizmeow-nft-discord-bot/information/faq\nJoin support server to report the problem.\nhttps://discord.gg/PxNF9PaSKv',
                                      color=0xFFA46E)
                await ctx.respond(embed=embed, view=view, ephemeral=True)
                return
            match marketplace_name:
                case 'Opensea':  # why tf requests result are all different? I'm very confused too.
                    daily_volume = 0 if r['data']['dailyVolume'] == None else float(r['data']['dailyVolume'])
                    weekly_volume = 0 if r['data']['WeeklyVolume'] == None else float(r['data']['WeeklyVolume'])
                    monthly_volume = 0 if r['data']['monthlyVolume'] == None else float(r['data']['monthlyVolume'])
                case 'Looksrare':
                    daily_volume = 0 if r['data']['DailyVolume'] == None else float(r['data']['DailyVolume'])
                    weekly_volume = 0 if r['data']['WeeklyVolume'] == None else float(r['data']['WeeklyVolume'])
                    monthly_volume = 0 if r['data']['MonthlyVolume'] == None else float(r['data']['MonthlyVolume'])
                case 'X2Y2':
                    daily_volume = 0 if r['data']['dailyVolume'] == None else float(r['data']['dailyVolume'])
                    weekly_volume = 0 if r['data']['WeeklyVolume'] == None else float(r['data']['WeeklyVolume'])
                    monthly_volume = 0 if r['data']['MonthlyVolume'] == None else float(r['data']['MonthlyVolume'])

            collection_address = 'no data' if r['data']['address'] == None else r['data']['address']
            daily_sales_count = 0 if r['data']['dailySalesCount'] == None else float(r['data']['dailySalesCount'])
            weekly_sales_count = 0 if r['data']['weeklySalesCount'] == None else float(r['data']['weeklySalesCount'])
            monthly_sales_count = 0 if r['data']['monthlySalesCount'] == None else float(r['data']['monthlySalesCount'])
            daily_average_price = 0 if r['data']['dailyAveragePrice'] == None else float(r['data']['dailyAveragePrice'])
            weekly_average_price = 0 if r['data']['weeklyAveragePrice'] == None else float(r['data']['weeklyAveragePrice'])
            monthly_average_price = 0 if r['data']['monthlyAveragePrice'] == None else float(r['data']['monthlyAveragePrice'])
            token_listed_count = 0 if r['data']['tokenListedCount'] == None else float(r['data']['tokenListedCount'])
            holders_count = 0 if r['data']['holders'] == None else float(r['data']['holders'])
            floor_price = 0 if r['data']['floorPrice']['price'] == None else float(r['data']['floorPrice']['price'])

            embed = discord.Embed(title='', color=0x6495ed)
            embed.set_image(url='https://open-graph.opensea.io/v1/collections/'f'{collection_slug}')
            embed.add_field(name='Daily Volume', value=f'{daily_volume:.2f} ETH', inline=True)
            embed.add_field(name='Weekly Volume', value=f'{weekly_volume:.2f} ETH', inline=True)
            embed.add_field(name='Monthly Volume', value=f'{monthly_volume:.2f} ETH', inline=True)
            embed.add_field(name='Daily Sales', value=f'{daily_sales_count} NFT', inline=True)
            embed.add_field(name='Weekly Sales', value=f'{weekly_sales_count} NFT', inline=True)
            embed.add_field(name='Monthly Sales', value=f'{monthly_sales_count} NFT', inline=True)
            embed.add_field(name='Daily Average Price', value=f'{daily_average_price:.2f} ETH', inline=True)
            embed.add_field(name='Weekly Average Price', value=f'{weekly_average_price:.2f} ETH', inline=True)
            embed.add_field(name='Monthly Average Price', value=f'{monthly_average_price:.2f} ETH', inline=True)
            embed.add_field(name='Token Listed Count', value=f'{token_listed_count:.2f}', inline=True)
            embed.add_field(name='Holders Count', value=f'{holders_count:.2f}', inline=True)
            embed.add_field(name='Floor Price', value=f'{floor_price:.2f} ETH', inline=True)

            match marketplace_name:
                case 'Opensea':
                    collection_link = f'https://opensea.io/collection/{collection_slug}'
                    footer_marketplace = 'OpenSea'
                    footer_icon = 'https://storage.googleapis.com/opensea-static/Logomark/Logomark-Blue.png'
                case 'Looksrare':
                    collection_link = f'https://looksrare.org/collections/{collection_address}'
                    footer_marketplace = 'LooksRare'
                    footer_icon = 'https://raw.githubusercontent.com/Xeift/Kizmeow-NFT-Discord-Bot/main/access/looks-green.png'
                case 'X2Y2':
                    collection_link = f'https://x2y2.io/collection/{collection_slug}/items'
                    footer_marketplace = 'X2Y2'
                    footer_icon = 'https://raw.githubusercontent.com/Xeift/Kizmeow-NFT-Discord-Bot/main/access/x2y2_logo.png'

            embed.set_author(name=collection_name, url=collection_link, icon_url=image_url)
            embed.set_footer(text=footer_marketplace,
                             icon_url=footer_icon)
            embed.timestamp = datetime.datetime.now()

            view = View(timeout=None)
            view.add_item(return_button)

            return (embed, view)
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        async def return_button_callback(interaction):
            if ctx.author == interaction.user:
                (embed, view) = await initial_embed()
                await interaction.response.edit_message(embed=embed, view=view)
            else:
                embed = discord.Embed(title='Consider use `/collection` command by yourself.', color=0xFFA46E)
                await interaction.response.send_message(embed=embed, ephemeral=True)
        return_button.callback = return_button_callback
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        async def opensea_button_callback(interaction):
            if ctx.author == interaction.user:
                (embed, view) = await marketplace_embed('Opensea')
                await interaction.response.edit_message(embed=embed, view=view)
            else:
                embed = discord.Embed(title='Consider use `/collection` command by yourself.', color=0xFFA46E)
                await interaction.response.send_message(embed=embed, ephemeral=True)
        opensea_button.callback = opensea_button_callback
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        async def looksrare_button_callback(interaction):
            if ctx.author == interaction.user:
                (embed, view) = await marketplace_embed('Looksrare')
                await interaction.response.edit_message(embed=embed, view=view)
            else:
                embed = discord.Embed(title='Consider use `/collection` command by yourself.', color=0xFFA46E)
                await interaction.response.send_message(embed=embed, ephemeral=True)
        looksrare_button.callback = looksrare_button_callback
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        async def x2y2_button_callback(interaction):
            if ctx.author == interaction.user:
                (embed, view) = await marketplace_embed('X2Y2')
                await interaction.response.edit_message(embed=embed, view=view)
            else:
                embed = discord.Embed(title='Consider use `/collection` command by yourself.', color=0xFFA46E)
                await interaction.response.send_message(embed=embed, ephemeral=True)
        x2y2_button.callback = x2y2_button_callback
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------


def setup(bot):
    bot.add_cog(collection(bot))