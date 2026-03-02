import json
import hashlib

from xml.etree import ElementTree


def parse_xml(file: bytes, filename: str) -> dict:
    root = ElementTree.fromstring(file.lstrip(b"\xef\xbb\xbf"))

    if article := root if root.tag == "article" else root.find("article"):
        return article.attrib

    raise ValueError(f"No <article> element found in {filename!r}")


def generate_hash(data: dict) -> str:
    return hashlib.sha256(json.dumps(data).encode("utf-8")).hexdigest()
