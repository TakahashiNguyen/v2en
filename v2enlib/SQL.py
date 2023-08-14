import sqlite3, v2enlib.utils as utils
import gspread
from oauth2client.service_account import ServiceAccountCredentials


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
        if obj[0] and obj[1] and obj[2]:
            googleSheet.worksheet("sentences").insert_row([obj[0], obj[1]], index=1)
    except Exception as e:
        utils.printError(createOBJ.__name__, e, False)


def createOBJPool(cmds):
    for cmd in cmds:
        createOBJ(*cmd)


def getSQL(conn, request):
    cursor = conn.cursor()
    cursor.execute(request)
    return cursor.fetchall()
