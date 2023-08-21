import v2enlib.utils as utils
from v2enlib.libs import *


scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]
creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
client = gspread.authorize(creds)
googleSheet = client.open("MyDatabase")


def createOBJPool(cmds):
    googleSheet.worksheet(const.worksheet_name).append_rows(cmds)


def getSQL(conn, request):
    cursor = conn.cursor()
    cursor.execute(request)
    return cursor.fetchall()
