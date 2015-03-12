import requests
from .auth import AuthBase

class Client():

    def __init__(self):
        self._provider = AuthBase()
        self.beam_url = 'https://beam.pro/api/v%s/'
        self.api_version = 1

    def setVersion(self, version):
        """
        Sets the numeric API version to interpolate with the URL.
        """
        self.api_version = version
        return self

    def setUrl(self, url):
        """
        Sets the beam URL to use. %s will be interpolated with the
        API version (defaults to `1` currently)
        """
        self.beam_url = url
        return self

    def _build_address(self, path):
        """
        Builds a URL to the given `path` on the Beam API.
        """
        url = self.beam_url % self.api_version
        return url.rstrip('/') + '/' + path.lstrip('/')

    def auth(self, provider):
        """
        Sets up and attempts to authenticate using the given provider.
        """
        self._provider = provider

        # This will throw an exception if it fails.
        provider.use(self).attempt()
        return self

    def use(self, service):
        """
        Instantiates a service, passing in this client as the first
        argument in the call.
        """
        return service(self)

    def request(self, method, path, *args, **kwargs):
        """
        Attempts to run a request against the Beam API.
        """

        url = self._build_address(path)
        method = method.lower()

        if self._provider.authenticated():
            return self._provider.request(method, url, *args, **kwargs)
        else:
            return getattr(requests, method)(url, *args, **kwargs)
