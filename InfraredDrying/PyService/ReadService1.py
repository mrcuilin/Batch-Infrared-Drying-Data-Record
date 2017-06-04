import serial
import time
import sys
import MySQLdb
from Consts1 import *

# 5 Seconds



def LOG( Prefix , Message ) :
    if Prefix in LOG_LEVEL :
        print Prefix + ":" + Message
    return

def initDBConn() :
    try :
        db = MySQLdb.connect( DB_SPEC[0], DB_SPEC[2],DB_SPEC[3], DB_SPEC[4], int( DB_SPEC[1]) )
        return db
    except Exception,e:  
        print Exception,":",e
        LOG("ERROR","DB Init failed" + str( DB_SPEC ))
        sys.exit()

def loadSampleInterval( DB ) :
    global SAMPLE_INTERVAL
    curs = DB.cursor()
    curs.execute( "select * from status where `KEY` = 'SAMPLEINTERVAL' ")
    data = curs.fetchone()
    SAMPLE_INTERVAL = int( data[1] )
    curs.close()
    DB.commit()
    return

def clearDBStatus( DB, grpId ) :
    curs = DB.cursor()
    curs.execute( "update `status` set `VALUE`='NO' where `KEY`='RUNNING' and SGROUP = '" + grpId + "'" )
    curs.close()
    DB.commit()
    return
    

def loadStatus( DB, sensorGroup ) :
    global RUNNING
    global ENABLED
    global CURRENT_SESSION
    DB.commit()
    curs = DB.cursor()
    SQLCMD = "select * from `status` where `KEY`='RUNNING' and `SGROUP` = '" + sensorGroup + "' "
    curs.execute( SQLCMD )
    data = curs.fetchone()
    if data[1] == "NO" :
        RUNNING = False
    else :
        RUNNING = True
    curs.close()
    
    curs = DB.cursor()
    SQLCMD = "select * from `status` where `KEY`='ENABLE' and `SGROUP` = '" + sensorGroup + "' "
    curs.execute( SQLCMD )
    data = curs.fetchone()
    if data[1] == "NO" :
        ENABLED = False
    else :
        ENABLED = True
    curs.close()

    if RUNNING and ENABLED :
        curs = DB.cursor()
        SQLCMD = "select * from `status` where `KEY`='SESSION' and `SGROUP` = '" + sensorGroup + "' "
        curs.execute( SQLCMD )
        data = curs.fetchone()
        CURRENT_SESSION = data[1].strip()
        curs.close()

    DB.commit()
    return


def Sample( DB, CP, sensorGP ) :
    global RUNNING
    global ENABLED
    global CURRENT_SESSION
    loadStatus( DB , sensorGP )
    if ( not ENABLED ) or ( not RUNNING ) or ( CURRENT_SESSION == None ) or ( CURRENT_SESSION == "" ):
        return

    NetWeight = weight( CP );
    time.timezone = 28800;
    nowStr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime( time.time() ))

    if( NetWeight[0] <> "-200" ) :
        SQL = "INSERT INTO sensordata values('" + str(( time.time() )) + "'," + \
                  "'" + CURRENT_SESSION + "'," + \
                  "'" + NetWeight[0] + "'," + \
                  "'" + NetWeight[1] + "','','','','','','','',''," + \
                  "'" + nowStr + "'," + \
                  "'" + str( sensorGP ) + "')"
        curs = DB.cursor()
        curs.execute( SQL )
        LOG("DEBUG","DB Saved " + str( NetWeight) )
        DB.commit()
        curs.close()
    else :
        LOG("DEBUG","DB Skiped " + str( NetWeight) )


# INITIALIZE a Serial Comm Port
#     return  : The Created Serial Object
def initCommPort() :
    
    try :
        SE = serial.Serial( COM_PORT, COM_BAUD )
    except :
        LOG("ERROR","Initialize Serial Port Failed..")
        sys.exit()
        

    reTryTimes = 0
    inBufferSize = 0

    while inBufferSize == 0 and reTryTimes < initRetryTimesLimit :
        SE.write( INIT_CMD )
        SE.write( INIT_CMD )    
        reTryTimes = reTryTimes + 1
        time.sleep(1)
        inBufferSize = SE.inWaiting()
        LOG("MESSAGE","Initialize Equipment, try " + str(reTryTimes) + " time..")
        
    LOG("MESSAGE",SE.read( SE.inWaiting() ) )

    LOG("NOTIFY", "Equipment Ready !" )
        
    return SE


# DISPLAY a set of Strings in the equipment
#     CP : The Serial Object
#     NotifyMsg : A List of String, messages
#     interval : The display time interval between 2 messages
#   return  NULL
def showNotify(CP, NotifyMsg, interval ) :
    for notify in NotifyMsg :
        show( CP, notify )
        time.sleep( interval  )
    showDefault( CP ) 

def show( CP, MSG ) :
    CMD = SHOW_MSG_CMD.replace("%S", MSG )
    CP.write( CMD )
    LOG("MESSAGE","CMD " + CMD )

def showDefault( CP ) :
    CP.write( SHOW_DEFAULT_CMD )
    LOG("MESSAGE","CMD " + SHOW_DEFAULT_CMD )
    
def clearBuffer( CP ) :
    CP.read( CP.inWaiting())
    LOG("MESSAGE","Clear Comm buffer")

def weight( CP ) :
    clearBuffer( CP )    
    #show( CP, "READING " + SensorNum )
    #time.sleep( 0.5 )
    #clearBuffer( CP )    
    #showDefault( CP )
    #time.sleep( 0.5 )
    #clearBuffer( CP )

    startT = time.time()
    CP.write( WEIGHT_CMD )
    weightStable = False
    while ( startT + WeightTimeup ) > time.time() and ( not weightStable ) :
        time.sleep(0.1)
        LOG("DEBUG","Wait For " + str( time.time()-startT ) )
        recLen = CP.inWaiting()
        if recLen >= 18 :
            weightStable = True

    W = CP.read( CP.inWaiting())

    if len( W ) > 18 :
        W = W[ len(W)-18: len(W)]

    Results1 = W.split()

    LOG( "DEBUG", str( Results1) )
    if len( Results1 ) == 4 :
        return [ Results1[2], "0" ]
    else :
        return [ str(-200), str(-200) ]
    

DBC = initDBConn()

clearDBStatus( DBC, grpId )

loadSampleInterval( DBC )
                                                  
CommPort = initCommPort()
LOG( "MESSAGE" , str( CommPort ))

showNotify( CommPort, ['HELLO','BEGIN...'], 0.5 )

clearBuffer( CommPort )

while True :
    #Wg = weight( CommPort )
    Sample( DBC, CommPort, grpId )
    time.sleep( SAMPLE_INTERVAL )

DBC.close()
CommPort.close()

sys.exit()
