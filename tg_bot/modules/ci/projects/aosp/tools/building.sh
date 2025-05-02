#!/bin/bash

# Set return codes
STATUS=(
	"SUCCESS"
	"MISSING_ARGS"
	"MISSING_DIR"
	"LUNCH_FAILED"
	"CLEAN_FAILED"
	"BUILD_FAILED"
)

status_len="$((${#STATUS[@]} - 1))"
for returncode in $(seq 0 "${status_len}"); do
	eval "${STATUS[${returncode}]}"="${returncode}"
done

# Parse arguments passed by the ROM or recovery's script
while [ "${#}" -gt 0 ]; do
	case "${1}" in
		--sources )
			CI_SOURCES="${2}"
			shift
			;;
		--lunch_prefix )
			CI_LUNCH_PREFIX="${2}"
			shift
			;;
		--lunch_suffix )
			CI_LUNCH_SUFFIX="${2}"
			shift
			;;
		--build_target )
			CI_BUILD_TARGET="${2}"
			shift
			;;
		--clean )
			CI_CLEAN="${2}"
			shift
			;;
		--device )
			CI_DEVICE="${2}"
			shift
			;;
	esac
	shift
done

if [ "${CI_DEVICE}" = "" ]; then
	exit "${MISSING_ARGS}"
fi

if [ ! -d "${CI_SOURCES}" ]; then
	exit "${MISSING_DIR}"
fi

cd "${CI_SOURCES}"
. build/envsetup.sh

lunch "${CI_LUNCH_PREFIX}_${CI_DEVICE}-${CI_LUNCH_SUFFIX}" &> lunch_log.txt
CI_LUNCH_STATUS=$?
if [ "${CI_LUNCH_STATUS}" != 0 ]; then
	exit "${LUNCH_FAILED}"
fi

if [ "${CI_CLEAN}" != "" ] && [ "${CI_CLEAN}" != "none" ]; then
	mka "${CI_CLEAN}" &> clean_log.txt
	CI_CLEAN_STATUS=$?
	if [ "${CI_CLEAN_STATUS}" != 0 ]; then
		exit "${CLEAN_FAILED}"
	fi
fi

mka "${CI_BUILD_TARGET}" "-j$(nproc --all)" &> build_log.txt
CI_BUILD_STATUS=$?
if [ ${CI_BUILD_STATUS} != 0 ]; then
	exit "${BUILD_FAILED}"
fi

exit "${SUCCESS}"
