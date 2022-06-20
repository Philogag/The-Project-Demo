from typing import Any

from pydantic import BaseModel


class FileBytesCarrier(BaseModel):

    bytes_io: Any
    file_name: str
    file_ext: str

    @property
    def file_name_with_ext(self):
        """read-only"""
        return self.file_name + '.' + self.file_ext
