from v2enlib import GSQLClass, utils
from config import config
from tensorflow.python.framework.errors_impl import *
import tensorflow as tf
import pandas as pd
import random
import tensorflow_model_optimization as tfmot
import os
import keras


class V2ENLanguageModel:
    class PrintLearningRateCallback(tf.keras.callbacks.Callback):
        def __init__(self, source, target, tokenizer_items):
            self.target = target
            self.source = source
            self.tokenizer_items = tokenizer_items

        def logits_to_text(self, logits):
            index_to_words = {id: word for word, id in self.tokenizer_items}
            return " ".join(
                [index_to_words[prediction] for prediction in logits if prediction != 0]
            )

        def generateText(self) -> str:
            ran_num = random.randrange(0, len(self.target._sentences))
            return "\t" + "\n\t".join(
                [
                    self.logits_to_text(
                        tf.argmax(
                            self.model.predict(
                                self.source.sentences[ran_num : ran_num + 1]
                            )[0],
                            axis=1,
                        ).numpy()
                    ),
                    self.logits_to_text(self.target._sentences[ran_num]),
                    self.logits_to_text(self.source._sentences[ran_num]),
                ]
            )

        def on_epoch_end(self, epoch, logs=None):
            print(f"Prediction after epoch {epoch + 1}\n {self.generateText()}")

    class Language:
        def __init__(
            self, lang: str, df, tk: tf.keras.preprocessing.text.Tokenizer
        ) -> None:
            if config.training.data_size:
                self._sentences = tk.texts_to_sequences(
                    df[lang].tolist()[: config.training.data_size]
                )
            else:
                self._sentences = tk.texts_to_sequences(df[lang].tolist())
            self.sentences = tf.keras.utils.pad_sequences(
                self._sentences, padding="post", maxlen=config.training.sent_len
            )

        def reshape(self):
            self.sentences.reshape(*self.sentences.shape, 1)

    class LanguageAccuracy(keras.metrics.Metric):
        def __init__(self, name="languageAccuracy", **kwargs):
            super(V2ENLanguageModel.LanguageAccuracy, self).__init__(
                name=name, **kwargs
            )
            self.custom_metric_values = self.add_weight(
                name="each_accuracy", initializer="zeros"
            )
            self.values_len = self.add_weight(name="len", initializer="zeros")

        def update_state(self, y_true, y_pred, sample_weight=None):
            y_true = tf.cast(y_true, tf.int64)
            y_pred = tf.argmax(y_pred, axis=2)

            y_pred = tf.boolean_mask(y_pred, tf.not_equal(y_true, 0))
            y_true = tf.boolean_mask(y_true, tf.not_equal(y_true, 0))

            acur = tf.reduce_mean(tf.cast(tf.equal(y_true, y_pred), tf.float32))
            self.custom_metric_values.assign_add(acur)
            self.values_len.assign_add(1)

        def result(self):
            return self.custom_metric_values / self.values_len

        def reset_state(self):
            self.custom_metric_values.assign(0.0)
            self.values_len.assign(0.0)

    @staticmethod
    def LanguageLoss(y_true, y_pred):
        return tf.nn.sparse_softmax_cross_entropy_with_logits(
            labels=y_true, logits=y_pred
        )

    def importData(self) -> None:
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
        latent_dim = 128
        layers = tf.keras.layers
        pruning_params = {
            "pruning_schedule": tfmot.sparsity.keras.PolynomialDecay(
                initial_sparsity=config.training.initial_sparsity,
                final_sparsity=config.training.final_sparsity,
                begin_step=config.training.begin_step,
                end_step=10**6,
            ),
        }

        # Build the layers
        model = tf.keras.models.Sequential()
        # Embedding
        pruneEmbedding = tfmot.sparsity.keras.prune_low_magnitude(
            layers.Embedding(
                len(self.tokenizer.word_index) + 1,
                latent_dim,
                input_length=self.source.sentences.shape[1],
                input_shape=self.source.sentences.shape[1:],
            ),
            **pruning_params,
        )
        model.add(pruneEmbedding)
        # Encoder
        model.add(layers.Bidirectional(layers.GRU(latent_dim)))
        model.add(layers.RepeatVector(config.training.sent_len))
        # Decoder
        model.add(layers.Bidirectional(layers.GRU(latent_dim, return_sequences=True)))
        model.add(
            layers.TimeDistributed(layers.Dense(latent_dim * 4, activation="relu"))
        )
        model.add(layers.Dropout(0.5))
        model.add(
            layers.TimeDistributed(
                layers.Dense(len(self.tokenizer.word_index) + 1, activation="softmax")
            )
        )

        try:
            utils.Terminal.cleanScreen()
            with keras.saving.custom_object_scope(
                {
                    "LanguageAccuracy": self.LanguageAccuracy,
                    "PruneLowMagnitude": pruneEmbedding,
                    # "LanguageLoss": self.LanguageLoss,
                }
            ):
                self.model = tf.keras.models.load_model(
                    f"{config.training.checkpoint_path}_{config.training.sent_len}.{config.training.extension}"
                )
            self.fitModel()
        except Exception as e:
            utils.Terminal.cleanScreen()
            print("Using blank model!")
            utils.debuger.printError(self.initModel.__name__, e)
            self.model = model
            self.fitModel()

    def initCallbacks(self) -> None:
        checkpoint = tf.keras.callbacks.ModelCheckpoint(
            f"{config.training.checkpoint_path}_{config.training.sent_len}.{config.training.extension}",
            mode="max",
            monitor="val_languageAccuracy",
            verbose=2,
            save_best_only=True,
        )
        earlystop_accuracy = tf.keras.callbacks.EarlyStopping(
            monitor="val_languageAccuracy",
            patience=divmod(config.training.num_epochs, 3)[0],
            verbose=1,
            mode="max",
        )
        earlystop_loss = tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=divmod(config.training.num_epochs, 3)[0],
            verbose=1,
            mode="min",
        )
        update_pruning = tfmot.sparsity.keras.UpdatePruningStep()
        check_pred = self.PrintLearningRateCallback(
            self.source,
            self.target,
            self.tokenizer.word_index.items(),
        )
        self.callbacks = [
            update_pruning,
            #check_pred,
            checkpoint,
            earlystop_accuracy,
            earlystop_loss,
        ]

    def fitModel(self) -> None:
        self.model.compile(
            loss=tf.keras.losses.sparse_categorical_crossentropy,
            optimizer=tf.keras.optimizers.Adam(
                learning_rate=config.training.learning_rate
            ),
            metrics=[self.LanguageAccuracy()],
            run_eagerly=config.training.eagerly,
        )
        self.initCallbacks()
        self.model.summary()
        try:
            self.model.fit(
                self.source.sentences,
                self.target.sentences,
                validation_split=config.training.validation_split,
                batch_size=config.training.batch_size,
                epochs=config.training.num_epochs,
                callbacks=self.callbacks,
            )
        except ResourceExhaustedError as e:
            utils.debuger.printError(self.fitModel.__name__, e)

    def __init__(self) -> None:
        os.makedirs("models", exist_ok=True)
        os.environ["TF_GPU_ALLOCATOR"] = "cuda_malloc_async"
        os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"
        if config.training.use_cpu:
            tf.config.set_visible_devices([], "GPU")
        elif gpus := tf.config.list_physical_devices("GPU"):
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(enable=True, device=gpu)
        else:
            print("test is only applicable on GPU")
            exit(0)

        for _ in range(config.training.num_train):
            self.importData()
            self.initModel()
            config.reset()


if __name__ == "__main__":
    V2ENLanguageModel()
