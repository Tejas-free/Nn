import asyncio
import secrets
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Configuration
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
ADMIN_USER_ID = 1441704343  # Replace with your admin user ID
approved_users = {}  # Dictionary of approved users and their expiration times
active_attack = None
saved_attacks = []  # List to store saved attack details
generated_keys = {}  # Dictionary to store keys with custom text

async def start(update: Update, context: CallbackContext):
    """Welcome message."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if user_id not in approved_users or approved_users[user_id] < datetime.now():
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "⛔ **Access Denied!**\n\n"
                "🚨 You are not approved to use this bot.\n"
                "📩 Please contact the admin: [@madhursaini7](https://t.me/madhursaini7)"
            ),
            parse_mode="Markdown",
        )
        return

    message = (
        "🔥 **Welcome to LEGEND Bot!** 🔥\n\n"
        "🛠 **Available Commands:**\n"
        "💥 `/attack <ip> <port>`: Launch a simulated attack\n"
        "📜 `/rules`: View rules like '30-40 kills'\n"
        "📝 `/save <attack details>`: Save attack details\n"
        "🔑 `/genkey <custom text>`: Generate a custom access key\n"
        "✅ `/approve <user_id> <days>`: Approve user access (Admin only)\n\n"
        "💬 **Admin Contact:** [@madhursaini7](https://t.me/madhursaini7)\n"
        "✨ Let the legendary battle begin! 🚀"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")

async def approve(update: Update, context: CallbackContext):
    """Approve a user to use the bot."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await context.bot.send_message(
            chat_id=chat_id, text="⛔ Only the admin can approve users.", parse_mode="Markdown"
        )
        return

    if len(context.args) != 2:
        await context.bot.send_message(
            chat_id=chat_id, text="⚠️ Usage: `/approve <user_id> <days>`", parse_mode="Markdown"
        )
        return

    try:
        target_user_id = int(context.args[0])
        days = int(context.args[1])
        expiration_time = datetime.now() + timedelta(days=days)
        approved_users[target_user_id] = expiration_time
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"✅ User `{target_user_id}` has been approved for {days} days! 🎉",
            parse_mode="Markdown",
        )
    except ValueError:
        await context.bot.send_message(
            chat_id=chat_id, text="❌ Invalid user ID or days.", parse_mode="Markdown"
        )

async def genkey(update: Update, context: CallbackContext):
    """Generate a custom access key."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await context.bot.send_message(
            chat_id=chat_id, text="⛔ Only the admin can generate keys.", parse_mode="Markdown"
        )
        return

    if len(context.args) < 1:
        await context.bot.send_message(
            chat_id=chat_id, text="⚠️ Usage: `/genkey <custom_text>`", parse_mode="Markdown"
        )
        return

    custom_text = " ".join(context.args)
    key = secrets.token_hex(8)  # Generate a random key
    generated_keys[key] = custom_text

    await context.bot.send_message(
        chat_id=chat_id,
        text=f"🔑 **Key Generated!**\n`{key}`\n📝 Description: {custom_text} ✨",
        parse_mode="Markdown",
    )

async def attack(update: Update, context: CallbackContext):
    """Handle the /attack command."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if user_id not in approved_users or approved_users[user_id] < datetime.now():
        await context.bot.send_message(
            chat_id=chat_id,
            text="❌ You are not authorized to use this command. Please contact the admin. 🚨",
            parse_mode="Markdown",
        )
        return

    if len(context.args) != 2:
        await context.bot.send_message(
            chat_id=chat_id,
            text="⚠️ Usage: `/attack <ip> <port>`",
            parse_mode="Markdown",
        )
        return

    ip, port = context.args
    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            f"🚀 **Attack Launched!** 🔥\n"
            f"🌐 **Target:** `{ip}:{port}`\n"
            f"⚔️ Prepare for the legendary battle! 🛡️"
        ),
        parse_mode="Markdown",
    )

async def rules(update: Update, context: CallbackContext):
    """Display the rules."""
    chat_id = update.effective_chat.id
    message = (
        "📜 **Rules of Engagement:**\n"
        "1️⃣ Respect the legend's command structure.\n"
        "2️⃣ Maintain 30-40 'kills' for operational effectiveness.\n"
        "3️⃣ Unauthorized access will result in a permanent ban.\n"
        "4️⃣ **Contact Admin for Support:** [@madhursaini7](https://t.me/madhursaini7)\n\n"
        "⚔️ **Stay Legendary!** 💪"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")

async def save(update: Update, context: CallbackContext):
    """Save attack details."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if user_id not in approved_users or approved_users[user_id] < datetime.now():
        await context.bot.send_message(
            chat_id=chat_id,
            text="❌ You are not authorized to use this command. Please contact the admin. 🚨",
            parse_mode="Markdown",
        )
        return

    attack_details = " ".join(context.args)
    if not attack_details:
        await context.bot.send_message(
            chat_id=chat_id, text="⚠️ Usage: `/save <attack details>`", parse_mode="Markdown"
        )
        return

    saved_attacks.append(attack_details)
    await context.bot.send_message(
        chat_id=chat_id,
        text=f"✅ **Attack Details Saved!**\n📄 `{attack_details}`",
        parse_mode="Markdown",
    )

if __name__ == "__main__":
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("approve", approve))
    application.add_handler(CommandHandler("genkey", genkey))
    application.add_handler(CommandHandler("attack", attack))
    application.add_handler(CommandHandler("rules", rules))
    application.add_handler(CommandHandler("save", save))

    print("🔥 LEGEND Bot is running!")
    application.run_polling()