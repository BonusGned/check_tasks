from pprint import pprint

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

# Файл, полученный в Google Developer Console
from .models import User, Answer, TaskConditional

CREDENTIALS_FILE = 'cred.json'
# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = '1izrQJNYwBVtcZzUXqYD6uhQi9nOjtIaEJw2TSXfU61g'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)


def sync_google_sheets():
    # for user in User.objects.all():
    data = []
    count = 1
    for user in User.objects.all():
        user_answers = TaskConditional.objects.filter(user=user).values_list('user_answer', flat=True)
        status_tasks = TaskConditional.objects.filter(user=user).values_list('status_task', flat=True)
        data.extend((user.email, user.username, *user_answers, *status_tasks, user.total_appraisal))
        count += 1
        print(count)
        values = service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": "C1:M1",
                     "majorDimension": "ROWS",
                     "values": [list(Answer.objects.filter(is_true=True).values_list('answer_content', flat=True))]},
                    {"range": f"A{count}:CZ{count}",
                     "majorDimension": "ROWS",
                     "values": [data]}
                ]
            }
        ).execute()
        data.clear()
