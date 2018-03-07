import requests
import lxml.html
import rethinkdb as r
import time, datetime
import matplotlib.pyplot as plt

db_name = "masternodes"

def getAnnHTML():
    annURL = "https://bitcointalk.org/index.php?board=159.0"#Announcements board
    r = requests.get(annURL)
    if r.status_code == requests.codes.ok:
        return r.text
    else:
        raise Exception("ERROR: could not process request. Status code {0}.".format(r.status_code))

def parseBoard(html):
    data = []
    root_doc = lxml.html.fromstring(html)
    topics = root_doc.cssselect("#bodyarea>div.tborder>table.bordercolor>tr")
    for topic in topics:
        toric_cells = topic.cssselect("td")
        if len(toric_cells) == 7:
            topic_link = toric_cells[2].cssselect("span>a")
            name = topic_link[0].text
            id = topic_link[0].attrib['href'].replace("https://bitcointalk.org/index.php?topic=", "")
            author = toric_cells[3].cssselect("a")[0].text
            replies = int(toric_cells[4].text)
            views = int(toric_cells[5].text)
            data_point = dict(id=id,name=name,author=author,replies=replies,views=views)
            #if "[ANN]" in name and "masternode" in name.lower():
            data.append(data_point)
    return data

def start_database():
    r.connect('localhost', 28015).repl()
    try:
        r.db_create(db_name).run()
        r.db(db_name).table_create("announcements").run()
    except:
        pass
def load_data(data_point):
    r.db(db_name).table("announcements").insert(data_point).run()
def is_in(x,y):
    y_id = []
    for item in y:
        y_id.append(item["id"])
    if x["id"] in y_id: return True
    return False





if __name__ == "__main__":
    wait_time = 5
    iter = 0
    max_iter = float("inf")#60/wait_time
    start_database()
    historical_data = []
    y = []
    while True:
        iter += 1
        annBoard = getAnnHTML()
        data = parseBoard(annBoard)
        print "-"*30, str(datetime.datetime.now()), "iteration %s of %s" % (iter, max_iter), "-"*30
        i = 0
        for data_point in data:
            if not is_in(data_point, historical_data):
                load_data(data_point)
                print "-"*5, data_point["name"]
                historical_data.append(data_point)
                i += 1
        y.append(i)

        if iter == max_iter:
            print y
            plt.plot(y)
            plt.title('wait time = %d s' % wait_time)
            plt.ylabel("data points added")
            plt.xlabel("iteration")
            plt.show()
            break
        time.sleep(wait_time)



#soup = BeautifulSoup(annPage)

