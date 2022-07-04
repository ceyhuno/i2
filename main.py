import ikea_api

constants = ikea_api.Constants(country="de", language="de")

token = ikea_api.Auth(constants).get_guest_token()

import asyncio

async def function(param) -> asyncio.coroutine:
    services = await ikea_api.get_delivery_services(
        constants=constants,
        token=token,
        items={
            "30457903": 1,
            "11111111": 2,  # invalid item that will be skipped
        },
        zip_code="101000",
    )
    print(f"services.delivery_options {services.delivery_options}")
    print(f"services.cannot_add {services.cannot_add}")


asyncio.run(function(whatever))

