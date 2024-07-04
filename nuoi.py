import random
import requests, json, re, time,threading
import urllib.parse
from lxml import etree
class InteractiveFacebook(threading.Thread):
    def __init__(self, cookie):
        self.headers = {
        "authority": "mbasic.facebook.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        #"sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        "sec-ch-ua-mobile": "?0",
        'sec-ch-ua-platform': '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "accept-language": "vi",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "cookie": cookie
        }
        self.userid = cookie.split('c_user=')[1].split(';')[0]
    def Reaction(self, access, type_react, id):
        react = re.findall('\/reactions\/picker\/\?.*?"', access)
        if react == []:
            print(f"ID: {id} Không có bày tỏ cảm xúc")
            return
        index = 1 if type_react == "LIKE" else 2 if type_react == "LOVE" else 3 if type_react == "CARE" else 4 if type_react == "HAHA" else 5 if type_react == "WOW" else 6 if type_react == "SAD" else 7
        access = requests.get("https://mbasic.facebook.com%s"%react[0].replace('"', "").replace("amp;", ""), headers=self.headers).text
        ufi = access.split('/ufi/reaction/?')
        if len(ufi) < 8:
            return
        hoan_thanh = requests.get("https://mbasic.facebook.com/ufi/reaction/?%s"%ufi[index].split('"')[0].replace("amp;", ""), headers=self.headers).text
        if "Cảnh báo" in hoan_thanh or "Giờ bạn chưa dùng được tính năng này" in hoan_thanh:
            print(f"User: {self.userid} block")
            return
        print(f"ID: {id} đã thả {type_react} bài viết")
    def Comment(self, access, nd, id):
        cmt = re.findall('\/a\/comment.php\?fs=.*?"', access)
        if cmt == []:
            print(f"ID: {id} Không thể bình luận")
            return
        fb_dtsg = access.split('name="fb_dtsg" value="')[1].split('"')[0]
        jazoest = access.split('name="jazoest" value="')[1].split('"')[0]
        hoan_thanh = requests.post("https://mbasic.facebook.com%s"%cmt[0].replace('"', "").replace("amp;", ""), headers=self.headers, data={"fb_dtsg": fb_dtsg,"jazoest": jazoest, "comment_text": nd}).text
        if "Cảnh báo" in hoan_thanh or "Giờ bạn chưa dùng được tính năng này" in hoan_thanh:
            print(f"User: {self.userid} block")
            return
        print(f"ID: {id} đã comment nội dung:", nd)
    def Delay(self, delay):
        for i in range(delay, -1, -1):
            print(f"Vui lòng đợi {i} giây                                                               ", end='\r')
            time.sleep(1)
    def run(self, path, link='https://mbasic.facebook.com/'):
        home = etree.HTML(requests.get(urllib.parse.unquote(link), headers=self.headers).content)
        find = home.xpath('''//div[@id="m_news_feed_stream"]//article[contains(@data-ft, '{"qid')]''')
        print("Tìm thấy:", len(find), 'bài viết')
        for i in find:
            global idl
            type_react = random.choice(["LIKE", "HAHA", "CARE", "LOVE", "WOW", "SAD"])
            nd = random.choice(open(path).read().splitlines())
            id = json.loads(i.attrib["data-ft"])
            if 'top_level_post_id' in id: id = id['top_level_post_id']
            elif 'mf_objid' in id: id = id['mf_objid']
            if id in idl:
                continue
            idl += id+","
            link = f"https://mbasic.facebook.com/{id}"
            link = urllib.parse.unquote(requests.get(link, headers=self.headers).url.replace('https://mbasic.facebook.com/login.php?next=', ''))
            access = requests.get(link, headers=self.headers).text
            self.Reaction(access, type_react, id)
            self.Delay(delayreact)
            self.Comment(access, nd, id)
            self.Delay(delaycmt)
        # next = home.xpath('//*[@id="m_news_feed_stream"]/a')
        # if next == []:
        #     return
        # next = next[0].attrib["href"]
        self.run(path, link='https://mbasic.facebook.com/')
global delaycmt, delayreact
idl = ""
print("Số trước phải luôn lớn hơn số sau")
tk = open("setting.txt").readlines()
min_sleep = int(tk[0].split("|")[0].strip("\n"))
max_sleep = int(tk[0].split("|")[1].strip("\n"))
path = tk[0].split("|")[2].strip("\n")
cookie = tk[0].split("|")[3].strip("\n")
#min_sleep = int(input(">> Nhập số min sleep (s): "))
#max_sleep = int(input(">> Nhập số max sleep (s): "))
#path = 'cmt.txt'
#cookie = input("Cookie: ")
#delayreact = random.randint(react[0], react[1])
delayreact = random.randint(min_sleep, max_sleep)
delaycmt = random.randint(min_sleep, max_sleep)
#while True:
    #InteractiveFacebook(cookie).run(path)

thread_count = len(tk)
def main(m):
        for i in range(m, 9999999, thread_count):
                mail = tk[i].strip()
                run = InteractiveFacebook(cookie)
                run.run(path)

for m in range(thread_count):
    threading.Thread(target=main, args=(m,)).start()

