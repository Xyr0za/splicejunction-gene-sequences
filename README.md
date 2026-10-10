# DNA Splicing Prediction using Deep Learning

In genomics, splice junctions are points on a DNA sequence wherein "superfluous" DNA is removed during the process of protein creation. This project aims to accurately classify DNA sequences into three categories (Intron-Exon boundaries, Exon-Intron boundaries, or neither) using the [Splice Junction Gene Sequences dataset](https://www.kaggle.com/datasets/muhammetvarl/splicejunction-gene-sequences-dataset/). 


For the full code, please refer to splicing.ipynb.


![performance of model over epochs](fma.png)

# Dataset

| Base | A1 | A2 | A3 |
| - | - | - | - |
| A | 1 | 0 | 0 |
| C | 0 | 1 | 0 |
| G | 0 | 0 | 1 |
| T | 0 | 0 | 0 |

The dataset is in the form of 180 A_n x entries, where every 3 entries code for a single base.
The table of this encoding is shown below.

| Row | A0 | A1 | A2 | A3 | A4 | A5 | ... | A175 | A176 | A177 | A178 | A179 | class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 0 | 0 | 0 | 0 | ... | 0 | 1 | 1 | 0 | 0 | 3 |
| 1 | 0 | 0 | 1 | 0 | 0 | 1 | ... | 0 | 0 | 0 | 1 | 0 | 3 |
| 2 | 0 | 0 | 1 | 0 | 0 | 1 | ... | 0 | 1 | 0 | 0 | 1 | 3 |
| 3 | 0 | 0 | 0 | 0 | 0 | 0 | ... | 0 | 1 | 0 | 0 | 1 | 1 |
| 4 | 0 | 1 | 0 | 0 | 0 | 0 | ... | 1 | 0 | 1 | 0 | 0 | 2 |

![distribution of 1,2,3 class identifiers](dist.png)


# Running Predictions


```py
import tensorflow as tf

from splice_tils import splice_tils as st
from splice_tils import CLASSIFICATIONS

my_model = tf.keras.models.load_model('splicing.keras')



import random

rb = lambda : random.choice(['A', 'C', 'G', 'T'])

ex_string = ''.join([rb() for _ in range(60)])

converted = st.encode_sequence(ex_string)
prediction = int(st.prediction(my_model, converted)[0])

print(f"Random DNA sequence: {ex_string}")
print(f"Predicted class: {prediction}")

print(f"Meaning: {CLASSIFICATIONS[prediction]}")
```

Codebase consists of two functions, *"prediction"* and *"encode_sequence"*. 
Pseudocode representations are below.

```
fn prediction(model, input_data):
    Runs a pre-trained Keras model on a list of numbers, applying the required preprocessing.
    
    args:
        model: A loaded Keras model.
        input_data: A list of 180 numbers (single sample) OR a list of lists (multiple samples).

    input: A list of 180 ints (0,1) (single sample) OR a list of lists (multiple samples).
    output: int or list of ints [0,1,2]
```

```
fn encode_sequence(sequence):
        Converts a string of 60 bases into a list of 180 numbers, applying the required preprocessing.
        
        args:
            sequence: A string of 60 characters representing nucleotide bases (A, C, G, T).

        input: A string of 60 bases.
        output: A list of 180 ints (0,1).
```

