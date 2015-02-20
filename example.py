#!env/bin/python

from tornado import ioloop
import threading
import chatty
import config


# Example chat bot that monitors incoming messages and prints out
# "Hi!" every second.
if __name__ == '__main__':
    chat = chatty.create(config)

    # Tell chat to authenticate with the beam server. It'll throw
    # a chatty.errors.NotAuthenticatedError if it fails.
    chat.authenticate(config.CHANNEL)

    # Listen for incoming messages. When they come in, just print
    # them.
    chat.on('message', lambda msg: print(msg))

    # Create a timer that sends the message "Hi!" every second.
    ioloop.PeriodicCallback(
        lambda: chat.message('Hi!'),
        1000
    ).start()

    # Start the tornado event loop.
    ioloop.IOLoop.instance().start()
