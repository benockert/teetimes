# Create a tee time for Abenaqui CC
import argparse
import requests
import time
import sys
from datetime import datetime, timedelta

from requests import Session

UNAVAIL_MSG = "Sorry, Another member is currently "
LARGE_GRP_MSG = "If you are booking a large group "

class NoRebuildAuthSession(Session):
    def rebuild_auth(self, prepared_request, response):
        """
        No code here means requests will always preserve the Authorization
        header when redirected.
        Be careful not to leak your credentials to untrusted hosts!
        """


class TeeTime(object):
    def __init__(self, username, password, date, tee_time):
        self.username = username
        self.password = password
        self.date = date
        self.tee_time = tee_time

        self.month = date[5:7]
        self.day = date[8:10]
        self.year = date[0:4]

    def tee_sheet_open(self):
        # current date and time, EST (-4 from UTC)
        right_now = datetime.now() - timedelta(hours=4)

        # requested teetime date, current time
        requested_date = datetime(int(self.year), int(self.month), int(self.day),
                                  right_now.hour, right_now.minute,
                                  right_now.second, right_now.microsecond)

        # day tee sheet opens, current time
        five_days_from_now = (right_now + timedelta(days=5))

        return requested_date < five_days_from_now


    def get_date(self):
        tee_time_date = str(self.year) + "-" + str(self.month) + "-" + str(self.day)
        return tee_time_date

    def login(self, session):
        # get login page
        session.get("https://www.abenaquicc.com/club/scripts/login/login.asp")

        # post login data
        loginresponse = session.post("https://www.abenaquicc.com/club/scripts/login/Login_Validate.asp?GRP=36600&NS=PUBLIC", data={'user': self.username, 'pw': self.password, 'MemEnter': ''})

        # TODO improve so check if redirect goes back to login page or to member-home
        if loginresponse.status_code == 200:
            print("Logged in successfully")
            return session

    def get_tee_sheet(self, session):
        # TODO this query needs username and password hash (Ben's is currently hardcoded)
        # Get today's tee sheet (no date in query parameters)
        teesheetresponse = session.get("http://abenaquicc.mfteetimes.com/sso/?u=01457D&p=b3a4e9474edc367129b1eaf6d8bd9b4f25eecef6&date=&time=&t=MEMBERNUM&course=1")
        resp1_status = teesheetresponse.status_code

        # Gets the tee sheet for the requested date in order to call the changeDate function
        teesheetresponse = session.get("http://abenaquicc.mfteetimes.com/teetimes.php?cmd=teesheet2017&action=display2017&jDate=" + self.date + "&course=1")
        resp2_status = teesheetresponse.status_code

        if resp1_status == 200 and resp2_status == 200:
            print("Got tee sheet for requested date")
            return session

    def request_tee_time(self, session):
        requestData = {'cmd': 'teesheet2017',
                       'action': 'teetime_interface_holes_to_play',
                       'slotsAvailable': '4',
                       'maxSlotsAvailable': '4',
                       'course': '1',
                       'dateof': self.date,
                       'time': self.tee_time,
                       'year': str(self.year),
                       'month': str(self.month),
                       'day': str(self.day),
                       'hole': '1',
                       'block_id': '0',
                       'blockSpecialStartAltText': '',
                       'extraTimesVal': ''}

        requesttimeresponse = session.post("http://abenaquicc.mfteetimes.com/teetimes.php?cmd=teesheet2017&action=display2017&jDate=" + self.date + "&course=1", data=requestData)

        #TODO maybe get content instead of text and check for the errModal id instead
        if requesttimeresponse.status_code == 200 and UNAVAIL_MSG not in requesttimeresponse.text:
            if LARGE_GRP_MSG in requesttimeresponse.text:
                print("Large group message, continuing to booking submit page")
                # continue through booking
                continueData = {'time': self.tee_time,
                                'course': '1',
                                'dateof': self.date,
                                'blockId': '0',
                                'hole': '1',
                                'holesToPlay': '18',
                                'isLottery': '0',
                                'cmd': 'teesheet2017',
                                'action': 'teetime_interface_select_players',
                                'year': str(self.year),
                                'month': str(self.month),
                                'day': str(self.day),
                                'time': self.tee_time,
                                'hole': '1',
                                'booked_ids': '[@booked_ids]',
                                'course': '1',
                                'block_id': '0'}
                continuetosubmit = session.post("http://abenaquicc.mfteetimes.com/teetimes.php", data=continueData)
                if continuetosubmit.status_code == 200:
                    print("Successfully requested tee time")
                    return session
            else:
                print("Successfully requested tee time")
                return session

    def make_tee_time(self):
        session = NoRebuildAuthSession()

        print("LOGGING IN USER " + self.username + "...")
        session = self.login(session)
        if not session:
            print("Error logging in")
            return "Error logging in"

        print("GETTING THE TEE SHEET FOR " + self.date + "...")
        session = self.get_tee_sheet(session)
        if not session:
            print("Error getting tee sheet")
            return "Error getting tee sheet"

        # wait for tee sheet to become open
        if not self.tee_sheet_open():
            print("WAITING FOR THE TEE SHEET TO OPEN...")
            while True:
                getServerTime = session.get("http://abenaquicc.mfteetimes.com/igolf/includes_admin/ajax/misc/getServerTime")
                serverTime = getServerTime.headers['Date'][-12:-4]
                print(serverTime)
                if serverTime == "00:00:01" or serverTime == "00:00:02" or serverTime == "01:00:01" or serverTime == "01:00:02" or serverTime == "20:00:01" or serverTime == "20:00:02":
                    break
                print("TEE SHEET CLOSED")
                time.sleep(1)

        print("TEE SHEET IS OPEN")
        time.sleep(1)

        print("REQUESTING TEE TIME OF " + self.tee_time + " on " + self.date + "...")
        session = self.request_tee_time(session)
        if not session:
            print("Error requesting tee time, another member may already be requesting that time")
            return "Error requesting tee time, another member may already be requesting that time"

        # print("\n\n\n\n\nSUBMITTING BOOKING")
        # # submit booking
        # # formHeaders = {"accept": "*/*",
        # #                "Accept-Encoding": "gzip, deflate, br",
        # #                "Accept-Language": "en-US,en;q=0.5",
        # #                "Connection": "keep-alive",
        # #                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        # #                "Host": "abenaquicc.mfteetimes.com",
        # #                "Origin": "https://abenaquicc.mfteetimes.com",
        # #                "Referer": "https://abenaquicc.mfteetimes.com/teetimes.php",
        # #                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
        # #                "X-Requested-With": "XMLHttpRequest"
        # # }
        #
        # #removed content length
        # formHeaders = {"accept": "*/*",
        #                "accept-encoding": "gzip, deflate, br",
        #                "accept-language": "en-US,en;q=0.9",
        #                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        #                "cookie": "__cfduid=d28e070d7c083966e44d5eb020358f7771619206651; PHPSESSID=14c79c3119fdb9da70c9299a0f2dfab3; _ga=GA1.2.1404092740.1619208706; _gid=GA1.2.1408328964.1619208706; _gat=1",
        #                "origin": "https://abenaquicc.mfteetimes.com",
        #                "referer": "https://abenaquicc.mfteetimes.com/teetimes.php",
        #                "sec-ch-ua": "\"Google Chrome\";v=\"89\", \"Chromium\";v=\"89\", \";Not A Brand\";v=\"99\"",
        #                "sec-ch-ua-mobile": "?0",
        #                "sec-fetch-dest": "empty",
        #                "sec-fetch-mode": "cors",
        #                "sec-fetch-site": "same-origin",
        #                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        #                "x-requested-with": "XMLHttpRequest"
        # }
        # formData = {'dateof:': self.date,
        #             'timeof': self.tee_time,
        #             'timeofOriginal': self.tee_time,
        #             'year': str(self.year),
        #             'month': str(self.month),
        #             'day': str(self.day),
        #             'course': '1',
        #             'hole': '1',
        #             'blockId': '0',
        #             'specialRequests': '',
        #             'players[0][id]': 'U1432',
        #             'players[0][trueId]': '1432',
        #             'players[0][playerType]': 'user',
        #             'players[0][bookedBy]': 'U1432',
        #             'players[0][name]': 'Ockert, Benjamin',
        #             'players[0][gender]': 'm',
        #             'players[0][cart_pref]': '0',
        #             'players[0][birthday]': '2000-07-10',
        #             'players[0][email]': 'benpiano710@gmail.com',
        #             'players[0][group]': 'FAMGF.DEP',
        #             'players[0][groupId]': '29',
        #             'players[0][isBuddy]': '0',
        #             'players[0][phone]': '',
        #             'players[0][imageUrl]': '',
        #             'players[0][isRestricted]': '0',
        #             'players[0][restrictedByGender]': '0',
        #             'players[0][restrictedByAge]': '0',
        #             'players[0][hasRequiredLeague]': '1',
        #             'players[0][memberType]': 'member',
        #             'players[0][holesToPlay]': '18',
        #             'recaptcha': '',
        #             'newMultiLock': ''}
        # submitTeeTime = session.post("http://abenaquicc.mfteetimes.com/igolf/includes_front/teesheet2017/bookingInterface/api/Services/Reservation/TeeTime", data=formData, headers=formHeaders)
        # print("............................................\n")
        # print("REQUEST HEADERS: " + str(submitTeeTime.request.headers))
        # print("............................................\n")
        # print("RESPONSE HEADERS: " + str(submitTeeTime.headers))
        # print("............................................\n")
        # print("SERVER RESPONSE: " + str(submitTeeTime.status_code))
        # print(submitTeeTime.text)

def tee_bot(u, p, d, t):

    TeeTimeBot = TeeTime(u.decode("utf-8"), p.decode("utf-8"), d.decode("utf-8"), t.decode("utf-8"))

    return TeeTimeBot.make_tee_time()
