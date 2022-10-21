import pymongo
from app.micro_apps.auth.endpoints.models.user import User
import app.micro_apps.snapshot.services.models.files
import app.micro_apps.snapshot.services.database


def query_by_drive(drive: str):
    return my_collection.find({driveId: drive})


def query_by_owner(user: str):
    return my_collection.find({owners: {emailAddress: user}})


def query_by_creator(user: str):
    return my_collection.find({owners: {emailAddress: user}})


def query_by_from(user: str):
    return my_collection.find({owners: {emailAddress: user}})


def query_by_to(user: str):
    return my_collection.find(
        {
            sharingUser: {
                emailAddress: user,
                permissions: {permissionDetails: {permissionType: "direct"}},
            }
        }
    )


def query_by_readable(user):
    return my_collection.find(
        {contentRestrictions: {readOnly: True, restrictingUser: user}}
    )


def query_by_writable(user):
    return my_collection.find(
        {contentRestrictions: {readOnly: False, restrictingUser: user}}
    )


def query_by_sharable(user):
    return my_collection.find({owners: {emailAddress: user}})


def query_by_name(name: str):
    return my_collection.find({name: {"$regex": name}})


def query_by_inFolder(folder: str):
    return my_collection.find({parents: {"$regex": folder}})


def query_by_folder(folder: str):
    return my_collection.find({parents: {"$regex": folder}})


def query_by_path(path: str, drive: str):
    return my_collection.find({spaces: path, driveId: drive})


def query_by_sharing_none():
    return my_collection.find({shared: False})


def query_by_sharing_anyone():
    return my_collection.find({shared: True})


def query_by_sharing_individual(user: str):
    return my_collection.find({sharingUser: {emailAddress: user}})


def query_by_sharing_domain(domains: str):
    return my_collection.find({shared: True, permissions: {domain: domains}})


# def query_by_group_off():
