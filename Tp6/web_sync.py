import sys
import os
import requests

if len(sys.argv[1:])!=1:
    print("Usage: python3 web_sync.py <url>")
    sys.exit(1)

def get_content(url):
    request = requests.get(url)
    return request.text

def write_content(content,file):
    if os.name == "posix":
        if os.path.exists("/tmp/web_page"):
            os.chdir("/tmp/web_page")
        else:
            os.mkdir("/tmp/web_page")
            os.chdir("/tmp/web_page")
        f= open(file,"w+", encoding="utf-8")
        f.write(content)
        f.close()
    else:
        if os.path.exists("./Tp6/web_page"):
            os.chdir("./Tp6/web_page")
        else:
            os.mkdir("./Tp6/web_page")
            os.chdir("./Tp6/web_page")
        f= open(file,"w", encoding="utf-8")
        f.write(content)
        f.close()


if __name__ == "__main__":
    url = sys.argv[1]
    file_name = url.split("/")[-1].split('.')[1]+".html" if url[-1]!="/" else url.split("/")[-2].split('.')[1]+".html"
    print("Saving content to", file_name)
    print("Getting content from", url)
    write_content(get_content(url),file_name)
    print("Done!")