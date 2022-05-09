import discord
from discord.ext import commands

import secret

ch = secret.po_ch
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    channel = bot.get_channel(ch)
    
    print(f'Logged in as {bot.user.name}')
    print('------')
    
    embed = discord.Embed(title="pay-off Bot", description="割り勘計算用に使えます．", color=discord.Colour.green())
    embed.add_field(name="使い方", value="!cul 誰に支払うか 合計金額 支払う人 \n 例: `!cul @Aさん 5000 @Bさん @Cさん @...`", inline=False)
    
    await channel.send(embed=embed)

@bot.command()
async def cul(ctx, payer, total, *member):
    channel = bot.get_channel(ch)
    
    if ctx.channel.id == ch:
        # 例外処理
        if len(member) == 0:
            await channel.send("> 支払う人がいません．正しい形で入力してください．")
        else:
            # 割り勘を求め，小数点を丸める．
            pp = round(int(total) / (len(member) + 1))
            # # 表示をきれいにするためにリストを文字列に変換
            # members = ' '.join(member)
            
            embed = discord.Embed(title=f"支払った人", description=f"{payer}", color=discord.Colour.green())
            embed.add_field(name=f"今回の支払い金額", value=f"**{total}円**", inline=False)
            embed.add_field(name=f"一人当たりの金額", value=f"**{pp}円**", inline=False)
            embed.add_field(name="Attention", value="支払った人はリアクションをつけてね！", inline=False)
            # await ctx.reply(f"{members}", embed=embed)
            await ctx.reply(embed=embed)
    
bot.run(secret.TOKEN1)