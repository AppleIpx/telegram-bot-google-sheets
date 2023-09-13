import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials


creds = 'creds.json'    #my_APIs
table_ID = ''   #google sheets ID
read_from_file = ServiceAccountCredentials.from_json_keyfile_name(creds, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

identification = read_from_file.authorize(httplib2.Http())  #log_in
choose_for_working = apiclient.discovery.build('sheets', 'v4', http=identification)

#working with google libraries for reading

def checking_date_for_repeat(date):

    global checkpoint_for_repeat , last_checkpoint
    values = choose_for_working.spreadsheets().values().get(
    spreadsheetId=table_ID,
    range='A2:A50',
    majorDimension='ROWS').execute()


    for i in range (len(values['values'])):
        if date == values['values'][i][0]:
            checkpoint_for_repeat = i
            last_checkpoint = len(values['values'])
            return True
        elif date != values['values'][i][0]:
            checkpoint_for_repeat = i
            last_checkpoint = len(values['values'])
            if i == len(values['values']) + 1:
                return False

def writing_date_and_event(event, date):
    check = last_checkpoint + 2
    checkA = 'A' + str(check)
    checkB = 'B' + str(check)
    values = choose_for_working.spreadsheets().values().batchUpdate(
        spreadsheetId=table_ID,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {'range': f'{checkA}:{checkB}',
                "majorDimension": "COLUMNS",
                "values": [[f'{date}'], [f'{event.text}']]
                }
            ]
        }).execute()


def adding_last_event(event):
    check = checkpoint_for_repeat
    values = choose_for_working.spreadsheets().values().get(
        spreadsheetId=table_ID,
        range='B2:B50',
        majorDimension='ROWS').execute()
    old_description = values['values'][check][0]
    check += 2

    checkB = 'B' + str(check)
    event = str(old_description) + ' ' + str(event.text)
    values = choose_for_working.spreadsheets().values().batchUpdate(
        spreadsheetId=table_ID,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {'range': f'{checkB}',
                "majorDimension": "COLUMNS",
                "values": [[f'{event}']]
                }
            ]
        }).execute()
