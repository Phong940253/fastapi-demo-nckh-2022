
from tensorflow.keras.layers import LSTM, Dense, Embedding, Input, concatenate, Flatten, Dropout
from tensorflow.keras import Model
from tensorflow.keras import backend as K
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.preprocessing.sequence import pad_sequences


def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall


def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision


def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2 * ((precision * recall) / (precision + recall + K.epsilon()))


def get_model():
    input_layer1 = Input(2121, name="Poster")
    # input_layer2 = Input(191,name="Pre-Comment")
    input_layer3 = Input(607, name="Comments")
    concat_layer_1 = concatenate([input_layer1, input_layer3])
    embedding_layer = Embedding(
        50000, 10, name="embedding_poster")(concat_layer_1)
    lstm_layer_1 = LSTM(
        512,
        return_sequences=True,
        go_backwards=True)(embedding_layer)
    dense_layer_1 = Dense(256, activation='relu')(lstm_layer_1)
    dropout1 = Dropout(0.25)(dense_layer_1)
    lstm_layer_2 = LSTM(
        128,
        return_sequences=True,
        go_backwards=True)(dropout1)
    dense_layer_2 = Dense(128, activation='relu')(dense_layer_1)
    dropout2 = Dropout(0.25)(dense_layer_2)
    flat_layer = Flatten()(dropout2)
    dense_layer_3 = Dense(64, activation='relu')(flat_layer)
    output_layer = Dense(1, activation='sigmoid', name="output")(dense_layer_3)
    model = Model(
        inputs=[input_layer1, input_layer3],
        outputs=[output_layer],
    )

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=[
            'acc',
            f1_m,
            precision_m,
            recall_m])

    return model


def padding_data(data):
    print(len(data))
    encoded_posters = [one_hot(d, 50000) for d in data['Poster']]
    # encoded_pre_comment = [one_hot(p,50000) for p in data['Pre-Comment'].values]
    encoded_comments = [one_hot(c, 50000) for c in data['Comment']]
    padded_posters = pad_sequences(
        encoded_posters, maxlen=2121, padding='post')
    # padded_pre_comment = pad_sequences(encoded_pre_comment,maxlen=191,padding='post')
    padded_comments = pad_sequences(
        encoded_comments, maxlen=607, padding='post')
    return padded_posters, padded_comments
