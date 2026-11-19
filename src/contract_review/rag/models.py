from dataclasses import dataclass


@dataclass(frozen=True)
class Page:
    text: str
    source: str
    location: str


@dataclass(frozen=True)
class Chunk:
    id: str
    text: str
    source: str
    location: str


@dataclass(frozen=True)
class RetrievedChunk:
    text: str
    source: str
    location: str
    distance: float
