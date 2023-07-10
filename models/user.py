#!/usr/bin/python3
"""
This module holds a class User
"""

from models.base_model import BaseModel


class User(BaseModel):
    """
    Implemenatating  the class User
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
