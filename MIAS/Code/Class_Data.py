class Data:
    """
    A class to store data-related constants and paths.

    Attributes:
    ----------
    Folder_data : str
        The path to the main data folder.
    Folder_logs : str
        The path to the logs folder inside the main data folder.
    
    Constants:
    ----------
    Change_format_name : str
        The name of the 'ChangeFormat' operation.

    Example usage:
    --------------
    data = Data()
    data_folder = data.Folder_data
    logs_folder = data.Folder_logs
    change_format_operation = data.Change_format_name
    """
    
    Folder_data = r"MIAS\Code\Data"
    Folder_logs = r"MIAS\Code\Data\logs"

    Change_format_name = "ChangeFormat"