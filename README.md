# HolidayService
Python service to fetch a list of up to next 100 US holidays

The data is fetched from https://www.timeanddate.com/holidays/us/ and is stored in the file holidays.csv.

Use the following command to start the service: python HolidayServer.py

The endpoint "/holidays" returns a list of upto 10 upcoming holidays in the US.
To filter based on holiday-type, use the parameter "holidayType=<type>", e.g. "/holidays?holidayType=federal".
