import requests
from requests import Session

class NoRebuildAuthSession(Session):
    def rebuild_auth(self, prepared_request, response):
        """
        No code here means requests will always preserve the Authorization
        header when redirected.
        Be careful not to leak your credentials to untrusted hosts!
        """

def remove_lock(u, p, d, t, id):
    session = NoRebuildAuthSession()
    username = u.decode("utf-8")
    password = p.decode("utf-8")
    date = d.decode("utf-8")
    time = t.decode("utf-8")
    block_id = id

    #LOGIN
    session.get("https://www.abenaquicc.com/club/scripts/login/login.asp")
    loginresponse = session.post("https://www.abenaquicc.com/club/scripts/login/Login_Validate.asp?GRP=36600&NS=PUBLIC", data={'user': username, 'pw': password, 'MemEnter': ''})
    print(loginresponse.status_code)
    print(loginresponse.headers)
    print(loginresponse.content)

    #ACCESS TEESHEET (first for today's date and then for the relevant date)
    session.get("http://abenaquicc.mfteetimes.com/sso/?u=01457D&p=b3a4e9474edc367129b1eaf6d8bd9b4f25eecef6&date=&time=&t=MEMBERNUM&course=1")
    session.get("http://abenaquicc.mfteetimes.com/teetimes.php?cmd=teesheet2017&action=display2017&jDate=" + date + "&course=1")

    #REMOVE LOCK
    response = session.get("http://abenaquicc.mfteetimes.com/teetimes.php?cmd=teesheet2017&jDate=" + date + "&jTime=" + time + "&course=1&removeLock=" + str(block_id))

    return response.status_code
