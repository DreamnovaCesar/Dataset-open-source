import pandas as pd
import logging

class DataFrameRefiller:
    """
    A class for refilling a Pandas DataFrame with 'None' values and saving it to a CSV file.

    Parameters
    ----------
    CSV_file_path : str
        The path to the CSV file to be refilled.

    Attributes
    ----------
    CSV_file_path : str
        The path to the CSV file.
    logger : Logger
        A logger for logging messages.

    Methods
    -------
    refill_dataframe()
        Refills the DataFrame with 'None' values and saves it to the CSV file.

    Raises
    ------
    FileNotFoundError
        If the CSV file is not found.
    Exception
        If an error occurs during the operation.

    Example
    -------
    CSV_file_path = 'your_csv_file.csv';
    RF = DataFrameRefiller(CSV_file_path);
    RF.refill_dataframe();
    """

    def __init__(self, CSV_file_path):
        """
        Initialize the DataFrameRefiller.

        Parameters
        ----------
        CSV_file_path : str
            The path to the CSV file to be refilled.
        """

        self.CSV_file_path = CSV_file_path;
        self.logger = logging.getLogger(__name__);
        logging.basicConfig(level=logging.INFO);

    def refill_dataframe(self):
        """
        Refill the DataFrame with 'None' values and save it to the CSV file.

        This method reads the specified CSV file, replaces NaN values with 'None',
        and then saves the modified DataFrame back to the same CSV file.

        Raises
        ------
        FileNotFoundError
            If the CSV file is not found.
        Exception
            If an error occurs during the operation.
        """
        try:

            Dataframe = pd.read_csv(self.CSV_file_path);

            # * Replace NaN with None
            Dataframe.fillna(None, inplace=True);
            Dataframe.to_csv(self.CSV_file_path, index=False);
            self.logger.info("DataFrame refilled with None values and saved to the CSV file.");
        
        except FileNotFoundError:
            self.logger.error(f"File '{self.CSV_file_path}' not found.");

        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}");

'''# Example usage:
csv_file_path = 'your_csv_file.csv'

refiller = DataFrameRefiller(csv_file_path)
refiller.refill_dataframe()'''