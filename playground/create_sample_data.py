"""
create collection with command


`solr create -c test_analytics`

"""
import pysolr
import datetime
import random




solr = pysolr.Solr('http://localhost:8983/solr/test_analytics')

date1 = datetime.date(2018, 1, 1)
date2 = datetime.date(2018, 12, 31)
day = datetime.timedelta(days=1)
final_data = []
while date1 <= date2:
    event_id = date1.strftime('%Y-%m-%d')
    date1 = date1 + day
    data = {
        "id": event_id,
        "sales_i": random.randint(10, 300),
        "expenses_i": random.randint(200, 1200),
        "savings_i": random.randint(200, 800),
        "share_value_i": random.randint(20, 120),
        "created_dt": date1
    }
    final_data.append(data)

solr.add(final_data)
