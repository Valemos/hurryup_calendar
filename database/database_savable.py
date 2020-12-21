
class DatabaseSavable:

    table_name: str = None
    """
    to save object attribute in column
    it must be included in dict with format:
    <object_field_name>: <SQL syntax definition>
    
    here object attribute must have axactly the same name as SQL column identifyer 
    """
    table_columns = {}


    """
    To allow saving functions work derived object 
    must have a constructor with no parameters (or all of them are default)
    """

    def __init__(self):
        # id is created by default for each object
        self.id = -1

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        else:
            return self.id == other.id

    def update_db(self, database):
        database.update(self)

    def delete_db(self, database):
        database.delete(self)

    @classmethod
    def from_table_values(cls, values):
        new_object = cls()
        for attribute, value_i in zip(cls.table_columns.keys(), range(len(values))):
            setattr(new_object, attribute, values[value_i])
        return new_object

    def get_values(self):
        return [(attribute, getattr(self, attribute)) for attribute in self.table_columns.keys()]
