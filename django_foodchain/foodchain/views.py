from django.shortcuts import render
from django.http import JsonResponse
import json
import subprocess

# Create your views here.
def info(request, txid):

    last_trans = "4a47e307138115f6f6ccf29c23f6f7f7d93aa29b6ba322d2bb54516e1602b011"
    txid = last_trans
    print "Final txid is ", txid
    vout = 1
    while vout:

        # step 1 - get the hex
        hex_p = subprocess.Popen(['multichain-cli', 'food2', 'getrawtransaction', txid],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        out, err = hex_p.communicate()
        big_string = ''.join(out.split('\n\n')[1]).strip()
        del hex_p

        # step 2 - decode the hex to get the json
        json_p = subprocess.Popen(['multichain-cli', 'food2', 'decoderawtransaction', big_string],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        
        big_json, err2 = json_p.communicate()
        big_json2 = ''.join(big_json.split('\n\n')[1])
        resp = json.loads(big_json2)
        del json_p

        # step 3 - index into json to get either prev txid or coinbase
        new_txid = resp['vin'][0]['txid']
        sender_address = resp['vout'][1]['scriptPubKey']['addresses'][0]
        print "Prev txid is ", new_txid
        print "Sender address is ", sender_address
        prev_owner = User.objects.get(address=sender_address).name
        print "sender name is ", prev_owner

        # step 4 - look for coinbase

        old_txid=txid
        txid=new_txid
        print '\n\n\n\n\n\n'

    try:
        coinbase = 


    response = JsonResponse(resp)
    response.__setitem__("Access-Control-Allow-Origin", "*")

    return response
