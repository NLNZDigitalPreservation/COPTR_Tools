with open(r"\\wlgprdfile12\home$\Wellington\GattusoJ\HomeData\Desktop\url_logger_external.txt", encoding="utf-8") as data:
    rows = data.read().split("\n")


statuses = {}

rows = [x for x in rows if x != ""]

for r in rows:
    # print (r)
    pageid, title, url, status = r.split("|")

    if status not in statuses:
        statuses[status]  = []

    if url not in statuses[status]:
        statuses[status].append(url)

counter = 0

for k, v in statuses.items():
    print (k, len(v))
    counter += len(v)

print ("Total:", counter)