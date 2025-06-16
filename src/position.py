
import concurrent.futures

import numpy as np
import pandas as pd
from google.cloud import firestore

# =========================================================================== #

def update(data: dict) -> None:
    buses_df = pd.DataFrame.from_dict(data).astype(str)

    db = firestore.Client(database='sptransit')

    def update_bus(bus):
        doc_ref = db \
            .collection('trips') \
            .document(bus.trip_id) \
            .collection('buses') \
            .document(bus.bus_prefix)

        update_data = {
            'lat': bus.lat,
            'lon': bus.lon,
            'timestamp': bus.timestamp,
        }

        doc_ref.set(update_data)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        list(executor.map(update_bus, buses_df.itertuples()))

# =========================================================================== #