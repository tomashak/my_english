from __future__ import print_function
from genericpath import exists
import os.path
import unicodedata
import string
import gtts
import csv


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
    # Cesta k CSV souboru
    csv_file_path = 'data/english.csv'

    # Načtení dat z CSV souboru
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        values = list(reader)[1:]  # Přeskočit první řádek (záhlaví)

    if not values:
        print('No data found.')
    else:
        print('Data OK')
        print(values)
        output = ""
        for row in values:            
            HTMLrow = "<tr>\r\n"
            print('------------')
            print(row)
            row = str(row).replace('"','').replace('[','').replace(']','').replace('\'','').split(';')
            print(row)
            if len(row) >= 2:
                HTMLrow =  HTMLrow + '<td class="column1">'+ row[0] +' <button onclick="playSound(\'mp3/'+clean_filename(row[0])+'.mp3'+'\');">&#9836;</button></td>\r\n'
                #print(clean_filename(row[0])+'.mp3')
                if not os.path.exists('web/mp3/'+clean_filename(row[0])+'.mp3'):
                    tts = gtts.gTTS(row[0], lang="en")
                    tts.save('web/mp3/'+clean_filename(row[0])+'.mp3')
                    #print('MP3 created')
                #print(row[1])
                HTMLrow =  HTMLrow + '<td class="column1">'+ row[1] +' <button onclick="playSound(\'mp3/'+clean_filename(row[1])+'.mp3'+'\');">&#9836;</button></td>\r\n'
                #print(clean_filename(row[0])+'.mp3')
                if not os.path.exists('web/mp3/'+clean_filename(row[1])+'.mp3'):
                    tts = gtts.gTTS(row[1], lang="en")
                    tts.save('web/mp3/'+clean_filename(row[1])+'.mp3')
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