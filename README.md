# beam-chatty

This is a super basic chat bot framework for Beam, built to serve as a basic example of a Beam chat bot.

## Usage

We've built a chat bot that logs incoming messages to the console, and sends "Hi!" to the channel every second.

To use it, ensure Python 3 is installed on your system. Then:

```bash
# install dependencies
python setup.py install
# copy the config and fill it in with your details
cp config.example.json config.json
vi config.json
# start the example chatbot
python example.py
```

## License

Public domain: CC0 1.0 Univeral License ([text](https://creativecommons.org/publicdomain/zero/1.0/legalcode))
