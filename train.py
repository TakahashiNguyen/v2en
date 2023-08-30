from v2enlib import GSQLClass
from config import config

import tensorflow as tf, pandas as pd, tensorflow_model_optimization as tfmot
import os, math


class V2ENLanguageModel:
    class Language:
        def __init__(self, lang: str, df) -> None:
            self.tokenizer = tf.keras.preprocessing.text.Tokenizer(
                filters="", lower=False
            )
            sheet = GSQLClass(config.v2en.sheet, f"dictionary_{lang}")
            self.tokenizer.fit_on_texts(sheet.getAll())
            self.sentences = self.tokenizer.texts_to_sequences(df[lang].tolist())
            self.sentences = tf.keras.utils.pad_sequences(
                self.sentences, padding="post"
            )

        def reshape(self):
            self.sentences.reshape(*self.sentences.shape, 1)

    @staticmethod
    def lr_schedule(epoch, lr):
        return lr if epoch < 10 else lr * math.exp(-0.1)

    def importData(self) -> None:
        data = GSQLClass(config.v2en.sheet, config.v2en.worksheet).getAll()
        df = pd.DataFrame(data[1:], columns=data[0])
        self.source = self.Language(config.v2en.flang, df)
        self.target = self.Language(config.v2en.slang, df)

    def syncData(self) -> None:
        self.target.reshape()

    def initModel(self):
        latent_dim = 256
        layers = tf.keras.layers

        modelInput = tf.keras.utils.pad_sequences(
            self.source.sentences, self.target.sentences.shape[1]
        )
        modelInput.reshape((-1, self.target.sentences.shape[-2]))

        # Build the layers
        model = tf.keras.models.Sequential()
        # Embedding
        model.add(
            layers.Embedding(
                len(self.source.tokenizer.word_index) + 1,
                latent_dim,
                input_length=modelInput.shape[1],
                input_shape=modelInput.shape[1:],
            )
        )
        # Encoder
        model.add(layers.Bidirectional(layers.LSTM(latent_dim, return_sequences=True)))
        model.add(layers.Bidirectional(layers.LSTM(latent_dim)))
        model.add(layers.RepeatVector(self.target.sentences.shape[1]))
        # Decoder
        model.add(layers.Bidirectional(layers.LSTM(latent_dim, return_sequences=True)))
        model.add(
            layers.TimeDistributed(layers.Dense(latent_dim * 4, activation="relu"))
        )
        model.add(layers.Dropout(0.5))
        model.add(
            layers.TimeDistributed(
                layers.Dense(
                    len(self.target.tokenizer.word_index) + 1, activation="softmax"
                )
            )
        )

        model.compile(
            loss=tf.keras.losses.SparseCategoricalCrossentropy(),
            optimizer=tf.keras.optimizers.Adam(
                learning_rate=config.training.learning_rate * 10
            ),
            metrics=["accuracy"],
        )

        self.modelInput = modelInput
        self.model = model

    def initCallbacks(self) -> None:
        checkpoint = tf.keras.callbacks.ModelCheckpoint(
            config.training.checkpoint_path,
            save_best_only=True,
            save_weights_only=True,
            verbose=1,
            monitor="val_accuracy",
            mode="max",
        )
        earlystop_accuracy = tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy", patience=30, verbose=1, mode="max"
        )
        earlystop_loss = tf.keras.callbacks.EarlyStopping(
            monitor="val_loss", patience=30, verbose=1, mode="min"
        )
        update_pruning = tfmot.sparsity.keras.UpdatePruningStep()
        self.callbacks = [
            checkpoint,
            earlystop_accuracy,
            earlystop_loss,
            tf.keras.callbacks.LearningRateScheduler(self.lr_schedule),
            update_pruning,
        ]

    def fitModel(self) -> None:
        self.initCallbacks()
        self.model.summary()
        batch_size = 475
        self.model.fit(
            self.modelInput,
            self.target.sentences,
            batch_size=batch_size,
            epochs=50,
            callbacks=self.callbacks,
            use_multiprocessing=True,
        )

    def __init__(self) -> None:
        self.config = config

        os.makedirs("models", exist_ok=True)

        gpus = tf.config.list_physical_devices("GPU")
        if len(gpus) == 0:
            print("test is only applicable on GPU")
            exit(0)
        os.environ["TF_GPU_ALLOCATOR"] = "cuda_malloc_async"

        self.importData()
        self.syncData()
        self.initModel()
        self.fitModel()


if __name__ == "__main__":
    V2ENLanguageModel()
