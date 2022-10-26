import json
from datetime import datetime
from re import sub


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime):
            return str(z)
        else:
            return super().default(z)


class BinaryTree:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def printTree(self, tree, level=0):
        if type(tree) == list:
            print("  " * 4 * level + "->" + tree[0] + tree[1] + tree[2])
        elif tree is not None:
            self.printTree(tree.left, level + 1)
            print("  " * 4 * level + "->" + tree.data)
            self.printTree(tree.right, level + 1)


def fix_key_in_dict_of_roots(dict_of_roots):
    if dict_of_roots == {}:
        return {}
    new_dict_of_roots = {}
    for root_key in dict_of_roots.keys():
        root_removed_key = remove_root(root_key)
        new_dict_of_roots[root_removed_key] = dict_of_roots[root_key]
    return new_dict_of_roots


def remove_root(text: str):
    new_text = text.replace("root", "")
    new_text = sub("[\[\]'\"]", "", new_text)  # noqa: W605
    return new_text


def remove_key_from_list_of_dict(keys, d_list):
    for items in d_list:
        for key in keys:
            if key in items:
                del items[key]


class ListOfDictsComparor:
    def intersection(self, l1, l2):
        return [x for x in l1 if x in l2]

    def difference(self, l1, l2):
        # l1 - l2
        return [x for x in l1 if x not in l2]
