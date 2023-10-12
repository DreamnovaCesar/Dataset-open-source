import os
import cv2
import json
import logging

from Decorator.Timer import Timer
from Class_Data import Data
from Class_ImageSorter import ImageSorter

class ChangeFormat:
    """
    A class for changing the format of image files in a folder to a desired format.

    Attributes:
    ----------
    folder : str
        The path to the folder containing the image files to be converted.
    new_folder : str
        The path to the folder where the converted image files will be saved.
    new_format : str
        The desired format for the image files (e.g., '.png', '.jpg').

    Methods:
    -------
    ChangeFormat()
        Changes the format of image files in the specified folder to the desired format.
    """

    # * Initializing (Constructor)
    def __init__(self, **kwargs):
        """
        Initialize a ChangeFormat instance.

        Parameters:
        ----------
        folder : str
            The path to the folder containing the image files to be converted.
        new_folder : str
            The path to the folder where the converted image files will be saved.
        new_format : str
            The desired format for the image files (default is '.png').

        Note: If new_folder is not specified, the converted files will be saved in the same folder as the original files.
        """

        # * Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.logger.info("Initializing {self.__class__.__name__} class...");

        self.__Folder = kwargs.get('folder', None);
        self.__New_folder = kwargs.get('new_folder', None);
        self.__New_format = kwargs.get('new_format', '.png');

        # * If NewFolder is None, use __Folder instead
        if self.__New_folder is None:
            self.__New_folder = self.__Folder;

    # * Class description
    def __str__(self) -> str:
        """
        Return a string description of the ChangeFormat object.

        Returns:
        ----------
        str
            A string description of the ChangeFormat object.
        """

        return f'''{self.__class__.__name__}:A class used to change the format of a file to another.''';

    # * Deleting (Calling destructor)
    def __del__(self) -> None:
        """
        Destructor called when the ChangeFormat object is deleted.

        Returns:
        ----------
        None
        """

        print(f'Destructor called, {self.__class__.__name__} class destroyed.');

    # * folder
    @property
    def Get_folder(self):
        """Getter method for the 'folder' property."""
        return self.__Folder

    # ? Method to change the format, for instance it could be png to jpg
    @Timer.timer(Data.Folder_logs, Data.Change_format_name)
    def ChangeFormat(self):
        """
        Change the format of image files in the specified folder to the desired format.

        This method reads image files from the 'folder' attribute, converts them to the format specified in the 'new_format' attribute,
        and saves the converted files in the 'new_folder' attribute (or the same folder if 'new_folder' is not specified).

        The method supports various image formats and tracks the progress of the conversion, reporting the number of images processed.

        Raises:
        ----------
        OSError
            If the image files cannot be converted to the desired format.

        Note: The 'new_format' attribute should be a supported image format (e.g., '.png', '.jpg').

        Example usage:
        --------------
        change_format = ChangeFormat(folder='/path/to/images', new_format='.jpg')
        change_format.ChangeFormat()
        """

        # * List of Image Formats Supported by OpenCV
        Images_supported_format = ('.bmp', '.pbm', '.pgm', '.ppm', '.sr', '.ras', '.jpeg', '.jpg', '.jpe', '.jp2', '.tiff', '.tif', '.png');
        
        Image_sorter = ImageSorter(self.__Folder);

        Count = 1;

        try:

            # * Compare the new format proposed with each format supported by OpenCV
            for Format_supported in Images_supported_format:
        
                if(self.__New_format == Format_supported):
                
                    # * Changes the current working directory to the given path
                    os.chdir(self.__Folder);
                    print(os.getcwd());
                    print("\n");

                    # * Using the sort function.
                    Sorted_files, Total_images = Image_sorter.sort_images();

                    # * Reading the files.
                    for File in Sorted_files:
                        # * Extract the file name and format.
                        Filename, Format  = os.path.splitext(File)

                        if File.endswith(Format):

                            try:
                                Filename, Format  = os.path.splitext(File)
                                print(f"Working with {Count} of {Total_images} {Format} images, {Filename} ------- {self.__New_format} ✅");
                                
                                # * Reading each image using cv2.
                                Path_file = os.path.join(self.__Folder, File)
                                Image = cv2.imread(Path_file)         
                                
                                # * Changing its format to a new one.
                                New_name_filename = Filename + self.__New_format
                                New_folder = os.path.join(self.__New_folder, New_name_filename)

                                cv2.imwrite(New_folder, Image)
                                Count += 1

                            except OSError:
                                print(f"Cannot convert {File} ❌") #! Alert

                    print("\n")
                    print(f"{Count} of {Total_images} tranformed ✅. From {Format} to {self.__New_format}.");

        except Exception as e:
            self.logger.error(f"Format incompatible {self.__New_format}, It must be: {Images_supported_format} ❌ {str(e)}")


