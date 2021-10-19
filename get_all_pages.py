import requests


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


results = get_all()

for r in results:
    pageid = r["pageid"]
    ns = r["ns"] 
    title = r["title"]
    print (f"\nWorking on page: {pageid} - {title}")
    page_json = get_page(pageid)

