from models.workspace_model import WorkspaceBase


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdate(WorkspaceBase):
    pass


class WorkspaceRead(WorkspaceBase):
    id: int

