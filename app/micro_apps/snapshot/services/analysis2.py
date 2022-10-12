from collections import Counter
from itertools import chain


def redundant_sharing(collection, snapshot):
    for file in collection[snapshot].values():
        setA = set(file["direct_permission"])
        setB = set(file["inherited_permission"])
        redundant_permission = setA.intersection(setB)
        if len(redundant_permission) != 0:
            print(
                "The file " + file["name"] + " has ",
                redundant_permission,
                " as a redundant permission.",
            )


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
                    print(
                        "The file " + fi["name"] + " has ",
                        file_only,
                        " as its permissions while its folder "
                        + folder["name"]
                        + " does not have one",
                    )
                elif len(file_only) == 0:
                    print(
                        "The file " + fi["name"] + " does not have ",
                        folder_only,
                        " as its permissions while its folder "
                        + folder["name"]
                        + " have one",
                    )
                elif len(folder_only) == 0 and len(file_only) == 0:
                    print()
                else:
                    print(
                        "The file " + fi["name"] + " has ",
                        file_only,
                        " as its permissions while its folder "
                        + folder["name"]
                        + " has ",
                        folder_only,
                        " as its permissions.",
                    )
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

redundant_sharing(collection, 1)
file_folder_sharing_difference(collection, 2)
deviant_sharing(collection, 1, 0.8)
