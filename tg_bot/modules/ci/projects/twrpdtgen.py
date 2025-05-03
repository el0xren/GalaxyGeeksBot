from git.exc import GitCommandError
from github import Github, GithubException
from tg_bot import get_config
from pathlib import Path
import requests
from telegram import Update
from telegram.ext import CallbackContext
from tempfile import TemporaryDirectory
from twrpdtgen.device_tree import DeviceTree
from twrpdtgen.info_extractors.buildprop import PARTITIONS

BUILD_DESCRIPTION = ["ro.build.description"] + [
    f"ro.{partition}.build.description" for partition in PARTITIONS
]


def ci_build(update: Update, context: CallbackContext):
    status_message = update.message.reply_text("Downloading file...")

    # Download file
    tempdir = TemporaryDirectory()
    path = Path(tempdir.name)
    url = update.message.text.split()[2]
    file = path / "recovery.img"
    open(file, "wb").write(requests.get(url, allow_redirects=True).content)

    # Generate device tree
    status_message.edit_text("Generating device tree...")
    try:
        devicetree = DeviceTree(path / "working", recovery_image=file)
    except Exception as e:
        status_message.edit_text("Device tree generation failed\n"
                                 f"Error: {e}")
        return

    try:
        build_description = devicetree.build_prop_reader.get_prop(
            BUILD_DESCRIPTION, "build description")
        branch = build_description.replace(" ", "-")
    except AssertionError:
        status_message.edit_text("Failed to get build description prop")
        return

    # Upload to GitHub
    status_message.edit_text("Pushing to GitHub...")
    gh_username = get_config("CI_GITHUB_USERNAME")
    gh_token = get_config("CI_GITHUB_TOKEN")
    gh_org_name = get_config("CI_TWRPDTGEN_GITHUB_ORG")
    repo_name = f"android_device_{devicetree.manufacturer}_{devicetree.codename}"
    git_repo_url = (
        f"https://{gh_username}:{gh_token}@github.com/{gh_org_name}/{repo_name}"
    )

    # Get organization
    try:
        gh = Github(gh_token)
        gh_org = gh.get_organization(gh_org_name)
    except GithubException as error:
        status_message.edit_text(f"Failed to get organization\n"
                                 f"Error: {error}")
        return

    # Create repo if needed
    status_message.edit_text("Creating repo if needed...")
    try:
        devicetree_repo = gh_org.create_repo(name=repo_name,
                                             private=False,
                                             auto_init=False)
    except GithubException as error:
        if error.status != 422:
            status_message.edit_text("Repo creation failed\n"
                                     f"Error: {error.status} {error}")
            return
        devicetree_repo = gh_org.get_repo(name=repo_name)

    status_message.edit_text("Pushing...")
    try:
        devicetree.git_repo.git.push(git_repo_url, f"HEAD:refs/heads/{branch}")
        devicetree_repo.edit(default_branch=branch)
    except GitCommandError:
        status_message.edit_text(f"Error: Push to remote failed!")
        return

    status_message.edit_text("Done")

    channel_id = get_config("CI_TWRPDTGEN_CHANNEL_ID")
    context.bot.send_message(
        channel_id,
        "TWRP device tree generated\n"
        f"Codename: {devicetree.codename}\n"
        f"Manufacturer: {devicetree.manufacturer}\n"
        f"Build description: {build_description}\n"
        f"Device tree: {devicetree_repo.html_url}/tree/{branch}",
        disable_web_page_preview=True,
    )
