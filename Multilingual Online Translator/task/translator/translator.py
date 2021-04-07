import requests

from bs4 import BeautifulSoup

import sys
from pathlib import Path


class Translator:
    LANGUAGES = {'all', 'arabic', 'german', 'english', 'spanish', 'french',
                 'hebrew', 'japanese', 'dutch', 'polish', 'portuguese',
                 'romanian', 'russian', 'turkish',
                 }
    link = f'https://context.reverso.net/translation/'
    header = {'User-Agent': 'Mozilla/5.0'}

    def __init__(self, language_from, language_to, word):
        self.language_from = language_from
        self.language_to = language_to
        self.word = word
        self.check_languages()
        self.path = Path().absolute()
        self.session = requests.session()
        self.limit = 2 if self.language_to == 'all' else 5
        self.message = ''
        self.request = None
        self.translate()

    def exit_translator(self):
        print(self.message)
        sys.exit(0)

    def check_languages(self):
        for lang in (self.language_to, self.language_from):
            if lang not in self.LANGUAGES:
                self.message = f'Sorry, the program doesn\'t support {lang}'
                self.exit_translator()

    def translate(self):
        languages_to_process = (self.LANGUAGES - {'all', self.language_from}
                                if self.language_to == 'all'
                                else {self.language_to, })
        for language in sorted(languages_to_process):
            self.language_to = language
            self.process_connection()
            self.write_to_file(*self.process_soup())
        self.print_file()

    def process_connection(self):
        parameters = f'{self.language_from}-{self.language_to}/{self.word}'
        request = self.session.get(self.link + parameters,
                                   headers=self.header)
        status = request.status_code
        if status == 404:
            self.message = f'Sorry, unable to find {self.word}'
            self.exit_translator()
        if status != 200:
            self.message = 'Something wrong with your internet connection'
            self.exit_translator()
        self.request = request

    def process_soup(self):
        soup = BeautifulSoup(self.request.content, 'html.parser')
        translations = soup.find(id='translations-content')('a',
                                                            limit=self.limit)
        examples = soup.find(id='examples-content')(class_='text',
                                                    limit=self.limit * 2)
        return translations, examples

    def print_file(self):
        with open(f'{self.path}/{self.word}.txt', 'r', encoding='UTF-8') as f:
            print(f.read())

    def write_to_file(self, translations, examples):
        with open(f'{self.path}/{self.word}.txt', 'a', encoding='UTF-8') as f:
            lines = [f'\n{self.language_to} Translations:\n']
            lines += [t.text.strip() + '\n' for t in translations]
            f.writelines(lines)

            lines = [f'\n{self.language_to} Examples:\n']
            lines += [e.text.strip() + '\n' for e in examples]
            f.writelines(lines)


if __name__ == '__main__':
    Translator(*sys.argv[1:4])
