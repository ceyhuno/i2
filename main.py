import ikea_api

constants = ikea_api.Constants(country="de", language="de")

print(f"constants {constants}")

token_endpoint = ikea_api.Auth(constants).get_guest_token()

ikea_api.run(token_endpoint)

print(f"token {token}")

cart = ikea_api.Cart(constants, token=token)

cart.add_items({"30403571": 1})  # { item_code: quantity }


order = ikea_api.OrderCapture(constants, token=token)

cart_show = run(cart.show())

items = ikea_api.convert_cart_to_checkout_items(cart_show)

checkout_id = run(order.get_checkout(items))

service_area_id = run(
    order.get_service_area(
        checkout_id,
        zip_code="10178",
    )
)

home_services = run(order.get_home_delivery_services(checkout_id, service_area_id))

collect_services = run(
    order.get_collect_delivery_services(checkout_id, service_area_id)
)

print(f"collect_services {collect_services}")


