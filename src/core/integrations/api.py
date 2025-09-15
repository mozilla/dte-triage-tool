import base64
import requests
import logging


class TestRailAPIClient:
    """
    TestRail API session.

    Attributes:
    ===========

    base_url: str
      The "home" of the instance in question.

    local: bool
      Assign True if communicating with an instance of an TestRail API on localhost.
    """
    def __init__(self, base_url, local=False):
        self.name = "TestRail"
        self.user = ""
        self.password = ""
        logging.info(f"base {base_url}")
        if not base_url.endswith("/"):
            base_url += "/"
        if local:
            self.__url = base_url
        else:
            self.__url = base_url + "index.php?/api/v2/"

    def __send_request(self, method, uri, data):
        url = self.__url + uri

        auth = str(
            base64.b64encode(bytes("%s:%s" % (self.user, self.password), "utf-8")),
            "ascii",
        ).strip()
        headers = {"Authorization": "Basic " + auth}

        if method == "POST":
            if uri[:14] == "add_attachment":  # add_attachment API method
                files = {"attachment": (open(data, "rb"))}
                response = requests.post(url, headers=headers, files=files)
                files["attachment"].close()
            else:
                headers["Content-Type"] = "application/json"
                response = requests.post(url, headers=headers, json=data)
        else:
            headers["Content-Type"] = "application/json"
            response = requests.get(url, headers=headers)

        if response.status_code > 201:
            try:
                error = response.json()
            except (
                requests.exceptions.HTTPError
            ):  # response.content not formatted as JSON
                error = str(response.content)
            raise APIError(
                "TestRail API returned HTTP %s (%s)" % (response.status_code, error)
            )
        else:
            if uri[:15] == "get_attachment/":  # Expecting file, not JSON
                try:
                    open(data, "wb").write(response.content)
                    return data
                except FileNotFoundError:
                    return "Error saving attachment."
            else:
                try:
                    return response.json()
                except requests.exceptions.HTTPError:
                    return {}

    def send_get(self, uri, filepath=None):
        """Issue a GET request (read) against the API.

        Args:
            uri: The API method to call including parameters, e.g. get_case/1.
            filepath: The path and file name for attachment download; used only
                for 'get_attachment/:attachment_id'.

        Returns:
            A dict containing the result of the request.
        """
        return self.__send_request("GET", uri, filepath)

    def send_post(self, uri, data):
        """Issue a POST request (write) against the API.

        Args:
            uri: The API method to call, including parameters, e.g. add_case/1.
            data: The data to submit as part of the request as a dict; strings
                must be UTF-8 encoded. If adding an attachment, must be the
                path to the file.

        Returns:
            A dict containing the result of the request.
        """
        return self.__send_request("POST", uri, data)


class BugzillaAPIClient:
    """
    Bugzilla API session.

    Attributes:
    ===========

    base_url: str
      The "home" of the instance in question.

    local: bool
      Assign True if communicating with an instance of an Bugzilla API on localhost.
    """
    def __init__(self, base_url, local):
        self.name = "Bugzilla"
        if not base_url.endswith("/"):
            base_url += "/"
        self.api_key = None
        self.__url = base_url

    def __send_request(self, method, uri, data=None, **kwargs):
        params = kwargs.get("params") or {}
        if kwargs.get("secure"):
            logging.warning("secure send")
            params["api_key"] = self.api_key

        url = self.__url + uri
        logging.info(url)

        if method == "POST" or method == "PUT":
            # TODO: Handle BZ attachments
            if params:
                logging.warning(f"params {params}")
                response = requests.post(url, params=params, json=data)
            else:
                response = requests.post(url, json=data)
        else:
            if params:
                response = requests.get(url, params=params)
                logging.info(response.request.url)
            else:
                response = requests.get(url)

        if response.status_code > 201:
            try:
                error = response.json()
            except (
                requests.exceptions.HTTPError,
                requests.exceptions.JSONDecodeError
            ):  # response.content not formatted as JSON
                error = str(response.content)
            raise APIError(
                "Bugzilla API returned HTTP %s (%s)" % (response.status_code, error)
            )
        else:
            # TODO: Handle receiving BZ attachments
            try:
                return response.json()
            except requests.exceptions.HTTPError:
                return {}

    def send_get(self, uri, filepath=None, **kwargs):
        return self.__send_request("GET", uri, filepath, **kwargs)

    def send_post(self, uri, data, **kwargs):
        return self.__send_request("POST", uri, data, **kwargs)

    def send_put(self, uri, data, **kwargs):
        return self.__send_request("PUT", uri, data, **kwargs)

class APIError(Exception):
    pass
