import os
import re
import json
import configparser
import errno
import requests


class Text2VoiceException(Exception):
    pass


def replace_text(matching_pattern, replace_characters, text):
    matched_list = re.findall(matching_pattern, text)
    for matched_characters in matched_list:
        text = text.replace(matched_characters, replace_characters)

    return text


def replace_text_all(text, user_dictionary):
    # Replace unnecessary characters in text such as URL, email, user, etc.
    # WARNING: DO NOT set no character in the replacement characters.
    # 現状、置き換え文字を空白にしてしまうと、入力した文字によっては置き換え後の読み上げテキスト文字列が何もなくなってしまい、エラーを起こします。
    DEFAULT_MATCHING_PATTERN = [
        ['URL', 'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', "URL"],
        ['MAIL', '[\w\-._]+@[\w\-._]+\.[A-Za-z]+', 'メール'],
        ['USER', '<@![\d]+>', 'ユーザー'],
        ['CUSTOM_EMOJI', '<:[\w]+:[\d]+>', '絵文字'],
        ['EMOJI', ':[\w]+:', '絵文字'],
    ]

    for replacement_set in DEFAULT_MATCHING_PATTERN:
        pattern = replacement_set[1]
        replace_characters = replacement_set[2]
        text = replace_text(pattern, replace_characters, text)

    # Replace user-defined characters in text
    for replacement_set in user_dictionary:
        pattern = replacement_set[0]
        replace_characters = replacement_set[1]
        text = replace_text(pattern, replace_characters, text)

    return text


class T2V(object):

    def __init__(self, api_key, api_endpoint, user_dictionary, speaker='show'):
        self._default_speaker = speaker
        self.api_preference = {'speaker': self._default_speaker}
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.user_dictionary = user_dictionary

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
        output = os.path.join(output_dir, output_filename)

        read_text = replace_text_all(text, user_dictionary)
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
    user_dictionary = json.loads(config_ini['General']['USER_DICTIONARY'])

    t2v = T2V(api_key=voiceText_api_key, api_endpoint=voiceText_api_endpoint, user_dictionary=user_dictionary)
    t2v.generate_voice(
        "これはテスト用に作成した音声です。https://www.google.com, hogehoge@ezweb.ne.jp, <@!123456789>, :fire:, <:fire:123456789>")
    print("OK")
