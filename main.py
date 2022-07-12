import ikea_api
from ikea_api.wrappers.parsers.order_capture import parse_delivery_services
import requests
import os

bot_token = os.getenv('T')
bot_chatID = os.getenv('C')
item_id = os.getenv('P')
zip_code = os.getenv('Z')

def telegram_bot_sendtext(bot_message):
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
   response = requests.get(send_text)
   return response.json()

constants = ikea_api.Constants(country="de", language="de")

# Stock
stock = ikea_api.Stock(constants)
res = ikea_api.run(stock.get_stock(item_id))
availableCC = [p for p in res['availabilities'] if (p['availableForCashCarry'] or p['availableForClickCollect']) and p['classUnitKey']['classUnitCode'] in ['324','394','421','129']]
if availableCC:
    telegram_bot_sendtext(f"🎉 Available CashCarry,ClickCollect: https://www.ikea.com/de/de/search/products/?q=${item_id}")

token_endpoint = ikea_api.Auth(constants).get_guest_token()

token = ikea_api.run(token_endpoint)

cart = ikea_api.Cart(constants, token=token)

add_items_endpoint = cart.add_items({item_id: 1})  # { item_code: quantity }

ikea_api.run(add_items_endpoint)

order = ikea_api.OrderCapture(constants, token=token)

cart_show = ikea_api.run(cart.show())

items = ikea_api.convert_cart_to_checkout_items(cart_show)

checkout_id = ikea_api.run(order.get_checkout(items))

service_area_id = ikea_api.run(
    order.get_service_area(
        checkout_id,
        zip_code=zip_code,
    )
)

home_services = ikea_api.run(order.get_home_delivery_services(checkout_id, service_area_id))

collect_services = ikea_api.run(order.get_collect_delivery_services(checkout_id, service_area_id))

parsed_data = parse_delivery_services(
    constants=constants,
    home_response=home_services,
    collect_response=collect_services,
)

available = [p for p in parsed_data if p.is_available == True]

home = [p for p in available if "HOME_DELIVERY" in p.type]
collect = [p for p in available if "CLICK_COLLECT_STORE" in p.type and p.service_provider in ['STO324@IKEASTORE_DE','STO394@IKEASTORE_DE','STO421@IKEASTORE_DE','STO129@IKEASTORE_DE',]]

if home or collect:
    telegram_bot_sendtext(f"🎉 Available: https://www.ikea.com/de/de/search/products/?q=${item_id}")
