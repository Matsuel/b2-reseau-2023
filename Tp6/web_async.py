import aiohttp
import aiofiles
import asyncio
import os
import sys

if len(sys.argv[1:])!=1:
    print("Usage: python3 web_sync.py <url>")
    sys.exit(1)

async def get_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def write_content(content,file):
    if os.name == "posix":
        if os.path.exists("/tmp/web_page"):
            os.chdir("/tmp/web_page")
        else:
            os.mkdir("/tmp/web_page")
            os.chdir("/tmp/web_page")
        f= await aiofiles.open(file, 'w', encoding="utf-8")
        await f.write(content)
    else:
        if os.path.exists("./Tp6/tmp/web_page"):
            os.chdir("./Tp6/tmp/web_page")
        else:
            os.mkdir("./Tp6/tmp")
            os.mkdir("./Tp6/tmp/web_page")
            os.chdir("./Tp6/tmp/web_page")
        f= await aiofiles.open(file, 'w', encoding="utf-8")
        await f.write(content)

if __name__ == "__main__":
    url = sys.argv[1]
    file_name = url.split(".")[1]+".html"
    print("Saving content to", file_name)
    print("Getting content from", url)
    asyncio.run(write_content(asyncio.run(get_content(url)),file_name))
    print("Done!")