import csv
import typing
from dataclasses import dataclass, field


@dataclass
class DatasetSong:
    title: str
    tag: str
    artist: str
    year: int
    views: int
    features: typing.List[str] = field(default_factory=list)
    lyrics: str = ''
    id: str = ''
    language_cld3: str = ''
    language_ft: str = ''
    language: str = ''


def parse_features(features_str: str) -> typing.List[str]:
    # Implement a method to parse the features from the string representation
    # This is a placeholder implementation
    return features_str.strip("{}").replace('"', '').split(',')


def load_songs_from_csv(filepath: str, limit: typing.Optional[int] = None) -> typing.List[DatasetSong]:
    songs = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader):
            if limit is not None and idx >= limit:
                break  # Stop reading once the limit is reached
            song = DatasetSong(
                title=row['title'].strip(),
                tag=row['tag'].strip(),
                artist=row['artist'].strip(),
                year=int(row['year']),
                views=int(row['views']),
            )
            songs.append(song)
    return songs
