import telebot
import requests

TOKEN = "8360480762:AAGZ9TGHm4y_ppEsbgsGAjn7sgMWiGdJCaQ"

bot = telebot.TeleBot(TOKEN)



def get_price(symbol):
    url = "https://api.bybit.com/v5/market/tickers"
    params = {
    "category": "spot",
    "symbol": symbol.upper() + "USDT"
    }

    try:
        r = requests.get(url, params=params).json()
        data = r["result"]["list"][0]

        price = float(data["lastPrice"])
        change = float(data["price24hPcnt"]) * 100

        return price, change
    except:
        return None, None


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Напиши /price BTC\n/help - все команды")


@bot.message_handler(commands=['price'])
def price(message):
    try:
        coin = message.text.split()[1].upper()
        price, change = get_price(coin)

        if price:
            bot.send_message(
            message.chat.id,
            f"{coin}/USDT\nЦена: ${price}\nИзменение 24ч: {change:.2f}%"
            )
        else:
            bot.send_message(message.chat.id, "Монета не найдена")
    except:
        bot.send_message(message.chat.id, "Пример: /price BTC")

@bot.message_handler(commands=['chart'])
def chart(message):
    try:
        coin = message.text.split()[1].upper()
        chart_url = f"https://www.tradingview.com/chart/?symbol={coin}USDT"
        bot.send_message(message.chat.id, f"График {coin}/USDT:\n{chart_url}")
    except:
        bot.send_message(message.chat.id, "Пример: /chart BTC")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f"Команды:\n/start\n/price 'coin'\n/chart 'coin'\n/help")

#print('bot workaet')
bot.polling(none_stop=True)