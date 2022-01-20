import requests
import re

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

    pageid = 836
    S = requests.Session()
    url = "https://coptr.digipres.org/api.php"
    PARAMS = {
        "action": "parse",
        "format": "json",
        "pageid":pageid}
    R = S.get(url=url, params=PARAMS)
    data = R.json()
    data['parse']['text']['*'] = data['parse']['text']['*'].replace("\u2010", "-")

    return data['parse']


    # return data


  
def find_urls(string):
    string = string.decode()
    # string = string.encode("utf-8")
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)      
    return [x[0] for x in url]

def check_url(url):
    if not url.startswith("http"):
        url = "https://"+url 
    try:
        r = requests.get(url)
        return r.status_code
    except:
        return "Bad response from server"

def get_edit_token():

    # https://coptr.digipres.org/api.php?action=help&modules=edit

    # api.php?action=edit&title=Test&summary=test%20summary&text=article%20content&baserevid=1234567&token=123ABC 


    S = requests.Session()
    url = "https://coptr.digipres.org/api.php"
    PARAMS = {
        "action": "query",
        "meta": "tokens",
        "type": "login",
        "format": "json"
    }
    R = S.get(url=url, params=PARAMS)
    DATA = R.json()
    LOGIN_TOKEN = DATA['query']['tokens']['logintoken']
    return LOGIN_TOKEN
# print (get_edit_token())



results = get_all()

for r in results:
    pageid = r["pageid"]
    ns = r["ns"] 
    title = r["title"]

    page_json = get_page(pageid)
    
#     # ['title', 'pageid', 'revid', 'text', 'langlinks', 'categories', 'links', 'templates', 'images', 'externallinks', 'sections', 'parsewarnings', 'displaytitle', 'iwlinks', 'properties']
    links = list(set(find_urls(page_json['text']['*'].encode("utf-8"))))
    for url in links:
        print (url, check_url(url))

    quit()
    print (links)

    quit()
#     print (page_json['pageid'])
#     print (page_json['revid'])
#     print (page_json['text'])
#     print (page_json['langlinks'])
#     print (page_json['categories'])
#     print (page_json['links'])
#     print (page_json['templates'])
#     print (page_json['images'])
#     print (page_json['externallinks'])
#     print (page_json['sections'])
#     print (page_json['parsewarnings'])
#     print (page_json['displaytitle'])
#     print (page_json['iwlinks'])
#     print (page_json['properties'])

#     print ("\n___________________\n")

#     # quit()
