import pandas as pd
from typing import Tuple


class StorageContainer:
    def __init__(self, name=None, *args, **kwargs):
        self.name = name
        self.number_of_rows = None
        self.number_of_columns = None
        self.wells = None
        self.rows = None
        self.columns = None

    def add_item(self, row, column, item):
        ...

    def remove_item(self, row, column, item):
        ...

    def get_item(self, row, column):
        ...

    def find_item(self, item):
        ...

    def instantiate_empty_container(self):
        data = pd.DataFrame(index=self.wells)
        data["id"] = None
        self.data = data

    def show(self):
        idata = self.data.reset_index()
        idata["row"] = idata["index"].apply(lambda x: x[0])
        idata["column"] = idata["index"].apply(lambda x: x[1:])
        return idata.pivot(index="row", columns="column", values="id")


class Plate(StorageContainer):
    STANDARD_FORMATS = {6: (2, 3), 12: (3, 4), 24: (4, 6), 48: (6, 8), 96: (8, 12), 384: (16, 24)}

    def __init__(self, size=None, name=None, *args, **kwargs):
        super().__init__(name, size, *args, **kwargs)
        self._size = None
        self.size = size
        self._dims = None
        self.dims = kwargs.get("dims")
        if not self._dims and not self._size:
            print(f"No plate information was passed.\nInitializing default plate: 96-well plate")
            self.size = 96
        self.validate_init()

    def __str__(self):
        return f"{self.size if self.size else '<UNDEFINED>'}-well plate ({self.number_of_rows if self.number_of_rows else '<UNDEFINED>'} rows x {self.number_of_columns if self.number_of_columns else '<UNDEFINED>'} columns)"

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if value:
            if not isinstance(value, int):
                raise TypeError("'size' must be an integer.")
            self._size = value

    @property
    def dims(self):
        return self._dims

    @dims.setter
    def dims(self, value):
        if value:
            if not isinstance(value, tuple):
                raise TypeError("'dims' must be a tuple (n_rows, n_cols)")
            if not isinstance(value[0], int) or not isinstance(value[1], int):
                raise ValueError("Both dimensions must be integers")
            self._dims = value
            self.number_of_rows, self.number_of_columns = self._dims

    def validate_init(self):
        if self._dims and self._size:
            if not self._dims[0] * self._dims[1] == self._size:
                raise ValueError(f"Plate size '{self._size}' and dims '{self._dims}' do not match!")
        if self._dims and not self._size:
            self.size = self._dims[0] * self._dims[1]
        if not self._dims and self._size:
            if self._size not in Plate.STANDARD_FORMATS:
                raise ValueError(f"Invalid plate size '{self._size}'. Pass valid dimensions to enforce initialization, "
                                 f"or choose one of valid plate sizes: {Plate.STANDARD_FORMATS.keys()}")
            else:
                self.dims = Plate.STANDARD_FORMATS[self._size]


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

# %%
