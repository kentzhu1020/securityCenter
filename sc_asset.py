import pycurl
import json
from io import BytesIO
import os,sys
import getpass
import getopt
import csv

def get_token(api_cmd,serveraddr,username,password):
    curl_base = "https://" + serveraddr + "/rest/"
    curlcmd = curl_base + api_cmd
    content_type = 'application/json'
    headers = ['Content-Type:'+content_type]
    buffer = BytesIO()
    post_data = {
        'username'           : username,
        'password'           : password,  
    }
    postfields = json.dumps(post_data)
    c = pycurl.Curl()
    c.setopt(c.URL, curlcmd)
    c.setopt(c.HTTPHEADER,headers)
    c.setopt(c.SSL_VERIFYPEER, False)
    c.setopt(c.POST, 1)
    c.setopt(c.POSTFIELDS, postfields)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(c.COOKIEJAR, 'cookie.txt')
    c.perform()
    c.close()
    response = json.loads(buffer.getvalue())
    return response['response']['token']

def create_an_asset(api_cmd,serveraddr,token,name,description,network):
    curl_base = "https://" + serveraddr + "/rest/"
    curlcmd = curl_base + api_cmd
    post_data = {
        'type' : 'static',
        'name' : name,
        'description':description,
        'definedIPs' : network,
    }
    postfields = json.dumps(post_data)
    buffer = BytesIO()
    content_type = "application/json"
    headers = ["Content-Type:"+ content_type,"X-SecurityCenter:"+ token]
    c = pycurl.Curl()
    c.setopt(c.URL, curlcmd)
    c.setopt(c.HTTPHEADER,headers)
    c.setopt(c.POST, 1)
    c.setopt(c.POSTFIELDS, postfields)
    c.setopt(c.COOKIEFILE,'cookie.txt')
    c.setopt(c.SSL_VERIFYPEER, False)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    http_code = c.getinfo(c.HTTP_CODE)
    c.close()
    response = json.loads(buffer.getvalue())
    return http_code

def get_asset(api_cmd,serveraddr,token,querystring=None):
    curl_base = "https://" + serveraddr + "/rest/"
    if querystring is None:
        curlcmd = curl_base + api_cmd
    else:
        curlcmd = curl_base + api_cmd + "/" +querystring;
    buffer = BytesIO()
    content_type = "application/json"
    headers = ["Content-Type:"+ content_type,"X-SecurityCenter:"+ token]
    c = pycurl.Curl()
    c.setopt(c.URL, curlcmd)
    c.setopt(c.HTTPHEADER,headers)
    c.setopt(c.COOKIEFILE,'cookie.txt')
    c.setopt(c.SSL_VERIFYPEER, False)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    response = json.loads(buffer.getvalue())
    return response

def delete_token(api_cmd,serveraddr,token):
    curl_base = "https://" + serveraddr + "/rest/"
    curlcmd = curl_base + api_cmd
    content_type = 'application/json'
    headers = ["Content-Type:"+ content_type,"X-SecurityCenter:"+ token]
    c = pycurl.Curl()
    c.setopt(c.URL, curlcmd)
    c.setopt(c.HTTPHEADER,headers)
    c.setopt(c.SSL_VERIFYPEER, False)
    c.setopt(pycurl.CUSTOMREQUEST, "DELETE")
    c.setopt(c.COOKIEFILE, 'cookie.txt')
    c.perform()
    http_code = c.getinfo(c.HTTP_CODE)
    c.close()
    if os.path.exists('cookie.txt'):
        os.unlink('cookie.txt')
    return http_code

def main():
    global log_dir
    global log_file
    global log_fp
    path = os.path.dirname(os.path.realpath(__file__))
    log_dir = path+'/log'
    log_file = log_dir+'/sc.debug'
    try:
        log_fp = open(log_file, 'a')
    except:
        pass

def logger(message=''):
    import datetime
    try:
        global log_fp
        global log_dir
        global log_file
        if os.path.isfile(log_file):
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            log_fp.write("%s\t%s\n" % (now, message))
        else:
            os.system("mkdir -p "+log_dir)
            os.system("touch "+log_file)
            log_fp = open(log_file, 'a')
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            log_fp.write("%s\t%s\n" % (now, message))
            # log_fp.close()
    except Exception as er:
        print "[-] Exception occurred while calling the logger "
        print "[-] Error is "+str(er)

def remove_an_asset(api_cmd,serveraddr,token,querystring=None):
    curl_base = "https://" + serveraddr + "/rest/"
    if querystring is None:
        curlcmd = curl_base + api_cmd
    else:
        curlcmd = curl_base + api_cmd + "/" +querystring;
    content_type = 'application/json'
    headers = ["Content-Type:"+ content_type,"X-SecurityCenter:"+ token]
    c = pycurl.Curl()
    c.setopt(c.URL, curlcmd)
    c.setopt(c.HTTPHEADER,headers)
    c.setopt(c.SSL_VERIFYPEER, False)
    c.setopt(pycurl.CUSTOMREQUEST, "DELETE")
    c.setopt(c.COOKIEFILE, 'cookie.txt')
    c.perform()
    http_code = c.getinfo(c.HTTP_CODE)
    c.close()
    return http_code

def view_all(serveraddr):
    while True:
        username = raw_input('Enter SecurityCenter username: ')
        password = getpass.getpass('Enter SecurityCenter password: ')
        try:
            token = str(get_token('token',serveraddr,username,password))
            break
        except Exception as e:
            print "Username and Password is not match. Please enter your username and password!"
    response = get_asset("asset",serveraddr,token)
    print response
    delete_token("token",serveraddr,token)

def view_asset_by_id(serveraddr,arg):
    while True:
        username = raw_input('Enter SecurityCenter username: ')
        password = getpass.getpass('Enter SecurityCenter password: ')
        try:
            token = str(get_token('token',serveraddr,username,password))
            break
        except Exception as e:
            print "Username and Password is not match. Please enter your username and password!"            
    response = get_asset("asset",serveraddr,token,str(arg))
    print response
    delete_token("token",serveraddr,token)


def usage():
    print "script.py usage:"
    print "-h,print help message."
    print "-v,view all the asset."
    print "-d, view asset by id."
    print "-l, load all the asset into security center."
    print "-r, remove all the asset."
    print "-s, remove the asset by id."
    # print "-n, remove the asset by name."

def load_all_asset(filename,serveraddr):
    while True:
        username = raw_input('Enter SecurityCenter username: ')
        password = getpass.getpass('Enter SecurityCenter password: ')
        try:
            token = str(get_token('token',serveraddr,username,password))
            break
        except Exception as e:
            print "Username and Password is not match. Please enter your username and password!"
    with open(filename, 'rb') as f:
        reader = csv.DictReader(f)
        try:
            for row in reader:
                name = row['Name']
                description= row['Description']
                definedIPs = row['IP Addresses']
                http_code = create_an_asset("asset",serveraddr,token,name,description,definedIPs)
                if str(http_code)!= "200" :
                    logger('Network  %s  is failed to create' %(definedIPs))
                    continue     
        except csv.Error as e:
            logger('file %s, line %d: %s' % (filename, reader.line_num, e))
    delete_token('token',serveraddr,token)


def remove_asset_by_id(serveraddr,arg):
    while True:
        username = raw_input('Enter SecurityCenter username: ')
        password = getpass.getpass('Enter SecurityCenter password: ')
        try:
            token = str(get_token('token',serveraddr,username,password))
            break
        except Exception as e:
            print "Username and Password is not match. Please enter your username and password!"

    http_code = remove_an_asset('asset',serveraddr,token,arg)
    if str(http_code) != "200":
        print 'Failed to remove asset, asset id is %s' % (arg)
    else :
        print 'Successfully remove asset!'
    delete_token('token',serveraddr,token)



def remove_asset(serveraddr):
    while True:
        username = raw_input('Enter SecurityCenter username: ')
        password = getpass.getpass('Enter SecurityCenter password: ')
        try:
            token = str(get_token('token',serveraddr,username,password))
            break
        except Exception as e:
            print "Username and Password is not match. Please enter your username and password!"

    asset = get_asset("asset",serveraddr,token)
    try:
        count = int(asset['response']['manageable'][-1]['id'])
    except Exception as e:
        count = 0
    if count == 0:
        print "Empty asset, No need to remove!"
    else:
        for i in range(0,count):
            try:
                id =str(i)
                http_code = remove_an_asset("asset",serveraddr,token,id)
                print http_code
                if str(http_code) != "200":
                    logger('Failed to remove asset id is %s' % (id))
                    print 'Failed to remove asset id is %s' % (id)
                    continue
            except Exception as e:
                logger('Failed to remove asset id is %s, reseaon is %s' % (id,str(e)))
    delete_token('token',serveraddr,token)


###############################################################################
# Main Program
###############################################################################

if __name__ == '__main__':
    global log_dir
    global log_file
    global log_fp
    main()
    serveraddr = '10.10.0.142'
    path = os.path.dirname(os.path.realpath(__file__))
    filename = path+"/asset_config.csv"
    try:
        opts,args = getopt.getopt(sys.argv[1:],'hvlrd:n:s:')
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    for opt,arg in opts:
        if opt == '-h':
            usage()
            sys.exit(2)
        elif opt == '-v':
            view_all(serveraddr)
        elif opt == '-d':
            id = str(arg)
            view_asset_by_id(serveraddr,id)
        elif opt == '-l':
            load_all_asset(filename,serveraddr)
        elif opt == '-r':
            remove_asset(serveraddr)
        elif opt == '-s':
            id = str(arg)
            remove_asset_by_id(serveraddr,id)
        # elif opt == '-n':
        #     name = arg
        #     print name
        #     print "execute method for removing asset by name"
        else:
            print "unhandled options"
            sys.exit(3)
