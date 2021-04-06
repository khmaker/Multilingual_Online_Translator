import requests

from bs4 import BeautifulSoup

import sys

LANGUAGES = {'all', 'arabic', 'german', 'english', 'spanish', 'french',
             'hebrew', 'japanese', 'dutch', 'polish', 'portuguese',
             'romanian', 'russian', 'turkish',
             }


class Translator:
    LANGUAGES = {'all', 'arabic', 'german', 'english', 'spanish', 'french',
                 'hebrew', 'japanese', 'dutch', 'polish', 'portuguese',
                 'romanian', 'russian', 'turkish',
                 }

    def __init__(self, language_from, language_to, word):
        self.language_from = language_from
        self.language_to = language_to
        self.word = word
        self.check_languages()
        self.translate()

    def check_languages(self):
        for lang in (self.language_to, self.language_from):
            if lang not in self.LANGUAGES:
                print(f'Sorry, the program doesn\'t support {lang}')
                sys.exit(0)

    def translate(self):
        pass

    def print_file(self):
        with open(f'{self.word}.txt', 'r', encoding='UTF-8') as f:
            print(f.read())


def translate(language_from, language_to, word):
    if language_to not in LANGUAGES:
        return print(f'Sorry, the program doesn\'t support {language_to}')
    if language_from not in LANGUAGES:
        return print(f'Sorry, the program doesn\'t support {language_from}')
    session = requests.session()
    n = None
    if language_to == 'all':
        LANGUAGES.remove('all')
        LANGUAGES.remove(language_from)
        for value in LANGUAGES:
            n = connect_to_site(language_from, value, word, session)
    else:
        n = connect_to_site(language_from, language_to, word, session, limit=5)
    if n is not None:
        return print(n)
    with open(f'{word}.txt', 'r', encoding='UTF-8') as f:
        print(f.read())


def connect_to_site(language_from, language_to, word, session, limit=2):
    link = f'https://context.reverso.net/translation/{language_from}-' \
           f'{language_to}/{word}'
    r = session.get(link.lower(), headers={'User-Agent': 'Mozilla/5.0'})
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        translations = soup.find(id='translations-content')('a', limit=limit)
        examples = soup.find(id='examples-content')(class_='text',
                                                    limit=limit * 2)
        write_to_file(translations, examples, language_to, word)
    elif r.status_code == 404:
        return f'Sorry, unable to find {word}'
    else:
        return 'Something wrong with your internet connection'
    return None


def write_to_file(translations, examples, language, word):
    with open(f'{word}.txt', 'a', encoding='UTF-8') as file:
        file.write(f'{language} Translations:\n')
        for trans in translations:
            file.write(trans.text.strip())
            file.write('\n')
        file.write('\n')

        file.write(f'{language} Examples:\n')
        for ex in examples:
            file.write(ex.text.strip())
            file.write('\n')
        file.write('\n')


if __name__ == '__main__':
    # a = Translator(*sys.argv[1:4])
    translate(*sys.argv[1:4])
