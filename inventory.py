import pandas as pd
import numpy as np

class StorageContainer:
    def __init__(self, name=None, size=96, **kwargs):
        self.name = name
        self._size = None
        self.size = size

        self.items = pd.DataFrame(columns=["id", "row", "column"])

        dimensions = kwargs.get("dims")
        if dimensions:
            self.number_of_rows, self.number_of_columns = dimensions

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if not isinstance(value, int):
            raise TypeError("'number of wells' needs to be an integer")

    def add_item(self, row, column, item):
        ...

    def remove_item(self, row, column, item):
        ...

    def get_item(self, row, column):
        ...

    def find_item(self, item):
        ...

    @property
    def number_of_rows(self):
        return self._number_of_rows
    @number_of_rows.setter
    def number_of_rows(self, value):
        ...

    def instantiate_empty_container(self):
        dataframe = pd.DataFrame(np.full((self.x,self.y), None),
                                 index=self.rows, columns=self.columns)

        data = dataframe.stack()
        data.index.name = ["row", "column"]
        data.name = "id"
        return data

class StorageItem:
    def __init__(self, item_type, **kwargs):

        attributes = ["format",
                      "volume",
                      "concentration",
                      "concentration_unit",
                      "weight",
                      "weight_unit",
                      "expiry_date",
                      "last_modified"]

        self.item_type = item_type
        for attr in attributes:
            setattr(self, attr, None)
            value = kwargs.get(attr)
            if value:
                setattr(self, attr, value)

    def get_details(self):
        return {
            "Item Type": self.item_type,
            "Volume": self.volume,
            "Concentration": str(self.concentration) + self.concentration_unit,
            "Weight": str(self.weight) + self.weight_unit,
            "Expiry Date": self.expiry_date,
            "Last Modified": self.lastmodified_date
        }


class Plate(StorageContainer):

    VALID_FORMAT = {6:(2,3), 12:(3,4), 24:(4,6), 48:(6,8), 96:(8,12), 384:(16,24)}
    def __init__(self, size=96, name=None):
        super().__init__(name, size)

    @property
    def size(self):
        return self._self

    @size.setter
    def size(self, value):
        if value not in Plate.VALID_FORMAT:
            raise ValueError("Invalid plate size")
        self._size = value




        if value not in Plate.VALID_FORMAT:
            raise ValueError("Invalid plate size")
        self._number_of_wells = value
        self.number_of_rows, self.number_of_columns = Plate.VALID_FORMAT[self._number_of_wells]

        self.wells = [a + b for a in self.rows for b in self.columns]

