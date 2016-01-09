from django.shortcuts import render
from django.http import JsonResponse
import json
import subprocess

# Create your views here.
def info(request):

    p = subprocess.Popen(['multichain-cli', 'food2', 'getinfo'],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    out, err = p.communicate()

    out2 = ''.join(out.split('\n\n')[1])

    resp = json.loads(out2)

    response = JsonResponse(resp)
    response.__setitem__("Access-Control-Allow-Origin", "*")

    return response
