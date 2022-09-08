import sys
import os
import hashlib
import pathlib
import csv
import datetime

#note on limitation of script, if there is a large number of files this program will load into memory alot of file names.
#errors out when no duplicates are found
def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk

def check_for_duplicates(paths, hash=hashlib.sha1):
    duplicates = []
    hashes = {}
    for path in paths:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                hashobj = hash()
                for chunk in chunk_reader(open(full_path, 'rb')):
                    hashobj.update(chunk)
                file_id = (hashobj.digest(), os.path.getsize(full_path))
                duplicate = hashes.get(file_id, None)
                if duplicate:
                    print("Duplicate found: %s and %s" % (full_path, duplicate))
                    duplicates.append({'from': duplicate,'duplicate': full_path})
                    
                else:
                    hashes[file_id] = full_path
    return duplicates

def pathing():
    local =os.environ['appdata']
    #create uneque dir
    speed_test_dir1 = f'\\duplicate_log'
    speed_test_dir2	= '\\results'
    Trec = datetime.datetime.now()
    date = Trec.strftime("%d_%m_%Y")
    time = Trec.strftime("__%H_%M")
    root_dir = local + speed_test_dir1 + speed_test_dir2 + date + time
    print('root_DIR: {}'.format(root_dir))
    if pathlib.Path(root_dir).exists() != bool(True):
        try: os.mkdir(local + speed_test_dir1)
        except OSError:
            print(f"path exists {local + speed_test_dir1}")
        os.mkdir(root_dir)
    return root_dir

def write_out_log(resultsDictL,oPath, mode):
    if len(resultsDictL) == 0: print('nothing to log'); return
    if pathlib.Path(oPath).exists() and not mode == 'w':
        with open(oPath, mode, encoding='UTF8', newline='') as f:
            fields = list(resultsDictL[0].keys())
            obj=csv.DictWriter(f, fieldnames=fields)
            obj.writerows(resultsDictL)
            print ("file exists adding rows")
    else:
        with open(oPath, mode, encoding='UTF8', newline='') as f:
            fields = list(resultsDictL[0].keys())
            obj=csv.DictWriter(f, fieldnames=fields)
            obj.writeheader()
            obj.writerows(resultsDictL)
            print("new file created: %s" % (oPath))

def chkInt(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

def delete_method(dataDictList, path):
    print("""
    /////////////////////////////////
    DELETION METHOD!! choose an option
    1 - delete all occourances after the first
    2 - decide on each case
    3 - delete specific file type
    0 - exit script without deleting
    /////////////////////////////////
    """)
    userChoice = input('enter value: ')
    #ensure that the input is an integer and one of the options
    if not chkInt(userChoice): print("ERROR please enter a integer number! try again"); delete_method(dataDictList)
    elif int(userChoice) == 1:
        #delete all none first occourances
        print('holder')
        for dupDict in dataDictList:
            try: os.remove(dupDict['duplicate']); write_out_log([{'File':dupDict['duplicate'],'Deleted':'YES'}],path, 'a+')
            except OSError:
                write_out_log({'File':dupDict['duplicate'],'Deleted':'NO'},path, 'a+')

    elif int(userChoice) == 2:
        #decide on each
        print('holder2')
    elif int(userChoice) == 3:
        #delete specific file type
        print('holder3')
    else:
        #invalid input
        print('invalid input, no action will be taken')

    #match userChoice:
    #        case "1":
                #delete all none first occourances
                #print('holder')
                #for i in dataDictList:
                #    print(i['duplicate'])

    #        case "2":
    #            #decide on each
    #            print('holder2')
    #        case "3":
    #            #exit and do nothing
    #            print('holder3')
    #        case _:
    #            #invalid input
    #            print('holder4')



if __name__ == "__main__":
    if sys.argv[1:]:
        dups = check_for_duplicates(sys.argv[1:])
        #dups = ''
        path = pathing()
        write_out_log(dups, path + '\\duplicates.csv', 'w')
        delete_method(dups, path + '\\duplicate_deletes.csv')
    else:
        print("Please pass the paths to check as parameters to the script")