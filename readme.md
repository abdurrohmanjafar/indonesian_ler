# Source Code for Named Entity Recognition on Indonesian Legal Documents Research Paper
By:
* Naradhipa Mahardhika Setiawan Bhary
* Jafar Abdurrohman
* Fariz Wahyuzan Dwitilas

### Content
Source code for data processing, analysis, preprocessing, and model training for our research in the `notebook` folder.
We also include the best model from every experiment.

### Usage
#### Deep Learning Model Training
Use the ```notebook/unified-DL-train.ipynb``` notebook to train deep learning based model. To adjust model parameter you can change these variables:
* EPOCHS: Number of passes through entire dataset `[2, 4, 8, 16]`
* EMBEDDING: Dimension of word embedding vector `[100, 200, 500]`
* MAX_LEN: Max length of review (in words) `[128, 256, 512]`
* STRIDE: The number of overlap between chunked input `[0, 10%, 25%, 50%]`

The notebook uses Tensorflow library to train BiLSTM and BiLSTM-CRF model.

#### Language Model Finetuning
Use the ```notebook/unified-LM-finetuning.ipynb``` notebook to finetune a language model for the LER task. To adjust model parameter you can change these variables:
* MODEL_NAME: The LM to use as the base for finetuning `["xlm-roberta-large", "xlm-roberta-base", "bert-base-multilingual-uncased", "indobenchmark/indobert-base-p1", "indobenchmark/indobert-large-p1", "flax-community/indonesian-roberta-base"]`
* STRIDE: The number of overlap between chunked input `[0, 10%, 25%, 50%]`
* SEQ_LEN: Max length of each input (in token) `[128, 256, 512]`
* EPOCH: Number of passes through entire dataset `[2, 4, 8, 16]`
* LEARNING_RATE: The size at each iteration while moving toward the optimal solution `[2e-5, 3e-5, 5e-5]`