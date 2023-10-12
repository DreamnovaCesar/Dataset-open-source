import os
import logging

import tqdm

from typing import Optional

class ImageSorter:
  """
  A class for sorting and displaying image files within a folder.

  Attributes
  ----------
  Folder_path : str
    The path to the folder containing image files.

  Methods
  -------
  sort_images()
    Sorts the image files in the folder and displays their details.

  """

  # * Initializing (Constructor)
  def __init__(self, Folder_path: str) -> None:
    """
    Initialize the ImageSorter class.

    Parameters
    ----------
    folder_path : str
        The path to the folder containing image files.
    """

    logging.info("Initializing ImageSorter class...");
    self.__Folder_path = Folder_path;

  #? Sort the image files in the folder and display their details.
  def sort_images(self, log_folder: Optional[str] = None) -> tuple[list[str], int]:
    """
    Sort the image files in the folder and display their details.

    Returns
    -------
    Sorted_files : list[str]
        A list of sorted image file names.
    Number_images : int
        The number of image files in the folder.
    """

    Asterisks = 60;

    logging.info(f"Sorting image files in folder: {self.__Folder_path}");

    # * Try to sort the images and display the results.
    try:
        # * Check if folder_path is None
        if self.__Folder_path is None:
            raise ValueError("Folder does not exist");

        # * Check if folder_path is a string
        if not isinstance(self.__Folder_path, str):
            raise TypeError("Folder must be a string");

        # * Create a logging handler for the file.
        if log_folder is not None:
            log_file_path = os.path.join(log_folder, 'sort_images.log')
        else:
            log_file_path = 'sort_images.log'

        file_handler = logging.FileHandler(log_file_path);
        file_handler.setLevel(logging.DEBUG);

        # * Add the handler to the logger.
        logging.getLogger('sort_images').addHandler(file_handler);

        # * Get the number of images in the folder
        Number_images = len(os.listdir(self.__Folder_path));
        logging.debug(f"Number of images: {Number_images}");

        # * Print the number of images
        print("\n");
        print("*" * Asterisks);
        print(f'Images: {Number_images}');
        print("*" * Asterisks);

        # * Get the list of files in the folder
        files = os.listdir(self.__Folder_path);
        logging.debug(f"Files in folder: {files}");

        # * Sort the list of files
        Sorted_files = sorted(files);
        logging.debug(f"Sorted files: {Sorted_files}");

        # * Print the sorted files
        print("\n")
        for index, sort_file in enumerate(tqdm.tqdm(Sorted_files, total=Number_images)):
            print(f"Index: {index} ----- {sort_file} ✅");

        print("\n")

        return Sorted_files, Number_images
    except Exception as e:
        logging.error(f"Failed to sort images: {e}")
        raise e

    finally:
        logging.info("Finished sorting images.")

        # * Remove the file handler.
        logging.getLogger('sort_images').removeHandler(file_handler);