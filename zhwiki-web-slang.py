#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import urllib.parse
import urllib.request
import collections
import sys
import re

def fetch():
    _ZHWIKI_SOURCE_URL = "https://zh.wikipedia.org/w/api.php?action=parse&format=json&prop=wikitext&uselang=zh&formatversion=2&page="
    _PAGE = "中国大陆网络用语列表"

    page = urllib.request.urlopen(_ZHWIKI_SOURCE_URL + urllib.parse.quote(_PAGE)).read()
    wikitext = json.loads(page)["parse"]["wikitext"]
    return wikitext

def process(wikitext):
    words = collections.OrderedDict()

    def add_word(word):
        if word.startswith("形容"):
            return
        words[word.strip()] = None

    for line in wikitext.split("\n"):
        pattern = r"\b[\u4e00-\u9fa5]{2,9}\b"
        matches = re.findall(pattern, line)
        
        for match in matches:
            add_word(match)

    return words

def print_words(words):
    for word in words:
        print(word)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        wikitext = fetch()
        words = process(wikitext)
        print_words(words)

    elif sys.argv[1] == "--fetch":
        print(fetch())

    elif sys.argv[1] == "--process":
        wikitext = open(sys.argv[2]).read()
        print_words(process(wikitext))

    else:
        raise NotImplementedError
