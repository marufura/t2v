```text
This software is released under the MIT License, see LICENSE.txt.
```

# Text2Voice (t2v)

VoiceText Web API を利用したテキストの読み上げ機能、ローカル保存されたmp3ファイルの再生機能(音楽再生機能)のあるDiscord BOTです。
普段から友人のサーバー内で使っているのですが、それなりに基本機能がしっかり出来てきたので公開しました。

他の読み上げbotがすぐ読み上げ上限に達してしまったり、ローカル保存した音楽を再生をしたい場合にどうぞ。
音声はデフォルトはモヤさまの声のやつです。

config.ini を自分用に追加するだけで使えるので、パソコンさえあればお手軽に設定・使用可能だと思います。
OptionでWindows限定ですがショートカット作成をしてワンクリックで起動できるようにする手順も書いておきます。

## License

OSSを利用したものについてのライセンスには詳しくなく、MIT License にしました。個人利用であれば問題なく使えるはずです。
ただし、以下のソフトウェアやライブラリの巨人の肩に乗っていることを考え適切なライセンス等あればそちらを適用します。
ライセンス周りに詳しい方で知っている場合には教えて頂けると幸いです。

- [VoiceText Web API](https://cloud.voicetext.jp/webapi)
- [ffmpeg](https://www.ffmpeg.org/)
- [discord.py](https://github.com/Rapptz/discord.py)
- [requests](https://2.python-requests.org/)

VoiceText Web API は利用については無料ですが、作成した音声データの商用利用や二次利用が禁止であるということに注意してください。

## Requirements

- Python 3.6 or later
- discord.py[voice]
- requests

## Installation

Requirementsに記載されたライブラリのインストールが必要です。

```shell
pip install requests
pip install 'discord.py[voice]'
```

また API key などを記載した config.ini を Text2Voice_Discord ディレクトリ上に作成する必要があります。

```shell
cd PATH/Text2Voice_Discord

# Mac or Linux
touch config.ini

# Windows
New-Item config.ini -type file
```

以下のテンプレートにしたがって{}にくくられた部分について config.ini を編集してください。
'' や "" で囲う必要はありません。
discord bot のトークン取得は日本語解説記事も多いので Google検索すれば多分すぐできると思います。

チャンネルIDは読み上げを行いたいテキストチャンネルのIDを入力してください。
USER_DICTIONARY はユーザー辞書です。

参考URL

- [discord bot token 取得方法](https://discordpy.readthedocs.io/ja/latest/discord.html)
- [チャンネルIDの取得](https://support.discord.com/hc/ja/articles/206346498-%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC-%E3%82%B5%E3%83%BC%E3%83%90%E3%83%BC-%E3%83%A1%E3%83%83%E3%82%BB%E3%83%BC%E3%82%B8ID%E3%81%AF%E3%81%A9%E3%81%93%E3%81%A7%E8%A6%8B%E3%81%A4%E3%81%91%E3%82%89%E3%82%8C%E3%82%8B-)
- [VoiceText Web API - API key の取得](https://cloud.voicetext.jp/webapi)
- [VoiceText Web API - API endpoint(URL) の記入](https://cloud.voicetext.jp/webapi/docs/api)

```ini
[Discord]
; Discord bot token: KEEP SECRET!
TOKEN = {Discord bot token}
; Read the text and send greeting messages of the channel in this CHANNEL_ID.
CHANNEL_ID = {channel id}

[VoiceText Web API]
; VoiceText Web API key: KEEP SECRET!
API_KEY = {VoiceText Web API key}
; API endpoint
API_ENDPOINT = {VoiceText Web API endpoint}

[General]
; ["pattern", "replaced string"] を入れて追加していく
; 例: [["hoge", "ほげ"], ["fuga", "ふが"], ["piyo", "ぴよ"]]
; 正規表現が使えません: 検討中
USER_DICTIONARY = []
```

## Starting

ReadTextInDiscord.py を実行してください。

```shell
cd PATH/Text2Voice_Discord
python src/ReadTextInDiscord.py
```

## Command

- t2v.help : コマンド一覧を表示
- t2v.hello : ボイスチャンネルに接続
  - コマンドを入力しているユーザーがボイスチャンネルに先に入っている必要があります。
- t2v.bye : ボイスチャンネルから切断
- t2v.speaker [speaker] : 読み上げBotの声を変更します。
  - [speaker]には VoiceText Web API で使用できるspeakerを選択してください。
- t2v.reset : BOT設定をデフォルトに戻します。
- t2v.music [arg] : src/music に保存された mp3 ファイルを再生します。[arg]に拡張子をつける必要はありません。
  - t2v.music list でローカル保存されているmp3ファイルを検索できます。
  - ex. hogehoge.mp3 が保存されていたら t2v.music hogehoge で再生。

## function

こまごました部分。

- URL, メール, ユーザー, カスタム絵文字を読みやすい形に変換します。
  - 前に読み上げbotを作った人ならわかるはず
  - URLは意図的に読まないようにしています。
- ボイスチャンネルに読み上げBOTのみが残った際に勝手にBOTも退出するようにしてあります。
- 例外処理: 割とほとんどの例外には対応できている(と思っている。)
- ユーザー辞書: iniファイルに加えれば使えます。ただし正規表現を利用したい場合は注意が必要です。

## Option

### Windows ショートカットの作成

Windows PC 限定ですが、ショートカット作成をしてワンクリックで起動できるようにする方法を書いておきます。
結構お手軽に使えるので愛用してます。

- [Qiita](#)

