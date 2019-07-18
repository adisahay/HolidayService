import csv
from datetime import datetime
from unicodedata import normalize
from urllib.parse import urlparse, parse_qs
import http.server
import socketserver
import json


PORT = 80

HOLIDAYS_FILE = "holidays.csv"
MAX_HOLIDAYS_COUNT = 10
HOLIDAYS_YEAR = 2019

INDEX_DATE = 0
INDEX_WEEKDAY = 1
INDEX_NAME = 2
INDEX_TYPE = 3
INDEX_DETAILS = 4

PRETTY_PRINT_RESPONSE = True
PRETTY_PRINT_INDENT = 2
PRETTY_PRINT_SEPARATORS = (',', ': ')


def holidays(holidayType = None):
    """
    Returns a list of a maximum of 10 holidays

    Keyword arguments:
    holidayType: string (default: None)
    """

    result = []
    now = datetime.now()
    count = 0

    if holidayType is not None:
        holidayType = holidayType.lower()

    with open(HOLIDAYS_FILE, encoding = "utf-8-sig") as hfile:
        lines = csv.reader(hfile, delimiter = ",")
        for values in lines:
            dateString = values[INDEX_DATE] + "-" + str(HOLIDAYS_YEAR)
            date = datetime.strptime(dateString, "%d-%b-%Y")

            if date > now and \
            (holidayType is None or holidayType in values[INDEX_TYPE].lower()):
                result.append({
                    "name": values[INDEX_NAME],
                    "date": datetime.strftime(date, "%A, %B %d, %Y"),
                    "type": values[INDEX_TYPE],
                    "details": normalize("NFKD", values[INDEX_DETAILS])
                })

                count += 1
                if count == MAX_HOLIDAYS_COUNT:
                    return result
    return result


class HolidayHandler(http.server.SimpleHTTPRequestHandler):
    """Handler object for the Holiday Server"""

    def do_GET(self):
        """GET request handler"""

        parsed = urlparse(self.path)
        if parsed.path == "/holidays":
            holidayType = None
            query = parsed.query.split("=")
            if query[0] == "holidayType":
                holidayType = query[1]

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            result = holidays(holidayType = holidayType)

            if PRETTY_PRINT_RESPONSE:
                jsonDump = json.dumps(result, indent = PRETTY_PRINT_INDENT,
                                    separators = PRETTY_PRINT_SEPARATORS)
            else:
                jsonDump = json.dumps(result)

            writeBytes = bytes(jsonDump, "utf-8")
            self.wfile.write(writeBytes)


socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), HolidayHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
