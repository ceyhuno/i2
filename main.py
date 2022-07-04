import ikea_api
import asyncio

constants = ikea_api.Constants(country="de", language="de")

print(f"constants {constants}")

token_endpoint = ikea_api.Auth(constants).get_guest_token()

token = ikea_api.run(token_endpoint)

print(f"token {token}")



async def main():
    services = await ikea_api.get_delivery_services(
        constants=constants,
        token=...,
        items={
            "30403571": 1,
        },
        zip_code="10178",
    )
    print(f"services {services}")

if __name__ ==  '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())



