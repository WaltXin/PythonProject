from urllib import request
from bs4 import BeautifulSoup
from splinter import Browser

houseList = []
SendEmail = []
origin_url = "http://www.daft.ie/dublin-city/residential-property-for-rent/ashtown,ballsbridge,blackrock,castleknock,clontarf,dartry,donnybrook,dublin-14,dublin-18,dublin-2,dublin-4,dublin-4,dublin-6,dublin-6w,dundrum,foxrock,milltown,monkstown,rathgar,rathmines,sandyford,terenure/?s%5Bmnb%5D=2&s%5Bmnbt%5D=2&s%5Badvanced%5D=1&s%5Bignored_agents%5D%5B0%5D=5732&s%5Bignored_agents%5D%5B1%5D=428&s%5Bignored_agents%5D%5B2%5D=1551&s%5Bsort_by%5D=price&s%5Bsort_type%5D=a&searchSource=rental"
# &offset=20
# 1 - 4 means 3 pages, each page 20 house, so it will send 40 house
for page in range(1, 4):
    url_no = 20 * (page - 1)
    url_str = origin_url + '&offset=' + str(url_no)
    r = request.urlopen(url_str)
    bytecode = r.read()
    htmlstr = bytecode.decode()
    soup = BeautifulSoup(htmlstr, "html.parser")
    # all house link in search result


    for div in soup.findAll('div', {'class': 'search_result_title_box'}):
        href = div.find('a')
        link = href.get('href')
        pref = "http://www.daft.ie"
        link = pref + link
        # strs = link[-8:-1]
        houseList.append(link)

    print(houseList)

    HouseTxt = []

    # Check if house in House.txt or not, if not, add house in and send email
    with open("C:\\Users\\xinwei.xiong\\Desktop\\House.txt", "r") as reader:
        for line in reader:
            if line is not None:
                line = line[:-1]
                HouseTxt.append(line)
        with open("C:\\Users\\xinwei.xiong\\Desktop\\House.txt", "a") as writer:
            for line in houseList:
                if line not in HouseTxt:
                    SendEmail.append(line)
                    writer.write(line + '\n')

    print(SendEmail)

    for URL in SendEmail:
        URL = URL + '?auth[login]=1'
        browser = Browser('firefox')
        browser.visit(URL)
        login_userName = 'yourname'
        login_password = 'yourpassword'
        email = 'youremail'
        phone = ''
        browser.fill('auth[username]', login_userName)
        browser.fill('auth[password]', login_password)
        browser.find_by_id('login_button').first.click()

        browser.find_by_id('your_name').fill(login_userName)
        browser.find_by_id('your_email').fill(email)
        browser.fill('contact_number', phone)
        browser.fill('your_message', '''Hi,

        We are 2 professionals both working as software engineer, we believe this is perfect place for us as it's near where we work.

        We can also provide both landlords and work references letters if needed.

        Please let us know.''')

        browser.find_by_id('copy_message').first.click()
        browser.find_by_id('ad_reply_submit').first.click()


