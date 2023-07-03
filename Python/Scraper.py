from PurposeGames import scrape_quiz_links

links = scrape_quiz_links(15)

with open("quizzes.txt","w") as fh:
    fh.write('\n'.join(links))