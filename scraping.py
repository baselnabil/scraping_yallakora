import requests
from bs4 import BeautifulSoup
import csv
date = input("enter a date in the following format mm/dd/yy")
page = requests.get(f"https://yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={date}")

def main(page):
    source = page.content
    soup = BeautifulSoup(source,"lxml")
    championShips= soup.find_all("div",{"class":"matchCard"})
    games=[]    
    def get_match_into(championShips):
        match_name = championShips.contents[1].find("h2").text.strip()
        all_matches= championShips.contents[3].find_all('div',{'class':'liItem'})

        number_of_matches= len(all_matches)
        for i in range(number_of_matches):
            # we get the name of the teams 
            Team_A = all_matches[i].find("div",{"class":"teamA"}).text.strip()
            Team_B = all_matches[i].find("div",{"class":"teamB"}).text.strip()

            # we get the scores of each team
            game_score= all_matches[i].find("div",{"class":"MResult"}).find_all("span",{"class":"score"})
            score=f"{game_score[0].text.strip()}--{game_score[1].text.strip()}"
            
            # now we get the time of the match 
            game_time= all_matches[i].find("div",{"class":"MResult"}).find("span",{"class":"time"}).text.strip()
            games.append({"match type":match_name,"name1":Team_A,"name2":Team_B,"game score ":score,"game time":game_time})
            print(game_time)
    for i in range (len(championShips)):
        get_match_into(championShips[i])
    keys= games[0].keys()
    with open('yalla.csv',"w", encoding="utf-8") as output_file:
        dic_writter = csv.DictWriter(output_file,keys)
        dic_writter.writeheader()
        dic_writter.writerows(games)
        print("file done")

main(page)