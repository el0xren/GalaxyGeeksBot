class AOSPProject:
    """
    This class represent an AOSP project.
    """

    def __init__(
        self,
        name,
        version,
        android_version,
        category,
        lunch_prefix,
        lunch_suffix,
        build_target,
        artifacts,
    ):
        """
        Fill the values.
        """
        # This value will also be used for folder name
        self.name = name
        # Version of the project
        self.version = version
        # Android version to display on Telegram post
        self.android_version = android_version
        # Name of the parent folder used when uploading
        self.category = category
        # These next 2 values are needed for lunch (e.g. "lineage"_whyred-"userdebug")
        self.lunch_prefix = lunch_prefix
        self.lunch_suffix = lunch_suffix
        # Target to build (e.g. to build a ROM's OTA package, use "bacon" or "otapackage", for a recovery project, use "recoveryimage")
        self.build_target = build_target
        # Filename of the output. You can also use wildcards if the name isn't fixed
        self.artifacts = artifacts
