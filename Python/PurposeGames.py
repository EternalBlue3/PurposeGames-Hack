import requests, json, math, random, concurrent.futures
from bs4 import BeautifulSoup

cookies = {'PHPSESSID': '63j6mgqi746s4ani9cn0477tup', 'pg_search': '1', '__gads': 'ID=ff10c844fc420a79:T=1686661099:RT=1686662496:S=ALNI_Ma3p-cp3QW3oqO0tJajDU9ZFg_Bkw', '__gpi': 'UID=00000c4e62c4812a:T=1686661099:RT=1686662496:S=ALNI_MbiF7du-Q5vsCgCXAmEm0btVFUVOw', '_gid': 'GA1.2.1539107160.1687813076', 'PURPOSEGAMES_2772fc80c0222b8aa0c6d22a3d36c4bf': 'Kowph%7C1760390858%7C1f60291843973110827d74640db74c4a', '_ga_3QWN0H35FH': 'GS1.1.1687829561.13.1.1687831004.0.0.0', '_ga': 'GA1.1.1359990607.1686661096', 'FCNEC': '%5B%5B%22AKsRol_m07DkkdAwjpNIwPsSAu4IUQyJvO3KB_N8XvGwT8h3eKHD3EmfNUEqq_xM77nxWxNO7B6raEE0nJd9CCbN4MW_add3uB7moqHJc61yfZscEJQQMNP0KqvSYceqic-Cw88NCnfEPNUKIw6WeQeGsvsTBA0AGQ%3D%3D%22%5D%2Cnull%2C%5B%5D%5D', 'cto_bundle': '09eRFV9Wb1k3SWJ2OGM4MTZBWGhtOTZLWHJzbndOaTFGamU4Tldwb2tDRCUyQjZ5SmRrSngzM2ZqRGx0ZXN1MDdXMlZqVXYydDRMTUR1ZTVrY29RQmtHRDdOSzlneG1rblVYSU9IU0o4Y0lubUd6YWNFTFVPY0VKUXY4OGkxakdJTENRaEhpWHQ2T2JMSVNsYlFBS3hPVXExeGtRdFZQbGZtQWpzeklzdE5jJTJCWmNIaThJJTNE'}

def get_quiz(url):
    global cookies

    headers = {'authority': 'www.purposegames.com', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'accept-language': 'en-US,en;q=0.9', 'cache-control': 'no-cache', 'dnt': '1', 'pragma': 'no-cache', 'referer': url, 'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Chrome OS"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'same-origin', 'sec-fetch-user': '?1', 'sec-gpc': '1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

    response = requests.get(url,cookies=cookies,headers=headers).text
    return response

def get_nonce(url, gameid, quiztype, noncetoken):
    global cookies

    headers = {'authority': 'www.purposegames.com', 'accept': '*/*', 'accept-language': 'en-US,en;q=0.9', 'cache-control': 'no-cache', 'dnt': '1', 'pragma': 'no-cache', 'referer': url, 'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Chrome OS"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

    params = {'game_id': gameid, 'token': noncetoken, 'language_id': '1'}

    success = False
    while not success:
        try:
            response = json.loads(requests.get(f'https://www.purposegames.com/api/1.0/get-{quiztype}quiz', params=params, cookies=cookies, headers=headers).text)
            success = True
        except:
            pass
    
    return response['nonce']

def get_token(url, gameid, nonce, csrf, fixedtime, time):
    global cookies

    headers = {'authority': 'www.purposegames.com', 'accept': '*/*', 'accept-language': 'en-US,en;q=0.9', 'cache-control': 'no-cache', 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'dnt': '1', 'origin': 'https://www.purposegames.com', 'pragma': 'no-cache', 'referer': url, 'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Chrome OS"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

    data = {'id': gameid, 'p': '80', 'rt': str(fixedtime-time), 'nonce': nonce, 'csrf': csrf}

    success = False
    while not success:
        try:
            response = json.loads(requests.post('https://www.purposegames.com/api/1.0/insert-token', cookies=cookies, headers=headers, data=data).text)
            success = True
        except:
            pass
        
    return response['token_id']

def get_quiz_info(url):
    # Get quiz and quiz information using bs4 parser
    quiz = get_quiz(url)
    soup = BeautifulSoup(quiz, 'html.parser')
    
    # Get quiz type
    quiztypes = {"Multiple-Choice":'mc',"Matching Game":'match',"Text Game":'text',"Type-the-Answer":'typing',"Shape Quiz":'v',"Order Quiz":'order'}
    element = soup.select(".bc__type")[0].text.replace('\n','')
    quiztype = quiztypes[element] if element in quiztypes else ''

    gameid = soup.find(id='game-like').get('data-id') # Game Id
    
    tid = url.split('=')[1] if '?t=' in url else '' # Tournament Id
    
    # Get reasonable completion time
    player_times = soup.find_all(class_='time')
    if len(player_times) >= 4: # Top 3 players and added time element at the top
        top_three = [time.get_text().replace(' min','') for time in player_times[1:4]]
        
        # Turn mins and secs into just secs
        top_three_parsed = []
        for time in top_three:
            mins,secs = time.split(":")
            mins,secs = int(mins),float(secs)
            mins *= 60
            top_three_parsed.append(mins+secs)
        
        # Reasonable time calculation
        reasonable_time = round(sum(top_three_parsed) / 3, 1) # Take average of top 3 times and round to the nearest tenth
        
        if reasonable_time > top_three_parsed[0]+10: # Check if there is an outlier
            reasonable_time = round(top_three_parsed[0] + random.uniform(0.5,2.5),1) # Round number to the tenth
        
        reasonable_time = int(str(reasonable_time).replace('.','')) # Convert to game format
    else: # If there is not enough player completions, base time off the estimated time at the top of the quiz
        reasonable_time = soup.select('.exinf')[0].text
        if reasonable_time == 'About a minute': # Handle when the text says, "About a minute"
            reasonable_time = 600 - random.randint(1,15)
        else:
            if ',' in reasonable_time: # Minutes and seconds
                minutes, seconds = reasonable_time.split(',')
                minutes, seconds = minutes.replace('~','').replace(' min',''), seconds.replace(' sec','')
                reasonable_time = int(minutes) * 60 + int(seconds)
            else: # Just seconds
                reasonable_time = int(reasonable_time.replace('~','').replace(' sec',''))

            reasonable_time = math.floor(reasonable_time * 100) / 10 + random.randint(-30,30) # Add on random amount
        

    num_questions = soup.select(".g__meta_info")[0].text.split("questions")[0].replace(' ','') # Number of questions
    fixedtime = 4800 if reasonable_time < 4800 else reasonable_time + 1000 # Total quiz time (always 4800ms unless time > 4800)
    csrf = soup.select_one('[name="csrf-token"]').get('content') # Csrf token
    nonce = get_nonce(url, gameid, quiztype, csrf) # Nonce value
    token = get_token(url, gameid, nonce, csrf, fixedtime, reasonable_time) # Token value
    
    return {"gameid": gameid, "tid": tid, "token": token, "nonce": nonce, "csrf": csrf, "num_questions": num_questions, "reasonable_time": reasonable_time}

def submit_quiz_results(url, time, acc, gameid, tid, token, nonce, csrf):
    global cookies

    headers = {'authority': 'www.purposegames.com', 'accept': '*/*', 'accept-language': 'en-US,en;q=0.9', 'cache-control': 'no-cache', 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'dnt': '1', 'origin': 'https://www.purposegames.com', 'pragma': 'no-cache', 'referer': url, 'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Chrome OS"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
    
    data = {'id': gameid, 'tid': tid, 'lid': '', 'rt': time, 'p': acc, 'token': token, 'nonce': nonce, 'csrf': csrf}

    response = requests.post('https://www.purposegames.com/api/1.0/insert-score-and-time', cookies=cookies, headers=headers, data=data)
    
def scrape_page(page_number,quiztype):
    success = False
    while not success:
        try:
            html_content = requests.get(f"https://www.purposegames.com/games/{quiztype}?sort=latest&page={str(page_number)}").text
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Get the main list of quizzes
            explore_list = soup.find('div', class_='explore__list')

            # Get all elements with the class name "game-title" under the "explore__list" div to make sure that we don't grab quizzes that aren't on the main list
            titles = explore_list.find_all(class_='game-title')
            page_links = [title.get("href") for title in titles]
            
            if len(page_links) != 50:
                print(f"https://www.purposegames.com/games/{quiztype}?sort=latest&page={str(page_number)}       {str(len(page_links))}")
            
            return page_links
        except Exception as e:
            print(f"Encountered error while scraping page {page_number}: {e}")
    
def scrape_quiz_links(thread_count):
    # Scrape quiz links from site with multithreading for speed up
    links = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
        quiz_types = ["geography", "history", "science", "medicine", "math", "entertainment", "tv", "movies", "music", "literature", "people", "sports", "language", "misc"]
        
        future_to_page = {}
        val = 0
        for quiz_type in quiz_types:
            for page_number in range(1,51):
                future_to_page.update({executor.submit(scrape_page, page_number, quiz_type): val})
                val += 1

        # Process the completed futures as they finish
        for future in concurrent.futures.as_completed(future_to_page):
            page_number = future_to_page[future]
            try:
                page_links = future.result()
                links.extend(page_links)
            except Exception as e:
                print(f"Encountered error while processing page {page_number}: {e}")
    return links
