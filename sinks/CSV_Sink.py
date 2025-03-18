import csv
import logging
import os
from collections import OrderedDict

import settings
from sinks.sink import Sink


class CSV_Sink(Sink):

    def __init__(self):
        self.ids = []

    def update(self, new_data: [OrderedDict]):
        if len(new_data) == 0:
            logging.info("empty data!")
            return
        file_exists = os.path.exists(settings.CSV_SINK_FILE_NAME)

        first_row = new_data[0]
        with open(settings.CSV_SINK_FILE_NAME, "a", newline='\n') as outfile:
            wr = csv.DictWriter(outfile, fieldnames=list(first_row))
            if not file_exists:
                wr.writeheader()
            for row in new_data:
                if row["id"] not in self.ids:
                    self.ids.append(row["id"])
                    wr.writerow(row)
