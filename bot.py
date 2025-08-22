import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Legge il token dalla variabile d'ambiente
TOKEN = os.environ.get("7269524372:AAEPh9Um53lP13aPOdDtET-QSFNJV3Lkr_M")
if not TOKEN:
    raise ValueError("BOT_TOKEN non impostato! Controlla le variabili d'ambiente.")

# Dizionario lingue e relative app
LANGUAGES = {
    "Arabo": [
        ("Lezioni", "https://t.me/lingue_bot/lezioniarabo"),
        ("Alfabeto", "https://t.me/lingue_bot/arabo")
    ],
    "Russo": [
        ("Lezioni", "https://t.me/lingue_bot/lezionirusso"),
        ("Alfabeto", "https://t.me/lingue_bot/alfabetorusso")
    ],
    "Giapponese": [
        ("Alfabeto", "https://t.me/lingue_bot/giapponese"),
        ("Lezioni", "https://t.me/lingue_bot/lezionigiapponese"),
        ("Scrittura", "https://t.me/lingue_bot/scritturagiapponese")
    ],
    "Coreano": [
        ("Lezioni", "https://t.me/lingue_bot/lezionecoreano"),
        ("Hangul", "https://t.me/lingue_bot/hangul"),
        ("Alfabeto", "https://t.me/lingue_bot/alfabetohangul")
    ],
    "Turco": [
        ("Lezioni", "https://t.me/lingue_bot/lezioniturco")
    ],
    "Cinese": [
        ("Lezioni", "https://t.me/lingue_bot/Chinese"),
        ("Ideogrammi", "https://t.me/lingue_bot/ideogrammi")
    ]
}

# Funzione /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(lang, callback_data=f"lang_{lang}")] for lang in LANGUAGES.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Benvenuto! Scegli la lingua:", reply_markup=reply_markup)

# Gestione dei pulsanti
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("lang_"):
        lang = data[5:]
        apps = LANGUAGES.get(lang, [])
        keyboard = [[InlineKeyboardButton(app_name, url=url)] for app_name, url in apps]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"App disponibili per {lang}:", reply_markup=reply_markup)

# Crea l'applicazione e aggiunge i gestori
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

# Avvia il bot
print("Bot avviato...")
app.run_polling()
