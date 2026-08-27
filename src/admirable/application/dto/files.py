from collections.abc import AsyncIterator
from dataclasses import dataclass


@dataclass
class UploadedFileDTO:
    filename: str
    content_type: str
    stream: AsyncIterator[bytes]
