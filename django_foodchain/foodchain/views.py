from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from foodchain.models import User
import json
import subprocess
import ast
import datetime

# Create your views here.
# url(r'(?P<fromAddress>)/(?P<toAddress>)/(?P<assetName>)/(?P<qty>)/(?P<assetIds>)$', views.info, name='info')
 
def info(request):

    # step 1 - get the hex
    hex_p = subprocess.Popen(['multichain-cli', 'food2', 'getinfo'],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    out, err = hex_p.communicate()
    big_string = ''.join(out.split('\n\n')[1]).strip()
    resp = json.loads(big_string)


    # step 3 - index into json to get either prev txid or coinbase
    # new_txid = resp['vin'][0]['txid']
    # sender_address = resp['vout'][1]['scriptPubKey']['addresses'][0]
    # print "Prev txid is ", new_txid
    # print "Sender address is ", sender_address
    # prev_owner = User.objects.get(address=sender_address).name
    # print "sender name is ", prev_owner

    # step 4 - look for coinbase

    response = JsonResponse(resp)
    response.__setitem__("Access-Control-Allow-Origin", "*")

    return response

def temp(request, temp, other):
    print temp
    print other
    return HttpResponse('the string was ' + temp + ' and other is ', other)

 
def producer(request,
             fromAddress,
             toAddress,
             assetNameHex,
             assetQtyHex,
             metaDataHex):

    """
    qty, assetName should be dict
    assetIds should be dicts
    unhex them


    but for now just do single assets
    """

    # assetNameList = assetNameHex.decode('hex').split(', ')
    # assetQtyList = assetQtyHex.decode('hex').split(', ')
    # # should be able to many many assets.
    # # that's too hard at this hour
    # asset_dict = {}

    # for i in range(len(assetNameList)):
    #     asset_dict[assetNameList[i]] = assetQtyList[i]

    assetName = str(assetNameHex.decode('hex'))
    assetQty = str(assetQtyHex.decode('hex'))
    # should be able to many many assets.
    # that's too hard at this hour
    asset_dict = {}
    asset_dict[assetName] = assetQty

    metaData = metaDataHex.decode('hex')

    fromAddress = '1MXuLZpXkSCrmKxV8tLwQkFCrGdcKoAz9c6ZAu'
    print 'fromAddress', fromAddress
    print 'toAddress length is ', len(toAddress)
    print 'assetNameHex as str ', str(assetNameHex)
    print 'assetQtyHex', assetQtyHex
    print 'assetQty', assetQty
    print 'metaDataHex', metaDataHex
    print 'asset_dict', str(asset_dict) 
    print 'metaData', metaData

    # step 1 - get the hex
    hex_p = subprocess.Popen(['multichain-cli',
                              'food2', 
                              'sendwithmetadatafrom',
                              fromAddress,
                              toAddress,
                              '"' + str(asset_dict) + '"',
                              metaData],
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)

    out, err = hex_p.communicate()
    print out
    big_string = ''.join(out.split('\n\n')[1]).strip()
    resp = json.loads(big_string)


    # step 3 - index into json to get either prev txid or coinbase
    new_txid = resp['vin'][0]['txid']
    sender_address = resp['vout'][1]['scriptPubKey']['addresses'][0]
    print "Prev txid is ", new_txid
    print "Sender address is ", sender_address
    prev_owner = User.objects.get(address=sender_address).name
    print "sender name is ", prev_owner

    # step 4 - look for coinbase

    response = JsonResponse(resp)
    response.__setitem__("Access-Control-Allow-Origin", "*")

    return response


def txid(request, txid):

    history = []

    # transactions that initially issued assets
    issuetxid =[]
    inits = subprocess.Popen(['multichain-cli', 'food2', 'listassets'],
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)

    out, err = inits.communicate()

    # eval is bad practice, but this is a hackathon
    list_of_inits = eval(''.join(out.split('\n\n')[1]).strip())

    issuetxids = [x['issuetxid'] for x in list_of_inits]

    if txid not in issuetxid:

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

        try:
            sender_address = resp['vout'][1]['scriptPubKey']['addresses'][0]
        except Exception, e:
            print "No more transactions"
        finally:
            print "Sender address is ", sender_address
            # prev_owner = User.objects.get(address=sender_address).name
            # print "sender name is ", prev_owner
            print 'time of transcation is'

            owner_data = {}
            owner_data['owner'] = prev_owner
            owner_data['sender_address  '] = sender_address
            owner_data['timestamp'] = '1341345'

        old_txid=txid
        txid=new_txid
        print '\n\n\n\n\n\n'


    response = JsonResponse(resp)
    response.__setitem__("Access-Control-Allow-Origin", "*")

    return response
