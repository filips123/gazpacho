import json
from typing import Dict, Optional, Union
from urllib.error import HTTPError as UrllibHTTPError
from urllib.parse import urlencode
from urllib.request import build_opener

from .utils import sanitize, HTTPError


def get(
    url: str,
    params: Optional[Dict[str, str]] = None,
    headers: Optional[Dict[str, str]] = None,
) -> Union[str, dict]:
    """Retrive url contents

    Params:

    - url: target page
    - params: GET request payload
    - headers: GET request headers

    Example:

    ```
    get('https://httpbin.org/anything', {'soup': 'gazpacho'})
    ```
    """
    url = sanitize(url)
    opener = build_opener()
    if params:
        url += "?" + urlencode(params)
    if headers:
        for h in headers.items():
            opener.addheaders = [h]
    if (headers and not headers.get("User-Agent")) or not headers:
        UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0"
        opener.addheaders = [("User-Agent", UA)]
    try:
        with opener.open(url) as response:
            content = response.read().decode("utf-8")
            if response.headers.get_content_type() == "application/json":
                content = json.loads(content)
    except UrllibHTTPError as e:
        raise HTTPError(e.code, e.msg) from None
    return content
