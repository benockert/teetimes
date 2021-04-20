# Create a tee time for Abenaqui CC
import argparse
import requests
import time
from datetime import datetime, timedelta

from requests import Session


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
        self.month = date[0:2]
        self.day = date[3:5]
        self.year = date[6:10]
        self.tee_time = tee_time

    def is_tee_sheet_closed(self):
        right_now = datetime.now()
        five_days_from_now = (right_now + timedelta(days=5))

        print(five_days_from_now)

        requested_date_current_time = datetime(int(self.year), int(self.month), int(self.day), int(right_now.hour), int(right_now.minute), int(right_now.second))
        when_tee_sheet_opens = datetime(five_days_from_now.year, five_days_from_now.month, five_days_from_now.day, 20, 00, 00)

        print("request date current time = ", requested_date_current_time)
        print("tee sheet opens = ", when_tee_sheet_opens)

        return requested_date_current_time < when_tee_sheet_opens

    def get_date(self):
        tee_time_date = str(self.year) + "-" + str(self.month) + "-" + str(self.day)
        return tee_time_date

    def make_tee_time(self):
        session = NoRebuildAuthSession()

        # get login page
        session.get("https://www.abenaquicc.com/club/scripts/login/login.asp")

        # login
        print("LOGGING IN USER " + self.username + " ...")
        loginresponse = session.post("https://www.abenaquicc.com/club/scripts/login/Login_Validate.asp?GRP=36600&NS=PUBLIC", data={'user': self.username, 'pw': self.password, 'MemEnter': ''})

        # get tee sheet
        print("GETTING THE TEE SHEET FOR " + self.get_date() + "...")
        teesheetresponse = session.get("http://abenaquicc.mfteetimes.com/sso/?u=01457D&p=b3a4e9474edc367129b1eaf6d8bd9b4f25eecef6&date=" + self.get_date() + "&time=&t=MEMBERNUM&course=1")

        # wait for tee sheet to become open
        if self.is_tee_sheet_closed():
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

        # request the time
        print("REQUESTING TEE TIME OF " + self.tee_time + " on " + self.get_date() + "...")
        requestData = {'cmd': 'teesheet2017',
                       'action': 'teetime_interface_holes_to_play',
                       'slotsAvailable': '4',
                       'maxSlotsAvailable': '4',
                       'course': '1',
                       'dateof': self.get_date(),
                       'time': self.tee_time,
                       'year': str(self.year),
                       'month': str(self.month),
                       'day': str(self.day),
                       'hole': '1',
                       'block_id': '0',
                       'blockSpecialStartAltText': '',
                       'extraTimesVal': ''}
        #requesttime = session.post("http://abenaquicc.mfteetimes.com/teetimes.php?cmd=teesheet2017&action=display2017&jDate=2020-10-03&course=1", data=requestData)

        # continue through booking
        continueData = {'time': self.tee_time,
                        'course': '1',
                        'dateof': self.get_date(),
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
        #continuetosubmit = session.post("http://abenaquicc.mfteetimes.com/teetimes.php", data=continueData)
        #return continuetosubmit.status_code

        # submit booking
        formData = {'dateof:': self.get_date(),
                    'timeof': self.tee_time,
                    'timeofOriginal': self.tee_time,
                    'year': str(self.year),
                    'month': str(self.month),
                    'day': str(self.day),
                    'course': '1',
                    'hole': '1',
                    'blockId': '0',
                    'specialRequests': '',
                    'players[0][id]': 'U1432',
                    'players[0][trueId]': '1432',
                    'players[0][playerType]': 'user',
                    'players[0][bookedBy]': 'U1432',
                    'players[0][name]': 'Ockert, Benjamin',
                    'players[0][gender]': 'm',
                    'players[0][cart_pref]': '0',
                    'players[0][birthday]': '2000-07-10',
                    'players[0][email]': 'benpiano710@gmail.com',
                    'players[0][group]': 'FAMGF.DEP',
                    'players[0][groupId]': '29',
                    'players[0][isBuddy]': '0',
                    'players[0][phone]': '',
                    'players[0][imageUrl]': '',
                    'players[0][isRestricted]': '0',
                    'players[0][restrictedByGender]': '0',
                    'players[0][restrictedByAge]': '0',
                    'players[0][hasRequiredLeague]': '1',
                    'players[0][memberType]': 'member',
                    'players[0][holesToPlay]': '18/9',
                    'recaptcha': ''}
        # submitTeeTime = session.post("http://abenaquicc.mfteetimes.com/igolf/includes_front/teesheet2017/bookingInterface/api/Services/Reservation/TeeTime", data=formData)
        # print("............................................")
        # print("SERVER RESPONSE: " + submitTeeTime.status_code)
        # print(submitTeeTime.text)

def tee_bot(u, p, d, t):

    TeeTimeBot = TeeTime(u.decode("utf-8"), p.decode("utf-8"), d.decode("utf-8"), t.decode("utf-8"))

    return TeeTimeBot.make_tee_time()
