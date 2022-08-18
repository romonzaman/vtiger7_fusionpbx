import logging
import settings
import datetime
from esl_listener import EslListener
from utils import get_header
import pickle
import requests

logger = logging.getLogger(__name__)

def on_event(e):
    
    # print(e.serialize())

    event_name = get_header(e, "Event-Name")
    event_time = "%sZ" % datetime.datetime.utcnow().replace(microsecond=0).isoformat()
    print(event_name)
    # print(event_time)
    host = {}
    host["name"] = get_header(e, "FreeSWITCH-Hostname")
    host["switch"] = get_header(e, "FreeSWITCH-Switchname")
    host["ipv4"] = get_header(e, "FreeSWITCH-IPv4")
    

    event_timestamp = get_header(e, "Event-Date-Timestamp")
    #vtiger_url = get_header(e, "variable_vtiger_url")
    vtiger_url = settings.VTIGER_URL
    variable_vtiger_api_key = settings.VTIGER_APIKEY

    # variable_vtiger_api_key = get_header(e, "variable_vtiger_api_key")
    variable_call_direction = get_header(e, "variable_call_direction")
    variable_direction = get_header(e, "variable_direction")
    
    call_uuid = get_header(e, "variable_vtiger_call_uuid")
    if call_uuid == "":
        call_uuid = get_header(e, "variable_call_uuid")

    requestBody = {}
    requestBody['timestamp'] = event_timestamp
    requestBody['uuid'] = call_uuid
    requestBody['vtigersignature'] = variable_vtiger_api_key
    
    requestBody['direction'] = variable_call_direction
    if variable_call_direction == "":
        requestBody['direction'] = variable_direction
    
    if event_name == "HEARTBEAT":
        # print(e.serialize())
        up_time = get_header(e, "Up-Time")
        print(up_time)
        logger.info(e.getBody())
        
    if event_name == "CHANNEL_PROGRESS":
        print(e.serialize())
        requestBody['callstatus'] = "call_ringing"
        variable_dialed_user = get_header(e, "variable_dialed_user")
        caller_destination_number = get_header(e, "Caller-Destination-Number")
        requestBody['number'] = variable_dialed_user
        if variable_dialed_user == "":
            requestBody['number'] = caller_destination_number

        request_options = {
            'method' : 'POST',
            'contentType' : 'json',
            'followRedirect' : True,
            'timeout' : [3000, 5000],
            'data' : requestBody    
        }
        print("sending %s request to %s"% (event_name, vtiger_url))
        print(requestBody)
        x = requests.post(vtiger_url, json = requestBody, timeout=5)
        print(x.text)
        logger.info(x.text)

    if event_name == "CHANNEL_BRIDGE":
        print(e.serialize())
        
        other_leg_destination_number = get_header(e, "Other-Leg-Destination-Number")
        if other_leg_destination_number == "":
            logger.error("other_leg_destination_number not set")

        requestBody['callstatus'] = "call_answered"
        caller_destination_number = get_header(e, "Other-Leg-Destination-Number")
        requestBody['number'] = caller_destination_number

        request_options = {
            'method' : 'POST',
            'contentType' : 'json',
            'followRedirect' : True,
            'timeout' : [3000, 5000],
            'data' : requestBody
        }
        print("sending %s request to %s"% (event_name, vtiger_url))
        print(requestBody)
        x = requests.post(vtiger_url, json = requestBody, timeout=5)
        print(x.text)
        logger.info(x.text)


###########################
### Main Entrypoint
##
EslListener(
    on_event=on_event,
    event_filters = [
        "HEARTBEAT",
        "CHANNEL_PROGRESS",
        "CHANNEL_BRIDGE",
    ]
).listen_forever()

