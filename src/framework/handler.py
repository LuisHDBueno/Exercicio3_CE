import pandas as pd
import multiprocessing as mp
import time
import numpy as np
        
def queue_to_dataframe(data):
    data_list = []
    
    while not data.empty():
        data_list.append(data.get())

    return pd.DataFrame(data_list, columns=["tag", "timestamp", "visitor_id", "event", "item_id"])

def handle_data(data, managed_dict):
    df = queue_to_dataframe(data)
    
    # Preprocessing
    df.drop(columns=["tag"], inplace=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format="%Y-%m-%d %H:%M:%S", errors='coerce')
    
    viewed = df[df["event"] == "view"].copy()
    bought = df[df["event"] == "buy"].copy()
    
    # Analytics
    views_per_item = viewed.groupby("item_id").size()
    buys_per_item = bought.groupby("item_id").size()
    
    managed_dict["views_per_item"] = pd.concat([managed_dict["views_per_item"], views_per_item], axis=1).sum(axis=1).sort_values(ascending=False)
    managed_dict["buys_per_item"] = pd.concat([managed_dict["buys_per_item"], buys_per_item], axis=1).sum(axis=1).sort_values(ascending=False)
    
    min_time_viewed = viewed["timestamp"].min()
    max_time_viewed = viewed["timestamp"].max()
    
    if min_time_viewed < managed_dict["min_time_viewed"]:
        managed_dict["min_time_viewed"] = min_time_viewed
    if max_time_viewed > managed_dict["max_time_viewed"]:
        managed_dict["max_time_viewed"] = max_time_viewed
    
    min_time_bought = bought["timestamp"].min()
    max_time_bought = bought["timestamp"].max()
    
    if min_time_bought < managed_dict["min_time_bought"]:
        managed_dict["min_time_bought"] = min_time_bought
    if max_time_bought > managed_dict["max_time_bought"]:
        managed_dict["max_time_bought"] = max_time_bought
    
    managed_dict["num_views"] += len(viewed)
    managed_dict["num_buys"] += len(bought)
    