
import requests, re, json, time, random
requests.packages.urllib3.disable_warnings()

# Created by Alex Beals
# Last updated: February 20, 2016

vote_url = "https://www.10best.com/awards/travel/best-new-brewery/odd-breed-wild-ales-pompano-beach-fla/"

useragents = []
current_useragent = ""

proxies = []
current_proxy = {"https":""}


def get_all_useragents():
    f = open("useragent.txt", "r")
    for line in f:
        useragents.append(line.rstrip('\n').rstrip('\r'))
    f.close()

def choose_useragent():
    k = random.randint(0, len(useragents)-1)
    current_useragent = useragents[k]
    #print current_useragent

def get_all_proxies():
    f = open("proxyhttps.txt", "r")
    for line in f:
        proxies.append(line.rstrip('\n').rstrip('\r'))
    f.close()

def choose_proxy():
    k = random.randint(0, len(proxies)-1)
    current_proxy["https"] = proxies[k]
    #current_proxy["https"] = "173.45.67.182:8080"


def vote_once():
    c = requests.Session()
    #Chooses useragent randomly
    choose_useragent()

    #Set the request headers
    headers = {
        #":authority:": "www.10best.com",
        #":method:" : "get",
        #":path:": "/awards/travel/best-new-brewery/odd-breed-wild-ales-pompano-beach-fla/",
        #"scheme": "https",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "User-Agent": current_useragent,
        "Upgrade-Insecure-Requests":"1",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"
    }

    # Chooses proxy randomly
    choose_proxy()
    try:
        init = c.get(vote_url, headers=headers, verify=False, proxies=current_proxy, timeout=5)
    except:
        print("error with proxy")
        proxies.remove(current_proxy['https'])
        return None

    # Get the vote key
    voteKey = re.search("type=\"hidden\" id=\"voteKey\" value=\"(.*?)\"",init.text).group(1)
    votePath = "/common/ajax/vote.php?voteKey="+str(voteKey)+"&email=&c=" + str(random.random())

    # Build the GET url to vote
    request = "https://www.10best.com" + votePath
    try:
        send = c.get(request, headers=headers, verify=False, proxies=current_proxy)
    except:
        print("error with proxy")
        #proxies.remove(current_proxy_num)
        return None

    return ("success" in send.text)

def vote(times, wait_min = None, wait_max = None):
    global headers
    # For each voting attempt
    i = 1
    while i < times+1:
        b = vote_once()
        # If successful, print that out, else try waiting for 60 seconds (rate limiting)
        if b:
            # Randomize timing if set
            if wait_min and wait_max:
                seconds = random.randint(wait_min, wait_max)
            else:
                seconds = 3

            print("Voted (time number " + str(i) + ")!")
            time.sleep(seconds)
        else:
            print("Vote failed.")
            i-=1
            time.sleep(1)
        i += 1

number_of_votes = 100000
wait_min = 1
wait_max = 1

get_all_proxies()
get_all_useragents()
vote(number_of_votes, wait_min, wait_max)
