import datetime
import discord
from discord.ext import tasks
from datetime import datetime
import pytz

import secret

ch = secret.sn_ch
client = discord.Client()


@client.event
async def on_ready():
    channel = client.get_channel(ch)
    
    print('System start!')
    await channel.send(f"授業スケジュールが**授業開始15分前**に，<#{secret.sn_ch}>に投稿されます．")
    
@tasks.loop(seconds=60)
async def loop():
    # Botが起動するまで待つ
    await client.wait_until_ready()
    
    channel = client.get_channel(ch)
    
    # 現在時刻の取得
    now =  datetime.now(pytz.timezone('Asia/Tokyo'))
    now_a = now.strftime('%A')
    now_hm = now.strftime('%H:%M')
    
    # スケジュールのアナウンス
    if now_a == 'Sunday':
        if now_hm == secret.cfirst:
            await channel.send("今日は日曜日．良い休日を！")
        # elif now_hm == secret.csecond:
        #     await channel.send(f"")
        # elif now_hm == secret.cthird:
        #     await channel.send(f"")
        # elif now_hm == secret.cforth:
        #     await channel.send(f"")
    
    elif now_a == 'Monday':
        if now_hm == secret.cfirst:
            await channel.send("今日は月曜日．全休最高！")
        # elif now_hm == secret.csecond:
        #     await channel.send(f"")
        # elif now_hm == secret.cthird:
        #     await channel.send(f"")
        # elif now_hm == secret.cforth:
        #     await channel.send(f"")

    elif now_a == 'Tuesday':
        if now_hm == secret.cfirst:
            await channel.send(f"<@&{secret.srole}> \n 今日は火曜日．15分後に1,2限，**{secret.tue_12_class}**の授業が始まるよ．\n Zoom: {secret.tue_12_zoom}")
        # elif now_hm == secret.csecond:
        #     await channel.send(f"")
        elif now_hm == secret.cthird:
            await channel.send(f"<@&{secret.srole}> \n 15分後に3,4限，**{secret.tue_34_sa}**のSAが始まるよ． \n Zoom: {secret.tue_34_zoom}")
        # elif now_hm == secret.cforth:
        #     await channel.send(f"")
        
    elif now_a == 'Wednesday':
        if now_hm == secret.cfirst:
            await channel.send(f'<@&{secret.srole}> \n 今日は水曜日．15分後に1限，{secret.wed_1_class}の授業が始まるよ． \n Boys<:mens:>: Zoom: {secret.wed_1_zoom_men} \n Girls<:womens:>: Zoom: {secret.wed_1_zoom_women}')
        elif now_hm == secret.csecond:
            await channel.send(f"<@&{secret.srole}> \n 実は1限から2コマ，{secret.wed_12_sa}のSAが始まってるぞ！ \n Zoom: {secret.wed_12_zoom}")
        # elif now_hm == secret.cthird:
        #     await channel.send(f"")
        # elif now_hm == secret.cforth:
        #     await channel.send(f"")
        
    elif now_a == 'Thursday':
        if now_hm == secret.cfirst:
            await channel.send(f"<@&{secret.srole}> \n 今日は木曜日．15分後に1,2限，{secret.thu_12_class}の授業が始まるよ． \n Zoom: {secret.thu_12_zoom}")
        # elif now_hm == secret.csecond:
        #     await channel.send(f"")
        # elif now_hm == secret.cthird:
        #     await channel.send(f"")
        # elif now_hm == secret.cforth:
        #     await channel.send(f"")
        
    elif now_a == 'Friday':
        if now_hm == secret.cfirst:
            await channel.send(f"<@&{secret.srole}> \n 今日は華の金曜日:beers: 3限からがんばろう．")
        # elif now_hm == secret.csecond:
        #     await channel.send(f"")
        elif now_hm == secret.cthird:
            await channel.send(f"<@&{secret.srole}> \n 今日は金曜日．15分後に3,4限，{secret.fri_34_class}の授業が始まるよ． \n Zoom: {secret.fri_34_zoom}")
        # elif now_hm == secret.cforth:
        #     await channel.send(f"")
        
    elif now_a == 'Saturday':
        if now_hm == secret.cfirst:
            await channel.send('今日は土曜日．良い休日を．')
        # elif now_hm == secret.csecond:
        #     await channel.send(f"")
        # elif now_hm == secret.cthird:
        #     await channel.send(f"")
        # elif now_hm == secret.cforth:
        #     await channel.send(f"")
        
#ループ処理実行
loop.start()
# Botの起動とDiscordサーバーへの接続
client.run(secret.TOKEN1)