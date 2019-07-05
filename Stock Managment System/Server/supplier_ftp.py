import sys, string, os, yaml
import ftplib
sys.path.insert(0, "../")
with open("config.yml", 'r') as cfg:
    config = yaml.load(cfg, Loader=yaml.FullLoader)

def getFile(supplier):
    # Gets values from config
    user = config['suppliers'][supplier]['user']
    passwd = config['suppliers'][supplier]['passwd']
    path = config['suppliers'][supplier]['file']

    # Break path down into attributes and create path
    pathspl = path.split("/")
    wd = "/".join(pathspl[1:len(pathspl)-1])
    filename = pathspl[len(pathspl)-1]
    outpath = "Suppliers/"+supplier.upper()+"/"+filename

    # Connect to FTP Server and move to working dir
    ftp = ftplib.FTP(pathspl[0], user, passwd)
    ftp.cwd(wd)

    # Save file
    localfile = open(outpath, 'wb')
    ftp.retrbinary('RETR ' + filename, localfile.write, 1024)

    # Close
    ftp.quit()
    localfile.close()
