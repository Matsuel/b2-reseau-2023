import asyncio

async def sleep_and_print():
    for i in range(1,11):
        print(i)
        await asyncio.sleep(0.5)

loop = asyncio.get_event_loop()

tasks=[
    loop.create_task(sleep_and_print()),
    loop.create_task(sleep_and_print())
]

loop.run_until_complete(asyncio.wait(tasks))
loop.close()