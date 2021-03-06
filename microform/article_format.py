#import html
from HTMLParser import HTMLParser
import re

from tomd import Tomd


class References(object):

    def __init__(self):
        self.references = []
        self.pattern = r'<a.*?href="(.*?)".*?>(.*?)<\/a>'
        self.content = ''
        self.endnotes = ''

    def process(self, content):
        new_string, n = re.subn(self.pattern,
                                self._get_ref,
                                content,
                                count=1)

        if n < 1:
            self._create_endnotes()
            return content

        return self.process(new_string)

    def _create_endnotes(self):

        endnotes = ''
        for i, ref in enumerate(self.references):
            num = i + 1
            endnotes += '[{}] {}\n'.format(num, ref)

        self.endnotes += endnotes

    def _get_ref(self, matchobj):

        url, text = matchobj.groups()

        self.references.append(url)

        return '{} [^{}]'.format(text, len(self.references))


class ArticleFormatter(object):

    def __init__(self, result, references=False):
        self.url = result['url'].encode("utf-8")
        self.title = HTMLParser().unescape(result['title']).encode("utf-8")
        self.content = HTMLParser().unescape(result['content']).encode("utf-8")
        self.refs = References() if references else None

    def render(self):
        endnotes = ''
        if self.refs:
            self.content = self.refs.process(self.content)
            endnotes = '\n' + self.refs.endnotes

        return self.title + '\n' + self.url + '\n' + Tomd(self.content).markdown + endnotes
