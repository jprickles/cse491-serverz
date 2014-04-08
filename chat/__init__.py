from quixote.publish import Publisher
import sys

from apps import ChatApp

def setup():
	chat_app = ChatApp('./html')
	return chat_app

def teardown():
    pass