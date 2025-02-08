import nest_asyncio
nest_asyncio.apply()

import asyncio
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# تنظیم لاگ‌ها
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

# توکن ربات تلگرام شما
API_TOKEN = "========"

# آدرس API بایننس برای دریافت قیمت ارز دیجیتال
BINANCE_API_URL = 'https://api.binance.com/api/v3/ticker/price?symbol={}'

def get_price(symbol: str) -> str:
    """
    دریافت قیمت ارز دیجیتال از API بایننس
    """
    try:
        response = requests.get(BINANCE_API_URL.format(symbol))
        response.raise_for_status()
        data = response.json()
        return data.get('price')
    except Exception as e:
        logging.error(f"خطا در دریافت قیمت برای {symbol}: {e}")
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    فرمان /start برای شروع کار با ربات
    """
    await update.message.reply_text(
        "سلام! من ربات قیمت ارزهای دیجیتال هستم.\n"
        "برای دریافت قیمت یک ارز از دستور /price استفاده کنید.\n"
        "مثال: /price ETHUSDT"
    )

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    فرمان /price برای دریافت قیمت ارز
    """
    if context.args:
        symbol = context.args[0].upper()
    else:
        symbol = 'BTCUSDT'  # پیش‌فرض: BTCUSDT
    price_value = get_price(symbol)
    if price_value:
        await update.message.reply_text(f"قیمت {symbol} برابر است با: {price_value} دلار")
    else:
        await update.message.reply_text("مشکلی در دریافت قیمت به وجود آمده است.")

async def main():
    """
    تابع اصلی برای ساخت و اجرای ربات
    """
    # ساخت Application با توکن ربات
    app = ApplicationBuilder().token(API_TOKEN).build()

    # ثبت handlerها برای فرمان‌های /start و /price
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))

    # شروع polling برای دریافت پیام‌ها
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
