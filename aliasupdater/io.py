from typing import List
import openpyxl
import os



def read_lookuptable(filepath: str) -> List:
    """
    Reads the lookup table from a spreadsheet.

    :param filepath: The local filepath to the spreadsheet.
    :raises ValueError: If the file is not supported.

    :return: The list of cell values of the spreadsheet.
    """
    # format the path to the excel document so it is recognized as a path
    normalized_filepath = os.path.normpath(filepath)

    # Read the lookup table and store the fields and alias names
    # TODO: Maybe use the standard library for parsing the file extension!
    # TODO: Prefer to using the logging capabilities!
    if normalized_filepath[-4:] != "xlsx":
        print("Please check your input. It needs to be a .xlsx excel file")
        raise ValueError("Please check your input. It needs to be a .xlsx excel file")
    else:
        print("Grabbing field and alias names from excel document...")
    
    # Open Master Metadata excel document
    workbook = openpyxl.load_workbook(normalized_filepath)
    sheet = workbook.active

    # Create an empty list to store all fields and alias names
    lookup_list = []

    # Store values from master metadata excel doc and put into a list
    # TODO: Why are we explicitly calling __next__()
    iter = sheet.iter_rows()
    iter.__next__()
    for row in iter:
        inner_list = []
        for val in row:
            inner_list.append(val.value)
        lookup_list.append(inner_list)

    workbook.close()
    return lookup_list