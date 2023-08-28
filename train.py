from v2enlib import config, GSQLClass

import tensorflow as tf, pandas as pd, tensorflow_model_optimization as tfmot
import os, math


class V2ENLanguageModel:
    class Language:
        def __init__(self, sentences, tokenizer) -> None:
            self.sentences = tokenizer.texts_to_sequences(sentences)

    @staticmethod
    def lr_schedule(epoch, lr):
        return lr if epoch < 10 else lr * math.exp(-0.1)

    def initTokenizer(self) -> None:
        self.tokenizer = tf.keras.preprocessing.text.Tokenizer()
        self.tokenizer.fit_on_texts(
            [
                str(e)
                for e in [
                    GSQLClass(config.v2en.sheet, f"dictionary_{i}").getAll()
                    for i in ["vi", "en"]
                ]
            ]
        )

    def importData(self) -> None:
        self.initTokenizer()
        data = GSQLClass(config.v2en.sheet, config.v2en.worksheet).getAll()
        df = pd.DataFrame(data[1:], columns=data[0])
        self.source = self.Language(df["English"].tolist(), self.tokenizer)
        self.target = self.Language(df["Vietnamese"].tolist(), self.tokenizer)

    def syncData(self) -> None:
        self.max_len = max(
            len(seq) for seq in self.source.sentences + self.target.sentences
        )
        self.source.sentences = tf.keras.preprocessing.sequence.pad_sequences(
            self.source.sentences, maxlen=self.max_len
        )
        self.target.sentences = tf.keras.preprocessing.sequence.pad_sequences(
            self.target.sentences, maxlen=self.max_len
        )
        self.dataset = tf.data.Dataset.from_tensor_slices(
            (self.source.sentences, self.target.sentences)
        )

    def initModel(self):
        # Config Hyperparameters
        latent_dim = 128
        layers = tf.keras.layers

        # Build the layers
        model = tf.keras.models.Sequential()
        # Embedding
        model.add(
            layers.Embedding(
                len(self.tokenizer.word_index),
                latent_dim,
                input_length=self.max_len,
                input_shape=self.max_len,
            )
        )
        # Encoder
        model.add(layers.Bidirectional(layers.LSTM(latent_dim)))
        model.add(layers.RepeatVector(self.max_len))
        # Decoder
        model.add(layers.Bidirectional(layers.LSTM(latent_dim, return_sequences=True)))
        model.add(
            layers.TimeDistributed(layers.Dense(latent_dim * 4, activation="relu"))
        )
        model.add(layers.Dropout(0.5))
        model.add(
            layers.TimeDistributed(
                layers.Dense(len(self.tokenizer.word_index), activation="softmax")
            )
        )

        model.compile(
            loss=tf.keras.losses.SparseCategoricalCrossentropy(),
            optimizer=tf.keras.optimizers.Adam(
                learning_rate=config.training.learning_rate * 10
            ),
            metrics=["accuracy"],
        )

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
        ]

    def fitModel(self) -> None:
        self.model.summary()
        batch_size = 475
        self.model.fit(
            self.dataset,
            batch_size=batch_size,
            epochs=50,
            validation_split=0.2,
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
