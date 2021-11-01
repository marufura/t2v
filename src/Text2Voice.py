import os
import re
import configparser
import errno
import requests


class Text2VoiceException(Exception):
    pass


def replace_text(text):
    # URLを抽出して書き換え
    url_matching_pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    url_list = re.findall(url_matching_pattern, text)
    # print(url_list)
    for url in url_list:
        text = text.replace(url, 'URL')

    # mailを抽出して書き換え
    mail_matching_pattern = '[\w\-._]+@[\w\-._]+\.[A-Za-z]+'
    mail_list = re.findall(mail_matching_pattern, text)
    # print(mail_list)
    for mail in mail_list:
        text = text.replace(mail, 'Mail')

    # ユーザを識別して書き換え
    usr_matching_pattern = '<@![\d]+>'
    usr_list = re.findall(usr_matching_pattern, text)
    # print(usr_list)
    for usr in usr_list:
        text = text.replace(usr, 'ユーザー')

    # カスタム絵文字を識別して書き換え
    emoji_matching_pattern = '<:[\w]+:[\d]+>'
    emoji_list = re.findall(emoji_matching_pattern, text)
    # print(emoji_list)
    for emoji in emoji_list:
        text = text.replace(emoji, '絵文字')

    return text


class T2V(object):

    def __init__(self, api_key, api_endpoint, speaker='show'):
        self._default_speaker = speaker
        self.api_preference = {'speaker': self._default_speaker}
        self.api_key = api_key
        self.api_endpoint = api_endpoint

        try:
            self.generate_voice('test')
        except Text2VoiceException:
            raise Text2VoiceException('HTTP basic auth error')

    def reset(self):
        self.api_preference = {'speaker': self._default_speaker}
        return self

    def speaker(self, speaker):
        if speaker in ['show', 'haruka', 'hikari', 'takeru', 'santa', 'bear']:
            self.api_preference['speaker'] = speaker

        return self

    def volume(self, volume):
        if isinstance(volume, int):
            if volume < 50:
                volume = 50
            elif 200 < volume:
                volume = 200
            self.api_preference['volume'] = volume

        return self

    def generate_voice(self, text):
        output_dir = os.path.dirname(__file__) + '/cache'
        os.makedirs(output_dir, exist_ok=True)
        output_filename = "tmp.mp3"
        output = output_dir + '/' + output_filename

        read_text = replace_text(text)
        self.api_preference['text'] = read_text
        result = requests.post(self.api_endpoint, data=self.api_preference, auth=(self.api_key, ""))
        if result.status_code != requests.codes.ok:
            raise Text2VoiceException('Invalid status code: %d' % result.status_code)
        with open(output, 'wb') as tmp:
            tmp.write(result.content)
        return output


# this is for test
if __name__ == '__main__':
    # load config.ini
    config_ini = configparser.ConfigParser()
    config_ini_path = '../config.ini'
    if not os.path.exists(config_ini_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_ini_path)
    config_ini.read(config_ini_path, encoding='utf-8')

    voiceText_api_key = config_ini['VoiceText Web API']['API_KEY']
    voiceText_api_endpoint = config_ini['VoiceText Web API']['API_ENDPOINT']

    t2v = T2V(api_key=voiceText_api_key, api_endpoint=voiceText_api_endpoint)
    t2v.generate_voice("これはテスト用に作成した音声です")
    print("OK")
