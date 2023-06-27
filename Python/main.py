from PurposeGames import get_quiz_info, submit_quiz_results
import time, random, requests
from bs4 import BeautifulSoup

def obfuscate_results(url):    
    success = False
    while not success:
        try:
            info = get_quiz_info(url)
            gameid, tid, token, nonce, csrf = info['gameid'], info['tid'], info['token'], info['nonce'], info['csrf']
            num_questions, finaltime = int(info['num_questions']), int(info["reasonable_time"])
            success = True
        except Exception as e:
            print(f"Error getting quiz info for: {url}")
            print(f"Error: {e}")
    
    print(f"Estimated reasonable submission time: {finaltime}")
    print(f"Quiz Obfuscation for: {url}")
    
    if num_questions < 3:
        print("Correct Guesses: 1")
        
        fakeacc = str(round((1 / num_questions) * 100)) # Automatically assume 1 correct answer
        faketime = (15 + random.randint(1,20)) * 10
        
        print(f"Time: {faketime}")
        print(f"Accuracy: {fakeacc}\n")
        submit_quiz_results(url, faketime, fakeacc, gameid, tid, token, nonce, csrf)
        time.sleep(60)
    
    if num_questions >= 3 and num_questions < 11:
        correct_guesses = random.randint(1, num_questions-2)
        print(f"Correct Guesses: {correct_guesses}")
        
        fakeacc = str(round((correct_guesses / num_questions) * 100))
        faketime = (35 + random.randint(1,30)) * 10
        
        print(f"Time: {faketime}")
        print(f"Accuracy: {fakeacc}\n")
        submit_quiz_results(url, faketime, fakeacc, gameid, tid, token, nonce, csrf)
        time.sleep(60)
    
    if num_questions >= 11 and num_questions < 25:
        for x in range(2):
            correct_guesses = random.randint(1,num_questions-5) if x == 0 else correct_guesses + random.randint(2,4)
            print(f"Correct Guesses: {correct_guesses}")
            
            fakeacc = str(round((correct_guesses / num_questions) * 100))
            faketime = (35 + random.randint(1,30) - (random.randint(1,15) * x)) * 10
            
            print(f"Time: {faketime}")
            print(f"Accuracy: {fakeacc}\n")
            submit_quiz_results(url, faketime, fakeacc, gameid, tid, token, nonce, csrf)
            time.sleep(60)
            
    if num_questions >= 25:
        for x in range(3):
            correct_guesses = random.randint(1,num_questions-10) if x == 0 else correct_guesses + random.randint(2,4)
            print(f"Correct Guesses: {correct_guesses}")
            
            fakeacc = str(round((correct_guesses / num_questions) * 100))
            faketime = (55 + random.randint(1,30) - (random.randint(5,15) * x)) * 10
            
            print(f"Time: {faketime}")
            print(f"Accuracy: {fakeacc}\n")
            submit_quiz_results(url, faketime, fakeacc, gameid, tid, token, nonce, csrf)
            time.sleep(60)
            
    # Submit final quiz results
    print(f"Finalizing time of {str(finaltime)}.\n\n")
    submit_quiz_results(url, finaltime, "100", gameid, tid, token, nonce, csrf)
    time.sleep(60)

if __name__ == '__main__':
    print("Webscraping...")
    links = []

    for x in range(10):  # Find all quizzes on the first 10 pages
        success = False
        while not success:
            try:
                html_content = requests.get(f"https://www.purposegames.com/games?sort=latest&page={str(x)}").text
                success = True
            except Exception as e:
                print(f"Entountered error: {e}")

        soup = BeautifulSoup(html_content, "html.parser")

        # Find all games on the page and get the href values
        titles = soup.find_all(class_="game-title")
        links += [title.get("href") for title in titles][:50]
        
    print("Finished webscraping. Starting obfuscated score submissions...\n\n\n")
    for x in links:
        obfuscate_results(x)
