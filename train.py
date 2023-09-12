from v2enlib import GSQLClass, utils
from config import config
from tensorflow.python.keras import mixed_precision

import tensorflow as tf, pandas as pd, tensorflow_model_optimization as tfmot
from tensorflow.python.framework.errors_impl import *
import os, numpy as np, math, random


class V2ENLanguageModel:
    class PrintLearningRateCallback(tf.keras.callbacks.Callback):
        def __init__(self, source, target_sentences, tokenizer_items):
            self.target_sentences = target_sentences
            self.source = source
            self.tokenizer_items = tokenizer_items

        def logits_to_text(self, logits):
            index_to_words = {id: word for word, id in self.tokenizer_items}

            return " ".join(
                [index_to_words[prediction] for prediction in logits if prediction != 0]
            )

        def generateText(self) -> str:
            ran_num = random.randrange(0, len(self.target_sentences))
            return "\t" + "\n\t".join(
                [
                    self.logits_to_text(
                        np.argmax(
                            self.model.predict(
                                self.source.sentences[ran_num : ran_num + 1]
                            )[0],
                            1,
                        )
                    ),
                    self.logits_to_text(self.target_sentences[ran_num]),
                    self.logits_to_text(self.source._sentences[ran_num]),
                ]
            )

        def on_epoch_end(self, epoch, logs=None):
            print(f"Prediction after epoch {epoch + 1}\n {self.generateText()}")

    class Language:
        def __init__(
            self, lang: str, df, tk: tf.keras.preprocessing.text.Tokenizer
        ) -> None:
            self._sentences = tk.texts_to_sequences(df[lang].tolist())
            self.sentences = tf.keras.utils.pad_sequences(
                self._sentences, padding="post", maxlen=config.training.sent_len
            )

        def reshape(self):
            self.sentences.reshape(*self.sentences.shape, 1)

    def importData(self) -> None:
        if config.training.data_size:
            data = GSQLClass(config.v2en.sheet, config.v2en.worksheet).getAll()[
                : config.training.data_size
            ]
        else:
            data = GSQLClass(config.v2en.sheet, config.v2en.worksheet).getAll()
        df = pd.DataFrame(data[1:], columns=data[0])

        self.tokenizer = tf.keras.preprocessing.text.Tokenizer(filters="", lower=False)
        sheet = GSQLClass(config.v2en.sheet, "dictionary")
        self.tokenizer.fit_on_texts(sheet.getAll())
        df = df.sample(frac=1).reset_index(drop=True)

        self.source = self.Language(config.v2en.flang, df, self.tokenizer)
        self.target = self.Language(config.v2en.slang, df, self.tokenizer)

        self.target.reshape()

    def initModel(self):
        latent_dim = 256
        layers = tf.keras.layers

        # Build the layers
        model = tf.keras.models.Sequential()
        # Embedding
        model.add(
            layers.Embedding(
                len(self.tokenizer.word_index) + 1,
                latent_dim,
                input_length=self.source.sentences.shape[1],
                input_shape=self.source.sentences.shape[1:],
            )
        )
        # Encoder
        model.add(layers.Bidirectional(layers.LSTM(latent_dim, return_sequences=True)))
        model.add(layers.Bidirectional(layers.LSTM(latent_dim)))
        model.add(layers.RepeatVector(config.training.sent_len))
        # Decoder
        model.add(layers.Bidirectional(layers.LSTM(latent_dim, return_sequences=True)))
        model.add(
            layers.TimeDistributed(layers.Dense(latent_dim * 4, activation="relu"))
        )
        model.add(layers.Dropout(0.5))
        model.add(
            layers.TimeDistributed(
                layers.Dense(len(self.tokenizer.word_index) + 1, activation="softmax")
            )
        )

        model.compile(
            loss=tf.keras.losses.SparseCategoricalCrossentropy(),
            optimizer=tf.keras.optimizers.Adam(
                learning_rate=config.training.learning_rate
            ),
            metrics=['accuracy'],
        )

        try:
            self.model = tf.keras.models.load_model(config.training.checkpoint_path)
            self.fitModel()
        except Exception as e:
            utils.debuger.printError(self.initModel.__name__, e)
            self.model = model
            self.fitModel()

    def initCallbacks(self) -> None:
        checkpoint = tf.keras.callbacks.ModelCheckpoint(
            config.training.checkpoint_path,
            mode="max",
            monitor="val_accuracy",
            verbose=2,
            save_best_only=True,
        )
        earlystop_accuracy = tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy", patience=30, verbose=1, mode="max"
        )
        earlystop_loss = tf.keras.callbacks.EarlyStopping(
            monitor="val_loss", patience=30, verbose=1, mode="min"
        )
        update_pruning = tfmot.sparsity.keras.UpdatePruningStep()
        self.callbacks = [
            self.PrintLearningRateCallback(
                self.source,
                self.target._sentences,
                self.tokenizer.word_index.items(),
            ),
            checkpoint,
            earlystop_accuracy,
            earlystop_loss,
            update_pruning,
        ]

    def fitModel(self) -> None:
        self.initCallbacks()
        try:
            utils.Terminal.cleanScreen()
            self.model.summary()
            self.model.fit(
                self.source.sentences,
                self.target.sentences,
                batch_size=config.training.batch_size,
                epochs=config.training.num_train,
                callbacks=self.callbacks,
                use_multiprocessing=True,
                validation_split=0.2,
            )
        except ResourceExhaustedError as e:
            utils.debuger.printError(self.fitModel.__name__, e)
            utils.Terminal.cleanScreen()
            self.model.summary()
            self.model.fit(
                self.source.sentences,
                self.target.sentences,
                batch_size=math.ceil(math.sqrt(config.training.batch_size)),
                epochs=config.training.num_train,
                callbacks=self.callbacks,
                use_multiprocessing=True,
                validation_split=0.2,
            )

    def __init__(self) -> None:
        os.makedirs("models", exist_ok=True)
        os.environ["TF_GPU_ALLOCATOR"] = "cuda_malloc_async"
        os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"
        if len(tf.config.list_physical_devices("GPU")) == 0:
            print("test is only applicable on GPU")
            exit(0)

        self.importData()
        self.initModel()


if __name__ == "__main__":
    V2ENLanguageModel()
