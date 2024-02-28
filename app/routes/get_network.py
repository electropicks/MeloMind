import numpy as np
from fastapi import APIRouter
from tensorflow.keras.callbacks import EarlyStopping, LearningRateScheduler
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers.legacy import Adam
from tensorflow.keras.regularizers import l2

router = APIRouter()


def get_network(x_train, y_train, x_val, y_val):
    input_shape = x_train.shape[1]
    num_classes = y_train.shape[1]

    model = create_model(input_shape, num_classes)
    compile_model(model, num_classes)
    history = train_model(model, x_train, y_train, x_val, y_val)

    network_response = {
        "validation_loss": history.history['val_loss'][-1],
        "validation_accuracy": history.history['val_accuracy'][-1]
    }
    return network_response


def create_model(input_shape, num_classes):
    model = Sequential([
        Dense(64, activation='relu', kernel_regularizer=l2(0.001), input_shape=(input_shape,)),
        BatchNormalization(),
        Dropout(0.1),
        Dense(128, activation='relu', kernel_regularizer=l2(0.001)),
        BatchNormalization(),
        Dropout(0.1),
        Dense(64, activation='relu', kernel_regularizer=l2(0.001)),
        BatchNormalization(),
        Dense(num_classes, activation='softmax' if num_classes > 2 else 'sigmoid')
    ])
    return model


def compile_model(model, num_classes):
    model.compile(
        optimizer=Adam(learning_rate=0.0001),
        loss='categorical_crossentropy' if num_classes > 2 else 'binary_crossentropy',
        metrics=['accuracy']
    )


def step_decay(epoch):
    initial_lr = 0.0001
    drop = 0.5
    epochs_drop = 10.0
    lr = initial_lr * (drop ** np.floor((1 + epoch) / epochs_drop))
    return lr


def train_model(model, x_train, y_train, x_val, y_val, epochs=100,
                batch_size=64):
    early_stopping = EarlyStopping(monitor='val_loss', patience=15, verbose=1, mode='min', restore_best_weights=True)
    lr_scheduler = LearningRateScheduler(step_decay)

    history = model.fit(
        x_train, y_train,
        validation_data=(x_val, y_val),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=[early_stopping, lr_scheduler]
    )
    return history
