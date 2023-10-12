# ? Class for images cropping.
import os 
import pandas as pd
import cv2

from Class_ImageSorter import ImageSorter

class CropImages:
    """

    A class used to crop Mini-MIAS images using the coordinates from the website.

    Methods
    -------
    data_dic()
        Returns a dictionary containing the attributes of the class.
    CropMIAS()
        Crops the images according to the coordinates in the CSV file.

    Attributes
    ----------
    __Folder : str
        Path to the folder containing the images.
    __Folder_Normal_images_splitted : str
        Path to the folder containing the cropped normal images.
    __Folder_Tormal_images_splitted : str
        Path to the folder containing the cropped tumor images.
    __Folder_Bormal_images_splitted : str
        Path to the folder containing the cropped benign images.
    __Folder_Malignant_images_splitted : str
        Path to the folder containing the cropped malignant images.
    __Dataframe : pd.DataFrame
        The dataframe containing the coordinates of the images to be cropped.
    __Shapes : int
        The size of the cropped images.
    __X_mean : int
        The x-coordinate of the center of the image.
    __Y_mean : int
        The y-coordinate of the center of the image.
    """

    # * Initializing (Constructor)
    def __init__(self, **kwargs) -> None:
        """
        Parameters
        ----------
        Folder : str
            Path to the folder containing the images.
        NF : str
            Path to the folder for saving the cropped normal images.
        TF : str
            Path to the folder for saving the cropped tumor images.
        BF : str
            Path to the folder for saving the cropped benign images.
        MF : str
            Path to the folder for saving the cropped malignant images.
        Dataframe : pd.DataFrame
            The dataframe containing the coordinates of the images to be cropped.
        Shapes : int
            The size of the cropped images.
        X mean : int
            The x-coordinate of the center of the image.
        Y mean : int
            The y-coordinate of the center of the image.
        """

        # * CSV to extract data
        self.__Dataframe: pd.DataFrame = kwargs.get('Dataframe', None);

        # * This algorithm outputs crop values for images based on the coordinates of the CSV file.
        self.Folder_path: str = kwargs.get('folder', None);

        '''self.__Folder_Normal_images: str = kwargs.get('Normal', None)
        self.__Folder_Tumor_images: str = kwargs.get('Tumor', None)
        self.__Folder_Benign_images: str = kwargs.get('Benign', None)
        self.__Folder_Malignant_images: str = kwargs.get('Malignant', None)'''

        self.Shapes = kwargs.get('Shapes', None);
        
        # * X and Y mean to extract normal cropped images
        self.X_mean = kwargs.get('Xmean', None);
        self.Y_mean = kwargs.get('Ymean', None);

        self.Image_sorter = ImageSorter(self.Folder_path);

    # * Class description
    def __str__(self) -> str:
        """
        Return a string description of the CropImages object.

        Returns:
        ----------
        str
            A string description of the CropImages object.
        """

        return f'''{self.__class__.__name__}:A class used to change the format of a file to another.''';

    # * Deleting (Calling destructor)
    def __del__(self) -> None:
        """
        Destructor called when the CropImages object is deleted.

        Returns:
        ----------
        None
        """

        print(f'Destructor called, {self.__class__.__name__} class destroyed.');
    
    
    # ? Method to crop Mini-MIAS images.
    def CropMIAS(self) -> None:
        

        os.chdir(self.Folder_path)

        Asterisks = 60;

        # * Columns
        Name_column = 0;
        Severity = 3;
        X_column = 4;
        Y_column = 5;
        Radius = 6;

        # * Labels
        Benign = 0;
        Malignant = 1;
        Normal = 2;

        # * Initial index
        Index = 1;
        
        # * Using sort function
        Sorted_files, Total_images = self.Image_sorter.sort_images();
        Count = 1;

        # * Reading the files
        for File in Sorted_files:
        
            Filename, Format = os.path.splitext(File);

            print("*" * Asterisks);
            print(self.__Dataframe.iloc[Index - 1, Name_column]);
            print(Filename);
            print("*" * Asterisks);

            if self.__Dataframe.iloc[Index - 1, Severity] == Benign:
                if self.__Dataframe.iloc[Index - 1, X_column] > 0  or self.__Dataframe.iloc[Index - 1, Y_column] > 0:
                
                    try:
                    
                        print(f"Working with {Count} of {Total_images} {Format} Benign images, {Filename} X: {self.__Dataframe.iloc[Index - 1, X_column]} Y: {self.__Dataframe.iloc[Index - 1, Y_column]}")
                        print(self.__Dataframe.iloc[Index - 1, Name_column], " ------ ", Filename, " ✅")
                        Count += 1

                        # * Reading the image
                        Path_file = os.path.join(self.Folder_path, File)
                        Image = cv2.imread(Path_file)
                        
                        #Distance = self.Shape # X and Y.
                        #Distance = self.Shape # Perimetro de X y Y de la imagen.
                        #Image_center = Distance / 2 
                            
                        # * Obtaining the center using the radius
                        Image_center = (self.__Dataframe.iloc[Index - 1, Radius] / 2);

                        # * Obtaining dimension
                        Height_Y = Image.shape[0] ;
                        #print(Image.shape[0]);
                        #print(self.__Dataframe.iloc[Index - 1, Radius]);

                        # * Extract the value of X and Y of each image
                        X_size = self.__Dataframe.iloc[Index - 1, X_column];
                        Y_size = self.__Dataframe.iloc[Index - 1, Y_column];
                            
                        # * Extract the value of X and Y of each image
                        XDL = (X_size - Image_center);
                        XDM = (X_size + Image_center);
                            
                        # * Extract the value of X and Y of each image
                        YDL = (Height_Y - Y_size - Image_center);
                        YDM = (Height_Y - Y_size + Image_center);

                        # * Cropped image
                        Cropped_Image = Image[int(YDL):int(YDM), int(XDL):int(XDM)]

                        print(Image.shape, " ----------> ", Cropped_Image.shape)

                        New_name_filename = Filename + '_Benign_cropped' + Format

                        New_folder = os.path.join(self.__Benignfolder, New_name_filename)
                        cv2.imwrite(New_folder, Cropped_Image)

                        New_folder = os.path.join(self.__Tumorfolder, New_name_filename)
                        cv2.imwrite(New_folder, Cropped_Image)

                    except OSError:
                            print(f"Cannot convert {File} ❌, {str(e)}");

            elif self.__Dataframe.iloc[Index - 1, Severity] == Malignant:
                if self.__Dataframe.iloc[Index - 1, X_column] > 0  or self.__Dataframe.iloc[Index - 1, Y_column] > 0:

                    try:

                        print(f"Working with {Count} of {Total_images} {Format} Malignant images, {Filename} X {self.__Dataframe.iloc[Index - 1, X_column]} Y {self.__Dataframe.iloc[Index - 1, Y_column]}")
                        print(self.__Dataframe.iloc[Index - 1, Name_column], " ------ ", Filename, " ✅")
                        Count += 1

                        # * Reading the image
                        Path_file = os.path.join(self.__Folder, File)
                        Image = cv2.imread(Path_file)
                        
                        #Distance = self.Shape # X and Y.
                        #Distance = self.Shape # Perimetro de X y Y de la imagen.
                        #Image_center = Distance / 2 
                            
                        # * Obtaining the center using the radius
                        Image_center = self.__Dataframe.iloc[Index - 1, Radius] / 2 # Center
                        # * Obtaining dimension
                        Height_Y = Image.shape[0] 
                        print(Image.shape[0])

                        # * Extract the value of X and Y of each image
                        X_size = self.__Dataframe.iloc[Index - 1, X_column]
                        Y_size = self.__Dataframe.iloc[Index - 1, Y_column]
                            
                        # * Extract the value of X and Y of each image
                        XDL = X_size - Image_center
                        XDM = X_size + Image_center
                            
                        # * Extract the value of X and Y of each image
                        YDL = Height_Y - Y_size - Image_center
                        YDM = Height_Y - Y_size + Image_center

                        # * Cropped image
                        Cropped_Image_Malig = Image[int(YDL):int(YDM), int(XDL):int(XDM)]

                        print(Image.shape, " ----------> ", Cropped_Image_Malig.shape)
                
                        # print(Cropped_Image_Malig.shape)
                        # Display cropped image
                        # cv2_imshow(cropped_image)

                        New_name_filename = Filename + '_Malignant_cropped' + Format

                        New_folder = os.path.join(self.__Malignantfolder, New_name_filename)
                        cv2.imwrite(New_folder, Cropped_Image_Malig)

                        New_folder = os.path.join(self.__Tumorfolder, New_name_filename)
                        cv2.imwrite(New_folder, Cropped_Image_Malig)

                        #Images.append(Cropped_Image_Malig)


                    except OSError:
                        print(f"Cannot convert {File} ❌, {str(e)}");
            
            elif self.__Dataframe.iloc[Index - 1, Severity] == Normal:
                if self.__Dataframe.iloc[Index - 1, X_column] == 0  or self.__Dataframe.iloc[Index - 1, Y_column] == 0:

                    try:

                        print(f"Working with {Count} of {Total_images} {Format} Normal images, {Filename}")
                        print(self.__Dataframe.iloc[Index - 1, Name_column], " ------ ", Filename, " ✅")
                        Count += 1

                        Path_file = os.path.join(self.__Folder, File)
                        Image = cv2.imread(Path_file)

                        Distance = self.__Shapes # Perimetro de X y Y de la imagen.
                        Image_center = Distance / 2 # Centro de la imagen.
                        #CD = self.df.iloc[Index - 1, Radius] / 2
                        # * Obtaining dimension
                        Height_Y = Image.shape[0] 
                        print(Image.shape[0])

                        # * Extract the value of X and Y of each image
                        X_size = self.__X_mean
                        Y_size = self.__Y_mean
                            
                        # * Extract the value of X and Y of each image
                        XDL = X_size - Image_center
                        XDM = X_size + Image_center
                            
                        # * Extract the value of X and Y of each image
                        YDL = Height_Y - Y_size - Image_center
                        YDM = Height_Y - Y_size + Image_center

                        # * Cropped image
                        Cropped_Image_Normal = Image[int(YDL):int(YDM), int(XDL):int(XDM)]

                        # * Comparison two images
                        print(Image.shape, " ----------> ", Cropped_Image_Normal.shape)
                    
                        New_name_filename = Filename + '_Normal_cropped' + Format

                        New_folder = os.path.join(self.__Normalfolder, New_name_filename)
                        cv2.imwrite(New_folder, Cropped_Image_Normal)

                        #Images.append(Cropped_Image_Normal)

                    except OSError as e:
                        print(f"Cannot convert {File} ❌, {str(e)}");

            Index += 1   