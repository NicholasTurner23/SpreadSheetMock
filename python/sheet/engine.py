from .helpers import *
from .models import Index
from typing import Any
from typing_extensions import TypedDict

__all__ = ["Spreadsheet"]

class Spreadsheet:
    """The spreadsheet engine. This is your job to implement!
    
    These functions are called by the spreadsheet UI.  Each time a value or 
    format is changed, `get_formatted` will be called for every cell in the 
    spreadsheet in sequence.
    """
    def __init__(self) -> None:
        self.sheet:dict[str, dict] = {}

    def get_formatted(self, index):
        """Get the evaluated and formatted value at the given cell ref.

        Arguments:
            index (Index): the cell to evaluate

        Returns:
            str: the cell value, evaluated (if a formula) and formatted
            according to the format set with `set_format`.
        """
        row = index.row_label
        col = index.column_label

        sheet = self.sheet

        entry:dict[str, dict] = {}
        original_value_:str = ""
        formatted_value_:str = ""
        
        if len(sheet) >= 1:
            try:
                entry = sheet.get(row)
                original_value_ = entry.get(col).get("original_value")
                formatted_value_ = entry.get(col).get("formatted_value")
            except AttributeError as e:
                pass

            
            if original_value_.startswith("="):
                try:
                    index = Index.parse(original_value_[1:])
                except ValueError as e:
                    raise ValueError(f"Error parsing formula '{original_value_}': {str(e)}")
                else:
                    row = index.row_label
                    col = index.column_label
                    entry = self.sheet.get(row, {})
                    ovalue_ = entry.get(col, {}).get("original_value", "")
                    fvalue_ = entry.get(col, {}).get("formatted_value", "")
                    formatted_value_ = fvalue_ if fvalue_ else ovalue_


            if formatted_value_ is None:
                return original_value_
            return formatted_value_
        else:
            return
        

    def get_raw(self, index):
        """Get the raw text that the user entered into the given cell.

        Arguments:
            index (Index): the cell to fetch

        Returns:
            str: the `raw` most recently set with `set`.
        """
        row = index.row_label
        col = index.column_label

        entry:dict[str, dict] = {}
        value:str = ""

        sheet = self.sheet

        if len(sheet) >= 1:
            try:
                entry:dict[str, dict] = sheet
                value:str = entry.get(row).get(col).get("original_value")
            except AttributeError as e:
                pass
            
        return value
    

    def set(self, index, raw):
        """Set the value at the given cell.

        Arguments:
            index (Index): the cell to update
            raw (str): the raw string, like ``'1'`` or ``'2018-01-01'`` or ``'=A2'``
        """
        if index == "":
            return
        
        row = index.row_label
        col = index.column_label

        if raw == "":
            del self.sheet[row]
            return 

        if self.sheet.get(row, -1) == -1:
            self.sheet[row] = {col:{"types":[type(raw)], "spec":"None", "original_value":raw, "formatted_value":None}}
        else:
            self.sheet.get(row, "Nan").update({col:{"types":[type(raw)], "spec":"None", "original_value":raw, "formatted_value":None}})
        
        return

    def set_format(self, index, type, spec):
        """Set the format string for a given cell.

        Arguments:
            index (Index): the cell to format
            type (str): the type of format--``'default'``, ``'number'`` or ``'date'``
            spec (str): the format string to use on the cell:

                - if `type` is ``'default'``, should be None
                - if `type` is ``'number'``, a string suitable for passing to
                  python's string % operator, e.g. ``'%.2f'``
                - if `type` is ``'date'``, a string suitable for passing to
                  `datetime.strftime`, e.g. ``'%Y-%m-%d'``
        """
        # index_ = Index.parse(index)
        row = index.row_label
        col = index.column_label

        if self.sheet.get(row, -1) == -1:
            raise KeyError 
        else:
            entry:dict[str, dict] = self.sheet.get(row, {})
            value:str = entry.get(col).get("original_value")
            types:list = entry.get(col).get("types")
            if len(types) < 2:
                types.append(type)
            if check_spec(type, spec):
                formatted = formatted_value(type, value, spec)
            self.sheet.get(row, {}).update({col:{"types":types, "spec":spec, "original_value":value, "formatted_value":formatted}})
        return


