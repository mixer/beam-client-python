"""
Example chat bot that monitors incoming messages and sends "Hi!" every second.
"""

from chatty import create
import config

from tornado.ioloop import PeriodicCallback, IOLoop
from functools import partial


if __name__ == "__main__":
    chat = create(config)

    # Tell chat to authenticate with the beam server. It'll throw
    # a chatty.errors.NotAuthenticatedError if it fails.
    chat.authenticate(config.CHANNEL)

    # Listen for incoming messages. When they come in, just print them.
    chat.on("message", partial(print, "RECEIVE:"))

    # Create a timer that sends the message "Hi!" every second.
    PeriodicCallback(
        lambda: chat.message('Hi!'),
        1000
    ).start()

    # Start the tornado event loop.
    IOLoop.instance().start()
