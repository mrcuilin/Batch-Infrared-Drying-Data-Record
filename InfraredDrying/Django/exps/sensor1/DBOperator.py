import logging
from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

import MySQLdb
from operator import itemgetter, attrgetter
import time

import string
import os
import datetime

logger = logging.getLogger('sensor')
fh = logging.FileHandler('/home/pi/DryingExp/Django/exps/log/sensors.log')
formatter = logging.Formatter('%(asctime)s %(message)s')
fh.setFormatter(formatter)
logger.addHandler( fh )
logger.setLevel( logging.INFO )




def getDBC() :
    db = MySQLdb.connect('127.0.0.1', 'root', '', 'serialdata', 3306 )
    return db

def releaseDB( db ) :
    db.commit()
    db.close()

def query_( dbc, SQL ) :
    logger.debug( SQL )
    curs = dbc.cursor()
    curs.execute( SQL )
    data = curs.fetchall()
    logger.debug( "Get Records Success" )
    curs.close()
    return data

def query( SQL ):
    db = getDBC()
    data = query_( db, SQL )
    db.close()
    return data

def execute( SQL ) :
    db = getDBC()
    execute_( db, SQL )
    db.close()

def execute_( dbc, SQL ) :
    logger.debug( SQL )
    curs = dbc.cursor()
    R = curs.execute( SQL )
    logger.debug( R )
    dbc.commit()
    curs.close()

def getEnableStatus( grpId ) :
    SQL = "select * from `status` where `KEY`='ENABLE' and `SGROUP`='" + grpId+ "'"
    data = query(SQL)
    if len(data)> 0 and data[0][1]=="YES" :
        return True
    else :
        return False

def getRunningStatus( grpId ) :
    SQL = "select * from `status` where `KEY`='RUNNING' and `SGROUP`='" + grpId+ "'"
    data = query(SQL)
    if len(data) > 0 and data[0][1]=="YES" :
        return True
    else :
        return False

def getCurrentSessionId( grpId ) :
    SQL = "select `VALUE` from `status` where `KEY`='SESSION' and `SGROUP`='" + grpId + "'"
    data = query(SQL)
    if len(data) > 0:
        return data[0][0]
    else:
        return ""

def getCurrentSession( grpId ) :
    sesid = getCurrentSessionId( grpId )
    if( sesid == "" ) :
        return None;
    ses = getSessionSelf( sesid, grpId  )
    return ses

def getSessionSelf( ses, grpId ) :
    SQL = "select * from `datasession` where `sessionid` = '" + ses + "' and s_sensorGroup ='" + grpId + "'"
    data = query(SQL)
    return data[0]

def getRecentRecords( grpId ) :
    ses = getCurrentSession( grpId )
    if ses == None :
        return None
    SQL = "select * from `sensordata` where `sessionid`='" + ses[0] + "' and sensorGroup = '" + grpId + "' order by `dataid` DESC limit 0, 10"
    data = query( SQL )
    return data

def getRecord( ses, grpId ) :
    SQL = "select * from `sensordata` where `sessionid`='" + ses + "' and sensorGroup = '" + grpId + "' order by `dataid`"
    data = query( SQL )
    return data

def listSessionYears( grpid ) :
    SQL = "select sessionid from `datasession` where `s_sensorGroup`='" + grpid + "'";
    data = query( SQL )
    years = set()
    for d in data :
        oneDid = d[0][0:4]
        years.add( oneDid )
    years = sorted( years )
    return years

def listDays( grpId, yearId ) :
    SQL = "Select sessionid from `datasession` where `s_sensorGroup`='" + grpId + "' and sessionid like '" + yearId + "%'";
    data = query( SQL )
    days = set()
    for d in data :
        oneDid = d[0][0:8]
        days.add( oneDid )
    days = sorted( days )
    return days

def listSessions( grpid, dayId ) :
    SQL = "Select A.*, B.sessionid, count(*) from `datasession` as A , `sensordata` as B where `s_sensorGroup`='" + grpid + "' and A.sessionid like '" + dayId + "%' and A.sessionid = B.sessionid group by B.sessionid ";
    data = query(SQL)
    sessions = sorted( data , key=itemgetter(0) )
    return sessions

def startSample( grpid ) :
    isRunning = getRunningStatus( grpid )
    isEnabled = getEnableStatus( grpid )
    if isRunning or ( not isEnabled ) :
        return
    SQL = "update `status` set `VALUE`='YES' where `KEY`='RUNNING' and `SGROUP`='" + grpid + "'";
    execute( SQL )

    time.timezone = -28800
    nowStr = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time() + 28800))
    #nowDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime( time.time() + 28800 ))
    nowDate = str( time.time())
    SQL = "update `status` set `VALUE`='" + nowStr + "' where `KEY`='SESSION' and `SGROUP`='" + grpid + "'";
    execute( SQL )

    SQL = "insert into `datasession` values('" + nowStr + "','"+ nowDate + "','" + grpid + "')"
    execute( SQL )


def endSample( grpid ) :
    isRunning = getRunningStatus( grpid )
    if not isRunning :
        return
    SQL = "update `status` set `VALUE`='NO' where `KEY`='RUNNING' and `SGROUP`='" + grpid + "'";
    execute(SQL)
    SQL = "update `status` set `VALUE`='' where `KEY`='SESSION' and `SGROUP`='" + grpid + "'";
    execute(SQL)


#print listSessionYears("1")
#print listDays("1","2017")
#print listSessions( "1","20170531")

#print getRunningStatus('1')
