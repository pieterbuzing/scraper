import os
from collections import OrderedDict
from unittest import TestCase

import settings
from sinks.CSV_Sink import CSV_Sink


class TestCSV_Sink(TestCase):
    def test_update(self):
        sink = CSV_Sink()
        data = [OrderedDict(a=1, b=2, c=3)]
        sink.update(data)
        assert os.path.exists(settings.CSV_SINK_FILE_NAME)
