import logging
from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

import MySQLdb
import string
import os
import DBOperator
import datetime


groupsensorId = "2"

def defLog() :
    return DBOperator.logger

# Show the Sample status
# Also show the proper command button
def result( request ):
    running = DBOperator.getRunningStatus( groupsensorId )
    enabled = DBOperator.getEnableStatus( groupsensorId )
    sesId = ""
    ses = ["",0]
    data = []
    if( running and enabled ) :
        sesId = DBOperator.getCurrentSessionId( groupsensorId )
        data = DBOperator.getRecentRecords( groupsensorId )
        ses = DBOperator.getSessionSelf( sesId, groupsensorId )

    dataStr = []
    if ses != None :
        for d in data:
                tempstr = "" + str( round( float( d[0] ) - float( ses[1])) ) + "s : Weight: " + d[2] + " g Tare(" + d[3] + "g )"
                dataStr.append( tempstr )

    if running :
        showStatus = 'RUN'
    else :
        showStatus = 'STOP'

    if enabled :
        ENABLED = "YES"
    else :
        ENABLED = "NO"

    return render( request = request,template_name='cmds.html',context={ 'status': showStatus , 'enable': ENABLED , 'nowdata' : dataStr, 'nowST' : sesId, 'NUM':'ONE' } )
    #return HttpResponse("The current status is " + status )

# Begin the Sample process
def commandRun( request ):
    log = defLog()
    DT = request.POST['DT']
    log.info( DT )
    if DT:
        os.system("sudo date -s '" + DT + "'")
        log.info( "Set Time successful :" + DT )

    DBOperator.startSample( groupsensorId )
    return render( request = request,template_name='gohome.html' )

# End the Sample Process
def commandStop( request ):
    DBOperator.endSample( groupsensorId )
    return render( request = request,template_name='gohome.html' )

def testCmd( request ):
    #template = loader.get_template('Cmds.html')
    tempContext = {
        'status' : 'STOP',
    }
    return render( request,'cmds.html',tempContext )


def yearList( request ):
    data = DBOperator.listSessionYears( groupsensorId )
    return render( request=request, template_name='yearlist.html', context = { 'years' : data } )


# List the exist days
def dayList( request ):
    YEAR = request.GET["YEAR"]
    data = DBOperator.listDays( groupsensorId, YEAR )
    return render( request=request, template_name='daylist.html', context = { 'days' : data } )

def sessionList( request ):
    theDay = request.GET['DAY']
    theYear=theDay[0:4]
    data = DBOperator.listSessions( groupsensorId, theDay )
    return render( request=request, template_name='sessionlist.html', context = { 'samplesessions' : data , 'day' : theDay, 'year': theYear } )

def download( request ) :
    theSampleTime = request.GET['SES']
    res = HttpResponse( content_type='application/vnd.ms-excel' )
    res['Content-Disposition'] = 'attachment; filename=' + theSampleTime + '.csv'
    res.write("Sample from " + theSampleTime + "\r\n");
    res.write("TimePoint, Sample-Time, Weight(g), Tare(g)\r\n");

    ses = DBOperator.getSessionSelf( theSampleTime, groupsensorId )
    data = DBOperator.getRecord( theSampleTime, groupsensorId )
    ts = float( ses[1] )

    for row in data:
        res.write( round( (float(row[0]) - ts) ))
        res.write( "," )
        res.write( row[12] )
        res.write( "," )
        res.write( row[2] )
        res.write( "," )
        res.write( row[3] )
        res.write( "\r\n" )
    res.flush()
    return res

def show( request ) :
    theSampleTime = request.GET['SES']
    res = HttpResponse( )
    res.write("<html><body><pre>")
    res.write("TimePoint,\tSample-Time,\tWeight(g),\tTare(g)\r\n")

    ses = DBOperator.getSessionSelf(theSampleTime, groupsensorId)
    data = DBOperator.getRecord(theSampleTime, groupsensorId)
    ts = float(ses[1])

    for row in data:
        res.write( round( (float(row[0]) - ts) ))
        res.write(",\t")
        res.write(row[12])
        res.write(",\t")
        res.write(row[2])
        res.write(",\t")
        res.write(row[3])
        res.write("\r\n")

    res.write("</pre></body></html>")
    res.flush()
    return res

def showRaw( request ) :
    theSampleTime = request.GET['SES']
    res = HttpResponse( )

    ses = DBOperator.getSessionSelf(theSampleTime, groupsensorId)
    data = DBOperator.getRecord(theSampleTime, groupsensorId)
    ts = float(ses[1])

    res.write( "var D = [" )
    for row in data:
    	res.write( "[" )
        res.write( round( (float(row[0]) - ts) ) )
        res.write( "," )
        res.write( row[2] )
        res.write( "],\r\n" )
    res.write("];")
    res.flush()
    return res

def showGraph( request ) :
    theSampleTime = request.GET['SES']
    return render( request=request, template_name='SHOWGRAPH.html', context = { 'SES':theSampleTime } )
