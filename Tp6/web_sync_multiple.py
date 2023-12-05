import sys
import os
import requests
import time 

if len(sys.argv[1:])!=1:
    print("Usage: python3 web_sync.py <file_name>")
    sys.exit(1)

def get_file_content(file_path):
    f = open(file_path, "r", encoding="utf-8")
    return f.read()

def get_content(url):
    request = requests.get(url)
    return request.text

def write_content(content,file):
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
    
    f= open(file+".html","w", encoding="utf-8")
    f.write(content)
    f.close()

    os.chdir("../../..")
    

if __name__ == "__main__":
    startTime= time.time()
    file_path = sys.argv[1]
    sites= get_file_content(file_path)
    for site in sites.split("\n"):
        file_name = site.split(".")[1]
        print(file_name)
        write_content(get_content(site),file_name)
    print(f"Done! In {time.time()-startTime} seconds")