import asyncio
import discord
import pickle
import re

from google.cloud import texttospeech

import secret


name = "ja-JP-Wavenet-B"
ch = secret.tts_ch
client = discord.Client()

# 連投処理用
message_list = []

@client.event
async def on_ready():
    channel = client.get_channel(ch)
    print('System start!')
    embed = discord.Embed(title='tts bot', description='Text-to-Speech の料金は、音声への合成のためにサービスに送信された文字数に基づいて、月単位で請求されます。WaveNet 音声の最初の 100 万文字は、毎月無料です。標準（WaveNet 以外の）音声では、最初の 400 万文字が毎月無料です。Text-to-Speech は無料枠以降 100 万文字ごとに課金されます。', color=discord.Colour.red())
    embed.add_field(name='Commands List', value='`!helptts`でコマンド一覧を表示します')
    await channel.send(embed=embed)
    
@client.event
async def on_message(message):
    try:
        channel = client.get_channel(ch)
        
        await client.wait_until_ready()
        
        # チャンネル指定
        if message.channel.id == ch:
            # BOTのメッセージは無視
            if message.author.bot:
                return
        
            if message.content == '!helptts':
                embed = discord.Embed(title='tts bot', description='Text-to-Speech の料金は、音声への合成のためにサービスに送信された文字数に基づいて、月単位で請求されます。WaveNet 音声の最初の 100 万文字は、毎月無料です。標準（WaveNet 以外の）音声では、最初の 400 万文字が毎月無料です。Text-to-Speech は無料枠以降 100 万文字ごとに課金されます。',color=discord.Colour.red())
                embed.add_field(name="!helptts", value="tts botのコマンド一覧を表示します", inline=False)
                embed.add_field(name="!vc", value="僕をVCに呼ぶためのコマンド", inline=False)
                embed.add_field(name="!vcb", value="僕をVCから切断するためのコマンド", inline=False)
                await channel.send(embed=embed)
                
            if message.content == '!vc':
                if message.author.voice is None:
                    await channel.send('> YOU ARE NOT IN VOICE CHANNEL.')
                with open('./main/name.pickle', 'rb') as f:
                    name = pickle.load(f)
                await message.author.voice.channel.connect()
                
            if message.content == '!vcb':
                if message.guild.voice_client is None:
                    await channel.send('> I AM NOT IN VOICE CHANNEL.')
                await message.guild.voice_client.disconnect()
                await channel.send('> SEE YOU AGAIN')
                
            if message.content.startswith('!voicelist'):
                embed = discord.Embed(title='Wavenetの音声種類一覧', description='**!setvoice A**のようなコマンドで音声を変更できます.', color=discord.Colour.red())
                embed.add_field(name="!setvoice A", value="高い声の女性音声を選択します．", inline=False)
                embed.add_field(name="!setvoice B", value="落ち着いた声の女性音声を選択します．", inline=False)
                embed.add_field(name="!setvoice C", value="男性音声を選択します．Dと違いがわからない．", inline=False)
                embed.add_field(name="!setvoice D", value="男性音声を選択します．Cと違いがわからない．", inline=False)
                await channel.send(embed=embed)
            
            if message.content.startswith('!setvoice '):
                if message.content == "!setvoice A":
                    with open('./main/name.pickle', 'wb') as f:
                        pickle.dump("ja-JP-Wavenet-A", f)
                    await message.reply('> VOICE SET TO ja-JP-Wavenet-A')
                elif message.content == "!setvoice B":
                    with open('./main/name.pickle', 'wb') as f:
                        pickle.dump("ja-JP-Wavenet-B", f)
                    await message.reply('> VOICE SET TO ja-JP-Wavenet-B')
                elif message.content == "!setvoice C":
                    with open('./main/name.pickle', 'wb') as f:
                        pickle.dump("ja-JP-Wavenet-C", f)
                    await message.reply('> VOICE SET TO ja-JP-Wavenet-C')
                elif message.content == "!setvoice D":
                    with open('./main/name.pickle', 'wb') as f:
                        pickle.dump("ja-JP-Wavenet-D", f)
                    await message.reply('> VOICE SET TO ja-JP-Wavenet-D')
                    
            else:
                if message.content != '!helptts' or '!voicelist' or '!setvoice A' or '!setvoice B'  or '!setvoice C'  or '!setvoice D' or '!vc' or '!vcb':
                    if message.guild.voice_client is None:
                        return
                    
                    # ttsの変数`name`の読み込み
                    with open('./main/name.pickle', 'rb') as f:
                        name = pickle.load(f)
                    
                    # message内にURLが含まれているかどうか判定
                    url = re.findall("https?://[\w/:%#\$&\?\(\)~\.=\+\-]+", message.content)
                    
                    if len(url) == 0:
                        message.content = message.content
                    else:
                        while len(url) != 0:
                            message.content = message.content.replace(url[0], 'URL')
                            del url[0]
                    
                    # 入力されたメッセージを格納
                    message_list.append(message.content)
                    print(message_list)
                    
            # ttsの処理
            while len(message_list) != 0:
                # 再生中は処理が終わるまで待つ
                if message.guild.voice_client.is_playing():
                    await asyncio.sleep(1)
                else:
                    # discordのclientと被るのでgclientにする
                    gclient = texttospeech.TextToSpeechClient()
                    synthesis_input = texttospeech.SynthesisInput(text=message_list[0])
                    voice = texttospeech.VoiceSelectionParams(
                        # nameで声を変更
                        language_code="ja-JP", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, name=name
                    )
                    audio_config = texttospeech.AudioConfig(
                        audio_encoding=texttospeech.AudioEncoding.MP3
                    )
                    response = gclient.synthesize_speech(
                        input=synthesis_input, voice=voice, audio_config=audio_config
                    )
                    with open("output.mp3", "wb") as out:
                        # Write the response to the output file.
                        out.write(response.audio_content)
                        print('Audio content written to file "output.mp3"')
                        
                    message.guild.voice_client.play(discord.FFmpegPCMAudio('output.mp3'))
                    
                    # # なんのために書いたか思い出せない
                    # if len(message_list) == 0:
                    #     return
                    
                    # 読み上げたメッセージをリストから消す
                    del message_list[0]
                    
    except UnboundLocalError:
        await channel.send("UnboundLocalError: 変数`name`が設定されていないので**!setvoice**を用いて音声を設定してください．音声の種類は**!voicelist**で確認できます．")
    
    
client.run(secret.TOKEN1)