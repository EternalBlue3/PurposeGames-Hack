from PurposeGames import get_quiz_info, submit_quiz_results
import time, random, requests, sys
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
    
    # If the number of questions is less than 3, don't bother faking a playthrough with less than 100% accuracy because the server will most likely not even save that playthrough in the stats section
    if num_questions >= 3 and num_questions < 11:
        correct_guesses = random.randint(1, num_questions-2)
        print(f"Correct Guesses: {correct_guesses}")
        
        fakeacc = str(round((correct_guesses / num_questions) * 100))
        faketime = (35 + random.randint(1,30)) * 10
        
        print(f"Time: {faketime}")
        print(f"Accuracy: {fakeacc}\n")
        submit_quiz_results(url, faketime, fakeacc, gameid, tid, token, nonce, csrf)
        time.sleep(faketime+5)
    
    if num_questions >= 11 and num_questions < 25:
        correct_guesses = random.randint(1,num_questions-5)
        print(f"Correct Guesses: {correct_guesses}")

        fakeacc = str(round((correct_guesses / num_questions) * 100))
        faketime = (35 + random.randint(1,30)) * 10

        print(f"Time: {faketime}")
        print(f"Accuracy: {fakeacc}\n")
        submit_quiz_results(url, faketime, fakeacc, gameid, tid, token, nonce, csrf)
        time.sleep(faketime+5)
            
    if num_questions >= 25:
        for x in range(2):
            correct_guesses = random.randint(1,num_questions-10) if x == 0 else correct_guesses + random.randint(2,4)
            print(f"Correct Guesses: {correct_guesses}")
            
            fakeacc = str(round((correct_guesses / num_questions) * 100))
            faketime = (55 + random.randint(1,30) - (random.randint(5,15) * x)) * 10
            
            print(f"Time: {faketime}")
            print(f"Accuracy: {fakeacc}\n")
            submit_quiz_results(url, faketime, fakeacc, gameid, tid, token, nonce, csrf)
            time.sleep(faketime+5)
            
    # Submit final quiz results
    print(f"Finalizing time of {str(finaltime)}.\n\n")
    submit_quiz_results(url, finaltime, "100", gameid, tid, token, nonce, csrf)

if __name__ == '__main__':
    print("Reading Quizzes...")
    with open("quizzes.txt","r") as fh:
        links = [link.strip() for link in fh.readlines()]
    
    print("Finished reading file. Starting obfuscated score submissions...\n\n\n")
    quizzes_played = 0
    for quiz in links:
        try:
            obfuscate_results(quiz)
            quizzes_played += 1
            time.sleep(20) # Add delay between playing quizzes
        except KeyboardInterrupt:
            # Remove quizzes the program has already played on exit
            links = links[quizzes_played:]
            with open("quizzes.txt","w") as fh:
                fh.write('\n'.join(links))
            print("Exiting...")
            sys.exit()
