from dataclasses import dataclass

# @dataclass is a decorator that automatically generates special methods like __init__(), __repr__(), and __eq__() 
# for the class based on its attributes. This makes it easier to create classes that are primarily used to store data.
# dataclass is a Python feature that makes it easier to create classes whose main purpose is to store structured data.
@dataclass
class StandardRule:

    id: str
    section: str
    title: str
    severity: str
    standard: str