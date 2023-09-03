import pandas as pd


class StorageContainer:
    
    def __init__(self, size=None, dims=None, name=None):
        self._name = None
        self.name = name
        self._size = None
        self.size = size
        self._dims = None
        self.dims = dims
        self.number_of_rows = None
        self.number_of_columns = None
        self.wells = None
        self.rows = None
        self.columns = None

        self.validate_container()

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

    def add_item(self, position, item, type=None):
        if item in self.data["id"].tolist():
            raise ValueError(f"Invalid name - '{item}' already exist in plate.")
        self.data.loc[position, "id"] = item
        self.data.loc[position, "type"] = type

    def remove_item(self, position, greedy=False):
        self.data.loc[position, "id"] = None
        if greedy:
            self.data.loc[position, "type"] = None

    def add_type(self, position, type):
        self.data.loc[position, "type"] = type

    def remove_type(self, position):
        self.data.loc[position, "type"] = None

    def get_item(self, position):
        return self.data.loc[position]["id"]

    def find_item(self, item):
        return self.data[self.data.id == item].index

    def validate_container(self):
        if self._dims and self._size:
            if not self._dims[0] * self._dims[1] == self._size:
                raise ValueError(f"Plate size '{self._size}' and dims '{self._dims}' do not match!")
        if self._dims and not self._size:
            self.size = self._dims[0] * self._dims[1]
        if self._dims:
            self.number_of_rows, self.number_of_columns = self._dims

    def instantiate_empty_container(self):
        data = pd.DataFrame(index=self.wells)
        data["id"] = None
        data["type"] = None
        data.reset_index(inplace=True)
        data["row"] = data["index"].apply(lambda x: x[0])
        data["column"] = data["index"].apply(lambda x: x[1:])
        data["plate_id"] = self.name
        data.set_index("index", inplace=True)
        self.data = data

    def count_empty(self, on="type"):
        return self.show(values=on).isna().sum().sum()

    def show(self, values="id"):
        idata = self.data.reset_index()
        idata["row"] = idata["index"].apply(lambda x: x[0])
        idata["column"] = idata["index"].apply(lambda x: x[1:])
        return idata.pivot(index="row", columns="column", values=values)


class Plate(StorageContainer):
    STANDARD_FORMATS = {6: (2, 3), 12: (3, 4), 24: (4, 6), 48: (6, 8), 96: (8, 12), 384: (16, 24)}

    def __init__(self, size=None, dims=None, name=None):
        super().__init__(size, dims, name)
        if not self._dims and not self._size:
            print(f"No plate information was passed.\nInitializing default plate: 96-well plate")
            self.size = 96
        self.validate_plate()
        self.instantiate_empty_container()

    def __str__(self):
        return (f"{self.size if self.size else '<UNDEFINED>'}-well plate "
                f"({self.number_of_rows if self.number_of_rows else '<UNDEFINED>'} rows x "
                f"{self.number_of_columns if self.number_of_columns else '<UNDEFINED>'} columns)")

    def validate_plate(self):
        if not self._dims and self._size:
            if self._size not in Plate.STANDARD_FORMATS:
                raise ValueError(f"Invalid plate size '{self._size}'. Pass valid dimensions to enforce initialization, "
                                 f"or choose one of valid plate sizes: {Plate.STANDARD_FORMATS.keys()}")
            else:
                self.dims = Plate.STANDARD_FORMATS[self._size]
        if self.number_of_rows:
            self.rows = [chr(65+i) for i in range(self.number_of_rows)]
        if self.number_of_columns:
            zwidth = len(str(self._size))
            self.columns = [str(i).zfill(zwidth) for i in range(1,self.number_of_columns+1)]
        self.wells = [a+b for a in self.rows for b in self.columns]


# %%
