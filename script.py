#content-card-info container
#ASYNCHRONOUS (VERY FAST)
import asyncio
import aiohttp
import requests
import json
from bs4 import BeautifulSoup
from colorama import Style, Fore
from datetime import datetime, timedelta, timezone

cols=[Fore.YELLOW, Fore.LIGHTBLACK_EX, Fore.BLUE, Fore.LIGHTMAGENTA_EX, Fore.CYAN, Fore.RED]
GREEN = '\033[32m'
RESET = '\033[0m'
YELLOW = '\033[33m'
RED = '\033[31m'
		

urls = ["https://tour.trueanal.com/", "https://tour.nympho.com/", 
"https://tour.allanal.com/", "https://tour.swallowed.com/", "https://dirtyauditions.com/","https://tour.analonly.com/" ]
api_urls=[url+'api/countdown' for url in urls]


dic = {}
for url in urls:
    dic[urls.index(url)] = {}
async def fetch(url, session):
    cls = "content-meta" if urls.index(url) == 0 else "content-models"
    try:
        async with session.get(url) as response:
            if response.status == 200:
                text = await response.text()
                soup = BeautifulSoup(text, 'html.parser')
                content_models = soup.find(class_=lambda value: value and cls in value)
                a_tags = content_models.find_all('a')
                models_text = [a.get_text(strip=True) for a in a_tags]
                #------------------------
                script_tag = soup.find('script', id='__NEXT_DATA__')
                json_content = script_tag.string
                data = json.loads(json_content)
                thumb_url = data['props']['pageProps']['contents'][0]['thumb']

                img_url = thumb_url
                #------------------------
                if urls.index(url) == 0:
                    #-------------------
                    elements = soup.find_all('a', class_="big-img to-preload")
    
                    src_links = []
                    for element in elements:
                        img_tag = element.find('img', class_="preload-on")
                        if img_tag and img_tag.has_attr('src'):
                            src_links.append(img_tag['src'])
                    img_url = src_links[0]
                    #-------------------
                    models_text = models_text[1:len(models_text)]
                dic[urls.index(url)].update({'url': url, 'models': models_text, 
                                              'img_url': img_url})
            else:
                
                dic[urls.index(url)].update({'error': f"Failed to fetch {url}: {response.status}"})
    except Exception as e:
        dic[urls.index(url)].update({'error': f"An error occurred while fetching {url}: {str(e)}"})

#now = datetime.now(timezone.utc).astimezone()
import pytz

async def fetch_api(url, session):
    global my_time
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                secs = int(data.get('countdown_time'))
                time_left = timedelta(seconds=secs)
                now = my_time
                
                future_time = now + time_left
                if time_left.days > 0:
                    time = "on " + str(future_time.strftime('%d/%m'))

                else:
                    time = "at " + str(future_time.strftime('%H:%M'))
                    dic[api_urls.index(url)].update({'left': str(secs) })

                dic[api_urls.index(url)].update({'next': time})
            else:
                dic[api_urls.index(url)].update({'error': f"Failed to fetch API {url}: {response.status}"})
    except Exception as e:
        dic[api_urls.index(url)].update({'error': f"An error occurred while fetching API {url}: {str(e)}"})


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(url, session) for url in urls] + [fetch_api(url, session) for url in api_urls]
        await asyncio.gather(*tasks)


import json
def run_():
    import asyncio
    asyncio.run(main())
    cols = [Fore.RED, Fore.GREEN, Fore.BLUE]
    output = []

    """for k, v in dic.items():
        entry = {'next': '', 'models': '', 'other': ''}
        for kk, vv in v.items():
            if kk == "next":
                entry['next'] = f'<span class="{cols[int(k) - 1]}">{vv}</span>'
            elif kk == "models":
                entry['models'] = f'<span class="{cols[int(k) - 1]}">{vv}</span>'
            else:
                entry['other'] = vv
        output.append(entry)"""
    print(json.dumps(dic))
    return [json.dumps(dic)]
        
import argparse

def process_time(my_time, timezone_str):
    # Convert the provided time string to a datetime object in UTC
    utc_time = datetime.fromisoformat(my_time).replace(tzinfo=pytz.utc)
    
    # Convert the UTC time to the target timezone
    target_timezone = pytz.timezone(timezone_str)
    local_time = utc_time.astimezone(target_timezone)
   
    return local_time
   # print(local_time.isoformat())

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Process some time.")
    parser.add_argument("my_time", type=str, help="The time to be processed (in UTC)")
    parser.add_argument("timezone", type=str, help="The timezone to convert to")
    args = parser.parse_args()

    # Convert the provided time string to a datetime object
    my_time = process_time(args.my_time, args.timezone)

    #my_time = datetime.now(timezone.utc).astimezone()
    run_()        



# Python's asyncio library requires an event loop to run asynchronous functions.


''' #SYNCHRONOUS
if __name__=="__main__":
	import asyncio
	asyncio.run(main())
	for k,v in dic.items():
		for kk,vv in v.items():
			if kk=="models":
				print(kk, GREEN +str(vv)+RESET)
			elif kk=="url":
				print(kk,YELLOW +str(vv)+RESET)
			else:
				print(kk,RED +str(vv)+RESET)
		print('\n')
import requests
from bs4 import BeautifulSoup


urls = ["https://tour.trueanal.com/", "https://tour.nympho.com/", 
"https://tour.allanal.com/", "https://tour.swallowed.com/", "https://dirtyauditions.com/","https://tour.analonly.com/" ]
i=1
for url in urls:
	if i==1:
		cls="content-meta"
	else:
		cls="content-models"
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	content_models = soup.find(class_=lambda value: value and cls in value)
	a_tags = content_models.find_all('a')
	models_text = [a.get_text(strip=True) for a in a_tags]
	print(i,url,"\n", models_text,"\n")
	i=i+1
		
	'''











