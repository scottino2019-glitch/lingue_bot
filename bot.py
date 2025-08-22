import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("7269524372:AAG5im_qPsx2vetXav_J0xH8sUKtdWTbe44")  # prende il token da Heroku

# Lingue con emoji
LANGUAGES = {
    "ar": "🇸🇦 Arabo",
    "ru": "🇷🇺 Russo",
    "ja": "🇯🇵 Giapponese",
    "ko": "🇰🇷 Coreano",
    "tr": "🇹🇷 Turco",
    "zh": "🇨🇳 Cinese",
    "fr": "🇫🇷 Francese"  # Coming soon
}

# App per lingua con emoji
APPS = {
    "ar": {"📖 Lezioni": "https://t.me/lingue_bot/lezioniarabo",
           "🔤 Alfabeto": "https://t.me/lingue_bot/arabo"},
    "ru": {"📖 Lezioni": "https://t.me/lingue_bot/lezionirusso",
           "🔤 Alfabeto": "https://t.me/lingue_bot/alfabetorusso"},
    "ja": {"🔤 Alfabeto": "https://t.me/lingue_bot/giapponese",
           "📖 Lezioni": "https://t.me/lingue_bot/lezionigiapponese",
           "✍️ Scrittura": "https://t.me/lingue_bot/scritturagiapponese"},
    "ko": {"📖 Lezioni": "https://t.me/lingue_bot/lezionecoreano",
           "🔤 Hangul": "https://t.me/lingue_bot/hangul",
           "🔤 Alfabeto": "https://t.me/lingue_bot/alfabetohangul"},
    "tr": {"📖 Lezioni": "https://t.me/lingue_bot/lezioniturco"},
    "zh": {"📖 Lezioni": "https://t.me/lingue_bot/Chinese",
           "🈶 Ideogrammi": "https://t.me/lingue_bot/ideogrammi"},
    "fr": {}  # Coming soon
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(name, callback_data=f"lang_{code}")]
                for code, name in LANGUAGES.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🌐 Seleziona la lingua:", reply_markup=reply_markup)

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("lang_"):
        lang_code = data.split("_")[1]
        context.user_data['lang'] = lang_code
        apps = APPS.get(lang_code, {})
        keyboard = []
        if apps:
            for app_name in apps.keys():
                keyboard.append([InlineKeyboardButton(app_name, callback_data=f"app_{app_name}")])
        else:
            keyboard.append([InlineKeyboardButton("⏳ Coming soon", callback_data="coming_soon")])
        keyboard.append([InlineKeyboardButton("⬅️ Indietro", callback_data="back_lang")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"Hai scelto: {LANGUAGES[lang_code]}\nSeleziona l'app:", reply_markup=reply_markup)

    elif data.startswith("app_"):
        app_name = data.split("_", 1)[1]
        lang_code = context.user_data.get('lang')
        link = APPS.get(lang_code, {}).get(app_name)
        if link:
            await query.edit_message_text(f"{app_name}: {link}")
        else:
            await query.edit_message_text(f"{app_name} non è ancora disponibile.")
        keyboard = [[InlineKeyboardButton("⬅️ Torna al menu app", callback_data=f"lang_{lang_code}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Se vuoi tornare al menu app:", reply_markup=reply_markup)

    elif data == "coming_soon":
        await query.edit_message_text("⏳ Questa lingua o app sarà disponibile presto!")
        keyboard = [[InlineKeyboardButton("⬅️ Indietro", callback_data="back_lang")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Torna indietro:", reply_markup=reply_markup)

    elif data == "back_lang":
        keyboard = [[InlineKeyboardButton(name, callback_data=f"lang_{code}")]
                    for code, name in LANGUAGES.items()]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🌐 Seleziona la lingua:", reply_markup=reply_markup)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(menu_callback))
    print("Bot avviato...")
    app.run_polling()

if __name__ == "__main__":
    main()


