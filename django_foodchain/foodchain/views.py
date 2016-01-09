from django.shortcuts import render
from django.http import JsonResponse
import json
import subprocess
import ast

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

    assetNameList = assetNameHex.decode('hex').split(', ')
    assetQtyList = assetQtyHex.decode('hex').split(', ')
    # should be able to many many assets.
    # that's too hard at this hour
    asset_dict = {}

    for i in range(len(assetNameList)):
        asset_dict[assetNameList[i]] = assetQtyList[i]

    metaData = metaDataHex.decode('hex')

    # step 1 - get the hex
    hex_p = subprocess.Popen(['multichain-cli',
                              'food2', 
                              'sendwithmetadatafrom',
                              fromAddress,
                              toAddress,
                              str(asset_dict),
                              metaData],
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


