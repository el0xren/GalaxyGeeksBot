from tg_bot.modules.ci.projects.aosp.project import AOSPProject
from tg_bot.modules.ci.projects.aosp.projects.projectfluid import common

project = AOSPProject(
	name = common.name,
	version = "11.0",
	android_version = "11",
	category = common.category,
	lunch_prefix = common.lunch_prefix,
	lunch_suffix = common.lunch_suffix,
	build_target = common.build_target,
	artifacts = common.artifacts
)
