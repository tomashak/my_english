from __future__ import print_function
from genericpath import exists
import os.path
import unicodedata
import string
import gtts
from playsound import playsound
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
# https://docs.google.com/spreadsheets/d/1fbV52htaYK1j0eOnaHBUrxqhJX7AFVReOPdN6KbscJ0/edit?usp=sharing
SAMPLE_SPREADSHEET_ID = '1fbV52htaYK1j0eOnaHBUrxqhJX7AFVReOPdN6KbscJ0'
SAMPLE_RANGE_NAME = 'english!A2:E805'

valid_filename_chars = "-_() %s%s" % (string.ascii_letters, string.digits)
char_limit = 255

def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    # replace spaces
    for r in replace:
        filename = filename.replace(r,'_')
    
    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
    
    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    if len(cleaned_filename)>char_limit:
        print("Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(char_limit))
    return cleaned_filename[:char_limit]  

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    print(values)
    if not values:
        print('No data found.')
    else:
        print('Data OK')
        output = ""
        for row in values:            
            HTMLrow = "<tr>\r\n"
            print('------------')
            print(row)
            if len(row) >= 2:
                HTMLrow =  HTMLrow + '<td class="column1">'+ row[0] +' <button onclick="playSound(\'mp3/'+clean_filename(row[0])+'.mp3'+'\');">&#9836;</button></td>\r\n'
                #print(clean_filename(row[0])+'.mp3')
                if not os.path.exists('web/mp3/'+clean_filename(row[0])+'.mp3'):
                    tts = gtts.gTTS(row[0], lang="en")
                    tts.save('web/mp3/'+clean_filename(row[0])+'.mp3')
                    #print('MP3 created')
                #print(row[1])
                HTMLrow =  HTMLrow + '<td class="column2">'+row[1]+'</td>\r\n'
                if len(row) >= 3:
                    #print(row[2])
                    HTMLrow =  HTMLrow + '<td class="column3">'+row[2]+'</td>\r\n'
                else:
                    HTMLrow =  HTMLrow + '<td class="column3">N/A</td>\r\n'
                if len(row) >= 4:
                    #print(clean_filename(row[3])+'.mp3')
                    HTMLrow =  HTMLrow + '<td class="column4">'+ row[3] +' <button onclick="playSound(\'mp3/'+clean_filename(row[3])+'.mp3'+'\');">&#9836;</button></td>\r\n'
                    if not os.path.exists('web/mp3/'+clean_filename(row[3])+'.mp3'):
                        tts = gtts.gTTS(row[3], lang="en")
                        tts.save('web/mp3/'+clean_filename(row[3])+'.mp3')
                        #print('MP3 created')
                else:
                    HTMLrow =  HTMLrow + '<td class="column4">N/A</td>\r\n'
                if len(row) >= 5:
                    HTMLrow =  HTMLrow + '<td class="column5">'+row[4]+'</td>\r\n'
                    #print(row[4])
                else:
                    HTMLrow =  HTMLrow + '<td class="column5">N/A</td>\r\n'
            HTMLrow = HTMLrow+"</tr>\r\n"
            output = output + HTMLrow
        print('vysledek:  '+output)
        inputfile = open('web/index_above.html',  encoding='utf8')
        outputfile = open('web/index.html', 'w', encoding='utf8')
        for s in inputfile.readlines():
            outputfile.write(s.replace('<!--=PLACEHOLDER=-->',output))
        outputfile.close()
        inputfile.close()


if __name__ == '__main__':
    main()