import requests
import re
import os
import datetime



# skip_list = [1113, 21, 76, 386, 613, 1012, 1088, 992, 637, 1106, 1105, 1084, 1158, 1159, 237, 979, 999, 225, 382, 75, 1009, 931, 1078, 1069, 220, 708, 197, 1100, 1082, 1017, 1015, 1187, 626, 1103, 1070, 1071, 370, 1004, 966, 555]
skip_list = []

def get_all():
    q_size = 500
    S = requests.Session()

    complete = False
    url = "https://coptr.digipres.org/api.php"

    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "allpages",
        "aplimit":q_size,

    }


    results = []

    R = S.get(url=url, params=PARAMS)
    data = R.json()
    try:
        results+=data['query']['allpages']
    except KeyError:
        print (data)
        quit()


    while not complete:    
        if 'continue' in data:
            PARAMS = {
            "action": "query",
            "format": "json",
            "list": "allpages",
            "aplimit":q_size,
            "apcontinue":data['continue']['apcontinue'],
            'continue':data['continue']['continue']}

        else:
            PARAMS = {
            "action": "query",
            "format": "json",
            "list": "allpages",
            "aplimit":q_size}

        R = S.get(url=url, params=PARAMS)
        data = R.json()
        
        try:
            results+=data['query']['allpages']
        except KeyError:
            print (data)
            quit("Quitting")

        if 'continue' not in data: 
            complete = True
    return results

def get_page(pageid):

    S = requests.Session()
    url = "https://coptr.digipres.org/api.php"
    PARAMS = {
        "action": "parse",
        "format": "json",
        "pageid":pageid}
    R = S.get(url=url, params=PARAMS)
    data = R.json()
    return data['parse']
  
def find_urls(string):
    string = string.decode()

    print ()
    print ()
    print ()
    print ()
    print ()
    print ()
    # print (string)
    # quit()
    # regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    
    regex = r'^(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?$' 
    url = re.findall(regex,string)      
    return [x[0] for x in url]

def check_url(url):
    try:
        r = requests.get(url)
        return r.status_code
    except:
        return "Bad response - worth checking"

if os.path.exists(r"\\wlgprdfile12\home$\Wellington\GattusoJ\HomeData\Desktop\copter_done_file.txt"):
    with open(r"\\wlgprdfile12\home$\Wellington\GattusoJ\HomeData\Desktop\copter_done_file.txt") as data:
        done = [int(x) for x in data.read().split("\n") if x != ""] 
else:
    done = []

print (f"Processed: {len(done)} pages")
results = get_all()

for r in results:
    pageid = r["pageid"]
    ns = r["ns"] 
    title = r["title"]
    print (f"\nWorking on page: {pageid}")
    print (title)
    print (datetime.datetime.now())
    print ()

    if pageid in skip_list:
        page_json = get_page(pageid)
        links = find_urls(page_json['text']['*'].encode("utf-8"))
        print ("Got links")
        links = [x for x in links if not x.startswith("index.php")]
        links = list(set(links))
        for url in links:
            #### forcing the issue of no schema urls. Assumes https. 
            if not url.startswith("http"):
                url = "https://www."+url

            response = check_url(url)
            print ("\t", url, response)
            row = [str(pageid), title, url, str(response)]
            with open(r"\\wlgprdfile12\home$\Wellington\GattusoJ\HomeData\Desktop\url_logger.txt", "a", encoding="utf-8") as data:
                data.write("|".join(row)+"\n")

    if pageid not in done and pageid not in skip_list:
        page_json = get_page(pageid)
        links = find_urls(page_json['text']['*'].encode("utf-8"))
        print ("Got links")
        links = [x for x in links if not x.startswith("index.php")]
        links += page_json["externallinks"]
        links = list(set(links))
        for url in links:
            #### forcing the issue of no schema urls. Assumes https. 
            if not url.startswith("http"):
                url = "https://www."+url

            response = check_url(url)
            print ("\t", url, response)
            row = [str(pageid), title, url, str(response)]
            with open(r"\\wlgprdfile12\home$\Wellington\GattusoJ\HomeData\Desktop\url_logger.txt", "a", encoding="utf-8") as data:
                data.write("|".join(row)+"\n")
        
        with open(r"\\wlgprdfile12\home$\Wellington\GattusoJ\HomeData\Desktop\copter_done_file.txt", "a", encoding="utf-8") as data:
            data.write(f"{pageid}\n")

    if pageid in skip_list and pageid not in done:
        page_json = get_page(pageid)
        links = page_json["externallinks"]
        print ("Using external links only")
        links = list(set(links))
        for url in links:
            #### forcing the issue of no schema urls. Assumes https. 
            if not url.startswith("http"):
                url = "https://www."+url

            response = check_url(url)
            print ("\t", url, response)
            row = [str(pageid), title, url, str(response)]
            with open(r"\\wlgprdfile12\home$\Wellington\GattusoJ\HomeData\Desktop\url_logger.txt", "a", encoding="utf-8") as data:
                data.write("|".join(row)+"\n")
        
        with open(r"\\wlgprdfile12\home$\Wellington\GattusoJ\HomeData\Desktop\copter_done_file.txt", "a", encoding="utf-8") as data:
            data.write(f"{pageid}\n")
