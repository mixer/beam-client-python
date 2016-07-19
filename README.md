# beam-client-python [![](https://badges.gitter.im/WatchBeam/beam.png)](https://gitter.im/MCProHosting/beam-dev)

This is a basic chat bot framework for Beam, built to serve as a basic example of a Beam chat bot.

## Usage

We've built a chat bot that logs incoming messages to the console, and sends "Hi!" to the channel every second.

To use it, ensure Python 3 is installed on your system. Then:

```bash
# install dependencies
python setup.py install

# copy the config and fill it in with your details
cp config.example.py config.py
vi config.py

# start the example chatbot
python example.py
```
