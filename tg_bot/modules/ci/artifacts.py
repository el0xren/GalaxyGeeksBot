from pathlib import Path

STATUS_ON_QUEUE = "On queue"
STATUS_UPLOADING = "Uploading"
STATUS_UPLOADED = "Uploaded"
STATUS_NOT_UPLOADED = "Error while uploading"


class Artifact:
    """
    This class represent an artifact.
    """

    def __init__(self, path: Path):
        """
        Initialize the artifact.
        """
        self.name = path.name
        self.path = path
        self.status = "On queue"


class Artifacts:
    """
    This class represent a lost of artifacts.
    """

    def __init__(self, path: Path, pattern: str):
        """
        Find the artifacts.
        """
        self.pattern = pattern
        self.path = path

        self.artifacts = [
            Artifact(artifact) for artifact in list(path.glob(pattern))
        ]

    def get_artifacts_on_status(self, status: str):
        return [i for i in self.artifacts if i.status == status]

    def get_readable_artifacts_list(self):
        artifact_total = len(self.artifacts)
        artifact_uploaded = len(self.get_artifacts_on_status(STATUS_UPLOADED))

        text = f"Uploaded {artifact_uploaded} out of {artifact_total} artifact(s)\n"
        for artifact in self.artifacts:
            text += f"{self.artifacts.index(artifact) + 1}) {artifact.name}: {artifact.status}\n"
        return text
