# Return codes
(
	SUCCESS,
	MISSING_ARGS,
	MISSING_DIR,
	LUNCH_FAILED,
	CLEAN_FAILED,
	BUILD_FAILED,
) = range(6)

ERROR_CODES = {
	SUCCESS: "Build completed successfully",
	MISSING_ARGS: "Build failed: Missing arguments",
	MISSING_DIR: "Build failed: Project dir doesn't exists",
	LUNCH_FAILED: "Build failed: Lunching failed",
	CLEAN_FAILED: "Build failed: Cleaning failed",
	BUILD_FAILED: "Build failed: Building failed"
}

NEEDS_LOGS_UPLOAD = {
	LUNCH_FAILED: "lunch_log.txt",
	CLEAN_FAILED: "clean_log.txt",
	BUILD_FAILED: "build_log.txt"
}
