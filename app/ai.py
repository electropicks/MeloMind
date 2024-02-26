from concurrent.futures import ThreadPoolExecutor, as_completed
from enum import Enum

import pandas as pd


class Genre(Enum):
    AcousticFolk = 0
    Alternative = 1
    Blues = 2
    Bollywood = 3
    Country = 4
    HipHop = 5
    IndieAlt = 6
    Instrumental = 7
    Metal = 8
    Pop = 9
    Rock = 10


def process_chunk(chunk):
    # Define your preprocessing here, for example:
    # chunk['processed_lyrics'] = chunk['lyrics'].apply(some_preprocessing_function)
    return chunk


def read_and_process_csv_in_chunks(file_path, chunksize=10000):
    chunks = []
    with ThreadPoolExecutor() as executor:
        futures = []
        for chunk in pd.read_csv(file_path, chunksize=chunksize, low_memory=True, memory_map=True, on_bad_lines='skip'):
            futures.append(executor.submit(process_chunk, chunk))
        for future in as_completed(futures):
            chunks.append(future.result())
    return pd.concat(chunks)


# Load the datasets
columns = ['Artist Name', 'Track Name', 'Popularity', 'danceability', 'energy',
           'key', 'loudness', 'mode', 'speechiness', 'acousticness',
           'instrumentalness', 'liveness', 'valence', 'tempo',
           'duration_in min/ms', 'time_signature', 'Class']
train_df = pd.read_csv('datasets/Music Genre Classification/train.csv')
test_df = pd.read_csv('datasets/Music Genre Classification/test.csv')
lyrics_df = pd.read_csv('datasets/song_lyrics.csv', memory_map=True, engine='c', on_bad_lines='skip')
try:
    lyrics_df = pd.read_pickle('lyrics.pkl')
except (OSError, IOError) as e:
    lyrics_df = read_and_process_csv_in_chunks('datasets/song_lyrics.csv')
    lyrics_df.to_pickle('lyrics.pkl')

print(lyrics_df['song'])
for song in train_df['Track Name']:
    print(song) if song in lyrics_df['song'] else None

print(lyrics_df)
