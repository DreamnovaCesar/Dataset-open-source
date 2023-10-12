import logging
from functools import wraps
import tensorflow as tf

import os

from typing import Optional

class GPUDetector(object):

    # * Define a custom logger for the GPU class.
    logger = logging.getLogger("GPU");
    logger.setLevel(logging.DEBUG);

    """
    A class for detecting the availability of a GPU for a function using the GPUDetector.detect_GPU method.

    This class provides a decorator that can be applied to functions to detect the presence of a GPU
    and measure the execution time of the decorated function. If a GPU is available, the function will
    be executed on the GPU, otherwise, it will run on the CPU.

    Examples:
    ---------
    >>> @GPUDetector.detect_GPU
    ... def my_func():
    ...     return tf.reduce_sum(tf.random.normal([1000, 1000]))
    ...
    >>> my_func()
    [PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
    Found GPU at: /device:GPU:0
    <tf.Tensor: shape=(), dtype=float32, numpy=-508.8744>

    >>> @GPUDetector.detect_GPU
    ... def another_func():
    ...     return tf.matmul(tf.random.normal([500, 500]), tf.random.normal([500, 500]))
    ...
    >>> another_func()
    [PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
    Found GPU at: /device:GPU:0
    <tf.Tensor: shape=(500, 500), dtype=float32, numpy=...]>

    Notes
    -----
    This class decorator uses the `functools.wraps` decorator to preserve the
    metadata of the original function, such as the function name, docstring, and
    parameter information.

    The GPU detection is based on TensorFlow's functions to list physical devices and check GPU support.
    It provides information about whether a GPU is available and its name.

    The decorator can be applied to any function that uses TensorFlow operations. It checks the presence
    of a GPU and prints the status accordingly. If a GPU is found, the function is executed on the GPU.

    """

    @staticmethod
    def detect_GPU(Folder: Optional[str] = 'Data\logs', Class_name=None):
        """
        Wrapper function that detects GPU availability and measures execution time.

        Parameters
        ----------
        func : callable
        The function to be wrapped.

        Returns
        -------
        callable
        The wrapped function that detects GPU availability and measures execution time.
        """
        def Inner(func):

            @wraps(func)
            def wrapper(*args, **kwargs):
                """
                Wrapper function that detects GPU availability and measures execution time.

                Parameters
                ----------
                args : tuple
                    Arguments to be passed to the decorated function.
                kwargs : dict
                    Keyword arguments to be passed to the decorated function.

                Returns
                -------
                Any
                    The return value of the decorated function.
                """

                Asterisk = 60;

                Log_app_name = f"{Class_name}_{func.__name__}_{__class__.__name__}.log";

                # * Create a logging handler that writes to a file.
                if(Folder is not None):
                    log_file_path = os.path.join(Folder, Log_app_name);
                
                File_handler = logging.FileHandler(log_file_path);
                File_handler.setLevel(logging.INFO);

                # * Configure the logger with a format and set the logging level to DEBUG.
                log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s';
                formatter = logging.Formatter(log_format);
                File_handler.setFormatter(formatter);
                
                # * Add the file handler to the Timer class logger.
                GPUDetector.logger.addHandler(File_handler);

                GPUDetector.logger.info("Detecting GPU availability...");

                # * Print TensorFlow version.
                GPUDetector.logger.info("TensorFlow version: {}".format(tf.__version__));

                # * List physical devices.
                GPUDetector.logger.info("Physical devices: {}".format(tf.config.list_physical_devices()));

                # * Check GPU support.
                GPUDetector.logger.info("GPU support: {}".format(tf.test.is_built_with_cuda()));

                # * Get GPU device name.
                gpu_name = tf.test.gpu_device_name();

                # * Check GPU availability.
                gpu_available = tf.config.list_physical_devices("GPU");

                GPUDetector.logger.info("\n");
                GPUDetector.logger.info("GPU availability: {}".format(gpu_available));
                GPUDetector.logger.info("\n");

                if not gpu_available:
                    GPUDetector.logger.info("GPU device not found.");
                elif "GPU" not in gpu_name:
                    GPUDetector.logger.info("GPU device not found.");
                else:
                    GPUDetector.logger.info("Found GPU at: {}".format(gpu_name));

                # *Execute the decorated function.
                Result = func(*args, **kwargs);
                
                # * Close the logging handler.
                File_handler.close();

                return Result

            return wrapper
        return Inner




