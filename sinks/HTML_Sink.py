import logging
from collections import OrderedDict

import settings
from sinks.sink import Sink


class HTML_Sink(Sink):

    def __init__(self):
        self.ids = {}

    def update(self, new_data: [OrderedDict]):
        if len(new_data) == 0:
            logging.info("empty data!")
            return
        self.ids.update({d["id"]: d for d in new_data})

        with open(settings.HTML_SINK_FILE_NAME, "w", newline='\n') as outfile:
            outfile.write("<!DOCTYPE html>\n<html><body style='width:100%'><table>\n")
            col_names = list(new_data[0])
            outfile.write("<tr><th>" + "</th><th>".join(col_names) + "</th></tr>\n")

            for id, row in self.ids.items():
                row_str = "<tr>"
                for k, v in row.items():
                    row_str += f"<td>{v}</td>"
                row_str += "</tr>\n"
                outfile.write(row_str)
            outfile.write("</table></body></html>\n")
