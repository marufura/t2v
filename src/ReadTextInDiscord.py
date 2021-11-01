import os
import glob
import configparser
import errno

import discord
from discord.ext import commands

import Text2Voice


def generate_mp3_for_discord(mp3_file_path):
    executable = os.path.dirname(__file__) + '/ffmpeg.exe'
    mp3 = discord.FFmpegPCMAudio(executable=executable, source=mp3_file_path)
    return mp3


class ReadTextInDiscord(commands.Cog):
    def __init__(self, bot, t2v):
        super().__init__()
        self.bot = bot
        self.t2v = t2v
        self.t2v.volume(200)

    @commands.command()
    async def hello(self, ctx):
        """Botをボイスチャンネルに接続します。"""
        voice_state = ctx.author.voice

        if (not voice_state) or (not voice_state.channel):
            await ctx.send("先にボイスチャンネルに入っている必要があります。")
            return

        channel = voice_state.channel
        await channel.connect()
        await ctx.send("ボイスチャンネルに接続しました。")

    @hello.error
    async def hello_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("既にボイスチャンネルに接続しています")

    @commands.command()
    async def bye(self, ctx):
        """Botをボイスチャンネルから切断します。"""
        voice_client = ctx.message.guild.voice_client

        if not voice_client:
            await ctx.send("Botはボイスチャンネルに参加していません。")
            return

        await voice_client.disconnect()
        await ctx.send("ボイスチャンネルから切断しました。")

    @commands.command()
    async def speaker(self, ctx, arg):
        """読み上げBotの声を変更します。"""
        if arg in ['show', 'haruka', 'hikari', 'takeru', 'santa', 'bear']:
            self.t2v.speaker(arg)
        else:
            await ctx.send("次の選択肢から選ぶ必要があります\n[show, haruka, hikari, takeru, santa, bear]")

    @commands.command()
    async def reset(self, ctx):
        """読み上げBotの設定を全てデフォルト値に戻します。"""
        self.t2v.reset()

    @commands.command()
    async def music(self, ctx, arg):
        """mp3ファイルを再生します。再生中は読み上げ機能が無効になります。[t2v.bye]で疑似的に再生終了できます。[t2v.music list]でローカル保存されているmp3ファイルを参照できます。"""
        music_path = os.path.dirname(__file__) + '/music'
        os.makedirs(music_path, exist_ok=True)
        sound_path = music_path + '/' + arg + '.mp3'

        if arg == 'list':
            sound_all = '保存中のmp3ファイル\n'
            files = glob.glob(music_path + "/*")
            for file in files:
                file = file.replace(music_path + '\\', '')
                file = file.replace('.mp3', '')
                sound_all = sound_all + ' - ' + file + '\n'
            await ctx.send(sound_all)
            return

        if not os.path.exists(sound_path):
            await ctx.send("指定されたファイルが存在しません。[t2v.music list]で確認")
            return

        mp3 = generate_mp3_for_discord(sound_path)
        ctx.guild.voice_client.play(mp3)


def main():
    # load config.ini
    config_ini = configparser.ConfigParser()
    config_ini_path = '../config.ini'
    if not os.path.exists(config_ini_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_ini_path)
    config_ini.read(config_ini_path, encoding='utf-8')

    discord_bot_token = config_ini['Discord']['TOKEN']
    greeting_channel = int(config_ini['Discord']['CHANNEL_ID'])
    voiceText_api_key = config_ini['VoiceText Web API']['API_KEY']
    voiceText_api_endpoint = config_ini['VoiceText Web API']['API_ENDPOINT']

    # Text2Voice
    t2v = Text2Voice.T2V(api_key=voiceText_api_key, api_endpoint=voiceText_api_endpoint)
    command_prefix = "t2v."
    bot = commands.Bot(command_prefix=command_prefix)
    bot.add_cog(ReadTextInDiscord(bot=bot, t2v=t2v))

    @bot.event
    async def on_ready():
        print('起動しました')
        channel = bot.get_channel(greeting_channel)
        embed = discord.Embed(title="Text2Voice",
                              description='コマンド一覧は \'t2v.help\' で確認できます',
                              color=discord.Colour.blue())
        embed.set_thumbnail(
            url="https://4.bp.blogspot.com/-15Zk1xUSJsk/WtRzFXf_X7I/AAAAAAABLjs/Y8EwsDjig5ceATVAEKNm-FbqsfRqyXtLQCLcBGAs/s800/kakuseiki_man_angry.png")
        await channel.send(embed=embed)

    @bot.event
    async def on_message(message):
        # メッセージ送信者がBotだった場合は無視する
        if message.author.bot:
            return

        # コマンド送信時以外
        if message.content.startswith(command_prefix):
            pass
        elif message.channel.id != greeting_channel:
            pass
        else:
            if message.guild.voice_client:
                try:
                    read_text = generate_mp3_for_discord(t2v.generate_voice(message.content))
                    message.guild.voice_client.play(read_text)
                except discord.errors.ClientException:
                    await message.channel.send("他のmp3ファイルを再生中です。再生が終了するまで待ってください。")
            else:
                pass
        await bot.process_commands(message)

    # disconnect from voice channel if bot is alone
    @bot.event
    async def on_voice_state_update(member, before, after):
        # print(member.name + ': ' + str(before.channel) + ' -> ' + str(after.channel))
        if after.channel is None and len(before.channel.members) == 1:
            for rest_member in before.channel.members:
                if rest_member.bot:
                    await member.guild.voice_client.disconnect()

    # Botの起動とDiscordサーバーへの接続
    bot.run(discord_bot_token)


if __name__ == '__main__':
    main()
