from pydantic import BaseModel


class DeleteFileSnapshotBody(BaseModel):
    snapshot_name: str


class PutFileSnapshotBody(BaseModel):
    snapshot_name: str
    new_snapshot_name: str


class PostFileSnapshotBody(BaseModel):
    snapshot_name: str
