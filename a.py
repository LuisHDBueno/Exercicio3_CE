import pandas as pd

a = pd.DataFrame([["view", "2020-01-01 00:00:00", 1, "view", 1],
                    ["view", "2020-01-01 00:00:00", 2, "view", 2],
                    ["view", "2020-01-01 00:00:00", 3, "view", 3],
                    ["buy", "2020-01-01 00:00:00", 1, "buy", 1],
                    ["buy", "2020-01-01 00:00:00", 2, "buy", 2],
                    ["buy", "2020-01-01 00:00:00", 3, "buy", 3]], columns=["tag", "timestamp", "visitor_id", "event", "item_id"])

b = pd.DataFrame([["view", "2020-01-01 00:00:00", 1, "view", 1],
                    ["view", "2020-01-01 00:00:00", 2, "view", 2],
                    ["view", "2020-01-01 00:00:00", 3, "view", 3],
                    ["buy", "2020-01-01 00:00:00", 1, "buy", 1],
                    ["buy", "2020-01-01 00:00:00", 2, "buy", 2],
                    ["buy", "2020-01-01 00:00:00", 5, "buy", 5]], columns=["tag", "timestamp", "visitor_id", "event", "item_id"])

c = a.groupby("item_id").size()
d = b.groupby("item_id").size()

print(pd.concat([c, d], axis=1).sum(axis=1))