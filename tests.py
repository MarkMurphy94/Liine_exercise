import unittest
import main
import datetime

# Simple test suite with a demo test case

class PipelineTests(unittest.TestCase):
    def test_day_in_day_range(self):
        date: datetime.datetime= "27-08-2024:21:18"
        formatted_date = datetime.datetime.strptime(date, main.DATE_TIME_FORMAT)
        self.assertTrue(main.is_in_day_range(formatted_date.weekday(), "Mon-Wed"))

if __name__ == '__main__':
    unittest.main()