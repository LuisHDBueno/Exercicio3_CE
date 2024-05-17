import pandas as pd
import multiprocessing as mp
import time

class Handler:
    def __init__(self, data:mp.Queue, managed_dict:dict):
        self.data = data
        self.df = pd.DataFrame()
        self.managed_dict = managed_dict
        
    def queue_to_dataframe(self):
        data_list = []
        
        while not self.data.empty():
            data_list.append(self.data.get())
    
        self.df = pd.DataFrame(data_list, columns=["tag", "timestamp", "visitor_id", "event", "item_id"])

    def handle_data(self):
        self.queue_to_dataframe()

        # Preprocessing
        self.df.drop(columns=["tag"], inplace=True)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], format="%Y-%m-%d %H:%M:%S", errors='coerce')
        
        viewed = self.df[self.df["event"] == "view"].copy()
        bought = self.df[self.df["event"] == "buy"].copy()
        
        # Analytics
        views_per_item = viewed.groupby("item_id").size()
        buys_per_item = bought.groupby("item_id").size()
        
        self.managed_dict["views_per_item"] = pd.concat([self.managed_dict["views_per_item"], views_per_item], axis=1).sum(axis=1).sort_values(ascending=False)
        self.managed_dict["buys_per_item"] = pd.concat([self.managed_dict["buys_per_item"], buys_per_item], axis=1).sum(axis=1).sort_values(ascending=False)
        
        min_time_viewed = viewed["timestamp"].min()
        max_time_viewed = viewed["timestamp"].max()
        
        if min_time_viewed < self.managed_dict["min_time_viewed"]:
            self.managed_dict["min_time_viewed"] = min_time_viewed
        if max_time_viewed > self.managed_dict["max_time_viewed"]:
            self.managed_dict["max_time_viewed"] = max_time_viewed
        
        min_time_bought = bought["timestamp"].min()
        max_time_bought = bought["timestamp"].max()
        
        if min_time_bought < self.managed_dict["min_time_bought"]:
            self.managed_dict["min_time_bought"] = min_time_bought
        if max_time_bought > self.managed_dict["max_time_bought"]:
            self.managed_dict["max_time_bought"] = max_time_bought
        
        timespan_viewed = (max_time_viewed - min_time_viewed).seconds / 60
        timespan_bought = (max_time_bought - min_time_bought).seconds / 60
        
        self.managed_dict["num_views"] += len(viewed)
        self.managed_dict["num_buys"] += len(bought)
        
        if timespan_viewed == 0:
            timespan_viewed = 1
        if timespan_bought == 0:
            timespan_bought = 1
        
        self.managed_dict["avg_views_per_minute"] = self.managed_dict["num_views"] / timespan_viewed
        self.managed_dict["avg_buys_per_minute"] = self.managed_dict["num_buys"] / timespan_bought