import tkinter as tk
from tkinter import ttk
from tkinter import Button
from tkinter import messagebox
from datetime import datetime

from steamwebapi.api import ISteamUserStats, ISteamUser, _SteamWebAPI

STEAM_API_KEY = '18BA4226434B86ED2AD10490BC510B56'
DOTA2_ID = 570
PUBG_ID = 578080
POE_ID = 238960

STEAM_WEB_API = _SteamWebAPI(STEAM_API_KEY)
STEAM_USER_STATS = ISteamUserStats(steam_api_key=STEAM_WEB_API.apikey)

GAME_ID_DICT = {
   "DOTA2": DOTA2_ID, 
   "PUBG": PUBG_ID,
   "PATH OF EXILE": POE_ID
}


def create_news_url(appID, count = 1, maxlength = 100, format = "json"):
   url_params_dict = {
      "appid": appID,
      "count": count,
      "maxlength": maxlength,
      "format": format
   }

   return STEAM_WEB_API.create_request_url("ISteamNews", "GetNewsForApp", 2, parameters = url_params_dict)


def get_news_for_app(appID, count = 1, maxlength = 100, format = "json"):
   url = create_news_url(appID, count, maxlength, format)
   data = STEAM_WEB_API.retrieve_request(url)
   
   return STEAM_WEB_API.return_data(data, format=format)


def update_news(app_name):
   messagebox.showinfo(title = "Новости по игре: %s." % (app_name), 
                       message = get_parsed_news(get_news_for_app
                       (appID = GAME_ID_DICT[app_name], format = "json")))


def get_parsed_news(raw_news):
   preparsed_news = raw_news["appnews"]["newsitems"][0]
   title = str(preparsed_news["title"])
   author = str(preparsed_news["author"])
   contents = str(preparsed_news["contents"])
   date = datetime.utcfromtimestamp(int(preparsed_news["date"])).strftime('%Y-%m-%d %H:%M:%S')
   return "Новость: " + title + \
          "\nСодержимое: " + contents + \
          "\nДата публикации: " + date + \
          "\nАвтор новости: " + author


def update_stat(app_name):
   messagebox.showinfo(title = "Количество игроков в игре: %s." % (app_name),
                       message =  get_parsed_stat(STEAM_USER_STATS.get_number_of_current_players
                       (appID = GAME_ID_DICT[app_name], format = "json")))


def get_parsed_stat(raw_stat):
   return "Количество текущих игроков: " + str(raw_stat["response"]["player_count"])


def create_combobox():
   app = tk.Tk() 
   app.geometry('350x100')
   app.title('STEAM API')

   labelTop = tk.Label(app, text="Choose your game")
   labelTop.grid(column=1, row=0)

   game_combobox = ttk.Combobox(app, 
                                values=["DOTA2", 
                                        "PUBG",
                                        "PATH OF EXILE"], state="readonly")

   game_combobox.grid(column=1, row=1)
   game_combobox.current(1)
   
   news_btn = Button(app, 
                     text="Show News", 
                     command= lambda: update_news(game_combobox.get()))
   news_btn.grid(column=0, row=2)

   glob_stat_btn = Button(app, 
                          text="Current Players", 
                          command= lambda: update_stat(game_combobox.get()))
   glob_stat_btn.grid(column=3, row=2)

   app.mainloop()


def main():
   create_combobox()


if __name__ == "__main__":
    main()