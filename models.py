from dataclasses import dataclass


@dataclass
class StandardRule:

    id: str
    section: str
    title: str
    severity: str
    standard: str