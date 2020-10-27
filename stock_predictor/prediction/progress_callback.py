import tensorflow as tf


class ProgressCallback(tf.keras.callbacks.Callback):

    def __init__(self, callback):
        self.callback = callback

    def on_epoch_begin(self, epoch, logs=None):
        self.callback(epoch)