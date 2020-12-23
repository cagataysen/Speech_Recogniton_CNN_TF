import librosa
import tensorflow as tf
import numpy as np

SAVED_MODEL_PATH = "_actions.h5"
SAMPLES_TO_CONSIDER = 22050

class _Predict_Number:

    model = None
    _mapping = [
        "four",
        "one",
        "three",
        "two",
        "zero"
    ]

    _instance = None

    def predict(self, file_path):

        # extract MFCC
        MFCCs = self.preprocess(file_path)

        # we need a 4-dim array to feed to the model for prediction: (# samples, # time steps, # coefficients, 1)
        MFCCs = MFCCs[np.newaxis, ..., np.newaxis]

        # get the predicted label
        predictions = self.model.predict(MFCCs)
        predicted_index = np.argmax(predictions)
        predicted_keyword = self._mapping[predicted_index]
        return predicted_keyword


    def preprocess(self, file_path, num_mfcc=13, n_fft=2048, hop_length=512):

        # load audio file
        signal, sample_rate = librosa.load(file_path)

        if len(signal) >= SAMPLES_TO_CONSIDER:
            # ensure consistency of the length of the signal
            signal = signal[:SAMPLES_TO_CONSIDER]

            # extract MFCCs
        MFCCs = librosa.feature.mfcc(signal, sample_rate, n_mfcc=num_mfcc, n_fft=n_fft,
                                    hop_length=hop_length)
        return MFCCs.T


def Predict_Number():

    # ensure an instance is created only the first time the factory function is called
    if _Predict_Number._instance is None:
        _Predict_Number._instance = _Predict_Number()
        _Predict_Number.model = tf.keras.models.load_model(SAVED_MODEL_PATH)
    return _Predict_Number._instance

if __name__ == "__main__":
  kss = Predict_Number()

  word1 = kss.predict("Test_Dataset/four/a6285644_nohash_2.wav")
  word2 = kss.predict("Test_Dataset/three/bdee441c_nohash_3.wav")

  print(f"Predicted keywords: {word1}, {word2}")