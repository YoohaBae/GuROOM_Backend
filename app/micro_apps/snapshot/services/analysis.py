def redundant_sharing(collection, snapshot):
    for file in collection[snapshot]:
        if file[inherited_permission] == file[direct_permission]:
            redundant_permission = file[direct_permission]
            print(
                "The file "
                + file[name]
                + " has "
                + redundant_permission
                + " as a redundant permission."
            )


def file_folder_sharing_difference(collection, snapshot):
    path = list()
    files = list()
    folders = list()
    for file in colletion[snapshot]:
        if file[isFolder] is True:
            path.append(file[absoulte_path])

    for p in path:
        for f in collection[snapshot]:
            if f[absoulte_path] == p and f[isFolder] is False:
                files.append(f)
            if f[absoulte_path] == p and f[isFolder] is True:
                folders.append(f)
        for fold in folders:
            for fi in files:
                if fold[file_permissions] != fi[file_permissions]:
                    print(
                        "The file "
                        + fi[name]
                        + " has "
                        + fi[file_permission]
                        + " as its permissions while its folder "
                        + fold[name]
                        + " has "
                        + fold[file_permission]
                        + " as its permissions."
                    )
        files.clear()
        folders.clear()
