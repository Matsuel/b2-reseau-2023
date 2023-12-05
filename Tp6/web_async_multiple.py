import sys
import os
import requests
import aiohttp
import aiofiles
import asyncio
import time

if len(sys.argv[1:])!=1:
    print("Usage: python3 web_sync.py <file_name>")
    sys.exit(1)

async def get_file_content(file_path):
    f = await aiofiles.open(file_path, "r", encoding="utf-8")
    return await f.read()

async def get_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def write_content(content,file):
    if os.name == "posix":
        tmp_dir = f"/tmp/web_{file}"
    else:
        tmp_dir = f"./Tp6/tmp/web_{file}"

    if not os.path.exists(tmp_dir.split('/')[0]):
        os.makedirs(tmp_dir)
    elif not os.path.exists('/'.join(tmp_dir.split('/')[1:])):
        os.makedirs('/'.join(tmp_dir.split('/')[1:]))
    elif not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    os.chdir(tmp_dir)
    
    f= await aiofiles.open(file+".html","w", encoding="utf-8")
    await f.write(content)
    await f.close()

    os.chdir("../../..")
    

if __name__ == "__main__":
    startTime= time.time()
    file_path = sys.argv[1]
    sites= asyncio.run(get_file_content(file_path))
    for site in sites.split("\n"):
        file_name = site.split(".")[1]
        print(file_name)
        asyncio.run(write_content(asyncio.run(get_content(site)),file_name))
    print(f"Done! In {time.time()-startTime} seconds")