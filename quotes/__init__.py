from quixote.publish import Publisher
import sys

from apps import QuotesApp

def setup():
    quotes_app = QuotesApp('quotes/quotes.txt', './html')
    return quotes_app

def teardown():
    pass