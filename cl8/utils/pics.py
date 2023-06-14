from django.core.files.images import ImageFile
import io
import logging
import requests
import typing

logger = logging.getLogger(__file__)


def fetch_user_pic(url: str = None) -> typing.Union[ImageFile, None]:
    """
    Fetch a picture from a given url, returning an Django Imagefile,
    and fail gracefully if the connection fails.
    """
    if not url:
        return None
    try:
        res = requests.get(url)
    except Exception as err:
        logger.warning(f"Unable to get url: {url}: Error: {err}")

    if res.content:
        filename = url.split("/")[-1]
        return ImageFile(io.BytesIO(res.content), name=filename)
