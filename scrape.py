import requests
import lxml.html
import time, datetime

DB_NAME = "masternodes.db"

def announcements_get_html():
    announcements_url = "https://bitcointalk.org/index.php?board=159.0"
    r = requests.get(announcements_url)
    if r.status_code == requests.codes.ok:
        return r.text
    else:
        raise Exception("ERROR: could not process request. Status code {0}.".format(r.status_code))

def board_parse(html):
    data = []
    root_doc = lxml.html.fromstring(html)
    topics = root_doc.cssselect("#bodyarea>div.tborder>table.bordercolor>tr")
    for topic in topics:
        topic_cells = topic.cssselect("td")
        if len(topic_cells) == 7:
            topic_link = topic_cells[2].cssselect("span>a")
            name = topic_link[0].text
            id = topic_link[0].attrib['href'].replace("https://bitcointalk.org/index.php?topic=", "")
            author = topic_cells[3].cssselect("a")[0].text
            replies = int(topic_cells[4].text)
            views = int(topic_cells[5].text)
            data_point = dict(id=id,name=name,author=author,replies=replies,views=views)
            #if "[ANN]" in name and "masternode" in name.lower():
            data.append(data_point)
    return data

if __name__ == "__main__":
    wait_time = 5
    iter = 1
    max_iter = float("inf")

    while True:
        data = board_parse(announcements_get_html())

        print("-"*30, str(datetime.datetime.now()), "iteration %s of %s" % (iter, max_iter), "-"*30)

        for data_point in data:
            print(data_point["name"])

        time.sleep(wait_time)
        iter += 1

