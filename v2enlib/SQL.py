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
googleSheet = client.open("Moon'sVoiceDatabase")


def createOBJ(obj):
    try:
        if obj[0] and obj[1]:
            googleSheet.worksheet(const.worksheet_name).append_row([obj[0], obj[1]])
    except Exception as e:
        utils.printError(createOBJ.__name__, e, False)


def createOBJPool(cmds):
    for cmd in cmds:
        createOBJ(*cmd)


def getSQL(conn, request):
    cursor = conn.cursor()
    cursor.execute(request)
    return cursor.fetchall()
