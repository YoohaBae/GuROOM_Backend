import json
from datetime import datetime


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime):
            return str(z)
        else:
            return super().default(z)


class ListOfDictsComparor:
    def intersection(self, l1, l2):
        return [x for x in l1 if x in l2]

    def difference(self, l1, l2):
        # l1 - l2
        return [x for x in l1 if x not in l2]
