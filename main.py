import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# Aktifkan logging untuk debugging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Simpan transaksi sementara di memori
saldo = 0
transaksi = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Ini adalah bot pencatat keuangan. Gunakan /masuk, /keluar, dan /saldo.")

async def masuk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global saldo
    try:
        jumlah = int(context.args[0])
        catatan = ' '.join(context.args[1:])
        saldo += jumlah
        transaksi.append(f"+{jumlah}: {catatan}")
        await update.message.reply_text(f"Pemasukan dicatat: +{jumlah}\nSaldo sekarang: {saldo}")
    except:
        await update.message.reply_text("Format salah. Gunakan: /masuk [jumlah] [catatan]")

async def keluar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global saldo
    try:
        jumlah = int(context.args[0])
        catatan = ' '.join(context.args[1:])
        saldo -= jumlah
        transaksi.append(f"-{jumlah}: {catatan}")
        await update.message.reply_text(f"Pengeluaran dicatat: -{jumlah}\nSaldo sekarang: {saldo}")
    except:
        await update.message.reply_text("Format salah. Gunakan: /keluar [jumlah] [catatan]")

async def cek_saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Saldo saat ini: {saldo}")

app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("masuk", masuk))
app.add_handler(CommandHandler("keluar", keluar))
app.add_handler(CommandHandler("saldo", cek_saldo))

if __name__ == '__main__':
    app.run_polling()
