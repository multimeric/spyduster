import requests
from email.message import Message


def response_filename(response: requests.Response) -> str:
    """
    Extracts the filename from the Content-Disposition header of a response.
    """
    if "Content-Disposition" in response.headers:
        msg = Message()
        msg['content-disposition'] = response.headers["Content-Disposition"]
        if (filename := msg.get_filename()) is not None:
            return filename
    raise ValueError("No filename found in Content-Disposition header")