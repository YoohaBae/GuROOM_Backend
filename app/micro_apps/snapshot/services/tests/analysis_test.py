import pytest
from collections import Counter
from itertools import chain


def redundant_sharing(collection, snapshot):
    for file in collection[snapshot].values():
        setA = set(file["direct_permission"])
        setB = set(file["inherited_permission"])
        redundant_permission = setA.intersection(setB)
        if len(redundant_permission) != 0:
            return redundant_permission
              


def file_folder_sharing_difference(collection, snapshot):
    path = list()
    files = list()
    folder = 0
    for file in collection[snapshot].values():
        if file["isFolder"] is True:
            path.append(file["absoulte_path"])

    for p in path:
        for f in collection[snapshot].values():
            if f["absoulte_path"] == p and f["isFolder"] is False:
                files.append(f)
            if f["absoulte_path"] == p and f["isFolder"] is True:
                folder = f

        for fi in files:
            if folder["file_permissions"] != fi["file_permissions"]:
                setA = set(folder["file_permissions"])
                setB = set(fi["file_permissions"])
                folder_only = setA - setB
                file_only = setB - setA
                if len(folder_only) == 0:
                   return file_only
                       
                       
                    
                elif len(file_only) == 0:
                    return folder_only
                elif len(folder_only) == 0 and len(file_only) == 0:
                    print()
                else:
                    return file_only, folder_only
        files.clear()


def commonly_occuring_permissions(List, threshold):
    num = list()
    size = len(List) * threshold
    temp = Counter(chain.from_iterable(List))

    for k, v in temp.items():
        if v > size:
            num.append(k)
    return num


def deviant_sharing(collection, snapshot, threshold):
    path = list()
    files = list()
    temp = list()
    deviancy = 0
    for file in collection[snapshot].values():
        if file["isFolder"] is True:
            path.append(file["absoulte_path"])

    for p in path:
        for f in collection[snapshot].values():
            if f["absoulte_path"] == p and f["isFolder"] is False:
                files.append(f)
        for fi in files:
            temp.append(fi["file_permissions"])
        setCommon = set(commonly_occuring_permissions(temp, threshold))
        for fi in files:
            setFile = set(fi["file_permissions"])
            setDeviancy = setFile - setCommon
            setUnion = setFile | setCommon
            deviancy = 1 - (len(setFile.intersection(setCommon)) / len(setUnion))
            if len(setDeviancy) == 0:
                return deviancy > threshold, deviancy
            else:
                return deviancy > threshold, deviancy, setDeviancy


collection = {
    1: {
        "a": {
            "name": "a.exe",
            "direct_permission": ["jk", "eh", "yh", "dh"],
            "inherited_permission": ["jk"],
            "file_permissions": ["jk", "eh", "yh", "dh"],
            "absoulte_path": "home/jinkyu",
            "isFolder": False,
        },
        "b": {
            "name": "a.dat",
            "direct_permission": ["jk", "eh", "yh"],
            "inherited_permission": [""],
            "file_permissions": ["jk", "eh", "yh"],
            "absoulte_path": "home/jinkyu",
            "isFolder": False,
        },
        "c": {
            "name": "c",
            "direct_permission": ["jk", "eh", "yh"],
            "inherited_permission": ["jk", "sh"],
            "file_permissions": ["jk", "eh", "yh", "sh"],
            "absoulte_path": "home/jinkyu",
            "isFolder": True,
        },
    },
    2: {
        "d": {
            "name": "d.word",
            "direct_permission": ["sk", "eh", "yh", "dh"],
            "inherited_permission": ["jk"],
            "file_permissions": ["jk", "eh", "yh", "dh", "sk"],
            "absoulte_path": "home/yooha",
            "isFolder": False,
        },
        "e": {
            "name": "e",
            "direct_permission": ["jk", "eh", "yh"],
            "inherited_permission": ["yh"],
            "file_permissions": ["jk", "eh", "yh"],
            "absoulte_path": "home/yooha",
            "isFolder": True,
        },
        "f": {
            "name": "f.ppt",
            "direct_permission": ["jk", "eh", "yh"],
            "inherited_permission": ["jk", "sh"],
            "file_permissions": ["jk", "eh", "yh", "sh"],
            "absoulte_path": "home/yooha",
            "isFolder": False,
        },
    },
}

def test_redundant_sharing():
    assert redundant_sharing(collection, 1) == {'jk'}

def test_redundant_sharing_fail():
    assert redundant_sharing(collection, 1) == {'eh'}

def test_file_folder_sharing_difference():
    assert file_folder_sharing_difference(collection, 2) == {'dh','sk'}

def test_file_folder_sharing_difference_fail():
    assert file_folder_sharing_difference(collection, 2) == {'sk'}

def test_deviant_sharing():
    assert deviant_sharing(collection, 1, 0.8) == (False, 0.25, {'dh'}) 

def test_deviant_sharing_failed():
    assert deviant_sharing(collection, 1, 0.8) == (True, 0.35, {'dh'}) 