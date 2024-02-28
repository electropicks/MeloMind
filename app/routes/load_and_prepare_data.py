import numpy as np
from fastapi import APIRouter
from tensorflow.keras.utils import to_categorical

from app.parsing import get_dataframes

router = APIRouter()


@router.get("/load_and_prepare_data")
def load_and_prepare_data():
    train_df, test_df, _ = get_dataframes(lyrics_df=False)

    # Drop 'Artist Name' and 'Track Name' columns
    train_df = train_df.drop(columns=['Artist Name', 'Track Name'])
    test_df = test_df.drop(columns=['Artist Name', 'Track Name'])

    train_df = train_df.dropna()
    test_df = test_df.dropna()

    # Separate features and labels for the training data
    x_train = train_df.drop(columns=['Class']).values
    y_train = to_categorical(train_df['Class'].values)


    # Prepare the test features
    x_test = test_df.values

    # Normalize features
    mean = np.mean(x_train, axis=0)
    std = np.std(x_train, axis=0)
    x_train_normalized = (x_train - mean) / std
    x_test_normalized = (x_test - mean) / std

    # Split training data into training and validation sets
    split_size = int(len(x_train_normalized) * 0.8)
    indices = np.arange(len(x_train_normalized))
    np.random.shuffle(indices)

    x_train_split = x_train_normalized[indices[:split_size]]
    y_train_split = y_train[indices[:split_size]]
    x_val_split = x_train_normalized[indices[split_size:]]
    y_val_split = y_train[indices[split_size:]]

    return {
        "message": "Data loaded and prepared successfully",
        "x_train": x_train_split.tolist(),
        "y_train": y_train_split.tolist(),
        "x_val": x_val_split.tolist(),
        "y_val": y_val_split.tolist(),
        "x_test": x_test_normalized.tolist()
    }
