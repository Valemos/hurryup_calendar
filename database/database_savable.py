
class DatabaseSavable:
    """
    This class is an interface to create table in database
    and save specified fields of an objects in that table
    """

    """
    static specification of table name
    name must be all lower case or surrounded in escaped double quotes \"\"
    """
    table_name: str = None

    """
    to save object attribute in column
    it must be included in dict with format:
    <object_field_name>: <SQL syntax definition>
    
    here object attribute have axactly the same name as SQL column identifyer 
    """
    table_columns = {}

    """
    If an object has any composite key, it can be defined using this variable
    
    It must specify list of column names to be included to primary key
    
    If table_composite_primary_key is None, primary key must be defined as modifier to existing column 
    """
    table_composite_primary_key: list = None

    def __init__(self):
        # id is created by default for each object
        self.id = -1

    def update_db(self, database):
        database.update(self)

    def delete_db(self, database):
        database.delete(self)

    def get_values(self):
        """
        Returns list with pairs of values according to table description
        Key is name of field, Value contains values of corresponding variable

        id field is omitted

        this method is universal for any derived object if table_columns is in correct format
        """

        return [(attribute, getattr(self, attribute)) for attribute in self.table_columns.keys()]
