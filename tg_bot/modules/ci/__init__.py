from tg_bot import get_config
from tg_bot.core.logging import LOGE, LOGI
from tg_bot.modules.ci.parser import CIParser
from importlib import import_module
from telegram.ext import CallbackContext
from telegram import Update
from tg_bot.core.permissions import authorized


@authorized
def ci(update: Update, context: CallbackContext):
    if get_config("CI_CHANNEL_ID") == "":
        update.message.reply_text("Error: CI channel or user ID not defined.")
        LOGE("CI channel or user ID not defined.")
        return

    parser = CIParser(prog="/ci")
    parser.set_output(update.message.reply_text)
    parser.add_argument("project", help="CI project")

    args_passed = update.message.text[len("/ci"):].split()
    args, _ = parser.parse_known_args(args_passed)

    try:
        project_module = import_module("tg_bot.modules.ci.projects." +
                                       args.project,
                                       package="*")
    except ImportError:
        update.message.reply_text("Error: Project script not found.")
        return

    LOGI(f"CI workflow started, project: {args.project}")
    project_module.ci_build(update, context)
    LOGI(f"CI workflow finished, project: {args.project}")


commands = {ci: ["ci"]}
