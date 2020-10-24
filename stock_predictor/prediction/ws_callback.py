import numpy as np
import tensorflow as tf


class WebsocketCallback(tf.keras.callbacks.Callback):

    def __init__(self, progress_callback, end_callback):
        super().__init__()
        self.progress_callback = progress_callback
        self.end_callback = end_callback

    def on_epoch_end(self, epoch, logs=None):
        progress = float(epoch) / 100
        self.progress_callback(progress)

    def on_train_end(self, logs=None):
        self.end_callback()
