def exit(update,context):
    update.message.reply_text("Exitting now...")
    exit()
    
commands = {
	exit: ['exit']
}
