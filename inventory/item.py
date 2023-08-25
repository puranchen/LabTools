
class StorageItem:
    def __init__(self, **kwargs):
        attributes = ["company", "cat_no", "exp_date", "owner"]
        for attr in attributes:
            setattr(self, attr, None)
            value = kwargs.get(attr)
            if value:
                setattr(self, attr, value)
    def get_details(self):
        return {
            "Company": self.company,
            "Catalogue No.": self.cat_no,
            "Expiry Date": self.exp_date,
            "Owner": self.owner
        }


class FlowAntibody(StorageItem):

    def __init__(self, **kwargs):
        super.__init__(**kwargs)
        attributes = ["antigen", "conjugate", "clone", "volume_cat", "comment", "vial_size"]
        for attr in attributes:
            setattr(self, f"_{attr}", None)
            value = kwargs.get(attr)
            if value:
                setattr(self, attr, value)