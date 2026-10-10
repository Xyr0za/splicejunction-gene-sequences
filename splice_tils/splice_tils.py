import numpy as np
import tensorflow as tf


class splice_tils:
    def __init__(self, model_path):
        pass

    @staticmethod
    def encode_sequence(sequence):
        """
        Converts a string of 60 bases into a list of 180 numbers, applying the required preprocessing.
        
        Args:
            sequence: A string of 60 characters representing nucleotide bases (A, C, G, T).

        input: A string of 60 bases.
        output: A list of 180 ints (0,1).

        Base    A1  A2  A3
        A       1   0   0
        C       0   1   0
        G       0   0   1
        T       0   0   0
        """
        mapping = {
            'A': [1, 0, 0],
            'C': [0, 1, 0],
            'G': [0, 0, 1],
            'T': [0, 0, 0]
        }
        
        result = []
        for base in sequence:
            # Defaults to [0, 0, 0] if an unexpected character is found
            result.extend(mapping.get(base.upper(), [0, 0, 0]))
            
        return result

    @staticmethod
    def prediction(model, input_data):
        """
        Runs a pre-trained Keras model on a list of numbers, applying the required preprocessing.
        
        Args:
            model: A loaded Keras model.
            input_data: A list of 180 numbers (single sample) OR a list of lists (multiple samples).

        input: A list of 180 ints (0,1) (single sample) OR a list of lists (multiple samples).
        output: int or list of ints [0,1,2]

        Base    A1  A2  A3
        A       1   0   0
        C       0   1   0
        G       0   0   1
        T       0   0   0
        """

        print(np.ndim(input_data))
        if np.ndim(input_data) > 1:
            return [int(splice_tils.prediction(model, i)[0]) for i in input_data]

        X_r = np.array(input_data, dtype=float)
        

        if X_r.ndim == 1:
            X_r = X_r.reshape(1, -1)


        assert X_r.ndim == 2, "Input data must be a 1D or 2D array."
        assert X_r.shape[1] == 180, f"Expected 180 features per sample, but got {X_r.shape[1]}"

        X_g = X_r.reshape(-1, 60, 3)
        X_c = np.dot(X_g, [1, 2, 3])
        
        pred_val = np.argmax(model.predict(X_c, verbose=0), axis=1)

        print("Prediction:", pred_val)
        assert pred_val in (0,1,2), "Prediction must be one of 0, 1, or 2."
        
        return pred_val