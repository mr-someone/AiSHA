# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import requests
from pprint import pprint
from . import aishabot
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt




class AiSHAView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '2318934571':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)
                    obj = open('test.txt','w+')
                    obj.write(str(message))

                    if 'text' in message['message']:
                        reply = aishabot.AiSHAbot.get_response(message)
                        post_facebook_message(message['sender']['id'], reply, 1)
                    else:
                        post_facebook_message(message['sender']['id'], message['message']['attachments'], 2)
        return HttpResponse()

def post_facebook_message(fbid, recevied_message,mtype):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAX6eV8ysK8BAErZBKZA2JTQ81tXjA8bxFln7hedwhh5TIjfGcK0CkUfduJljoCzjl8mugnBSKCFBKZCZBSnsvBFokSIjRx1affPJOmW2vtBtoj17ixjUo0gSRk0YKVBhwzEwJhJ5eQ5Gquw9TfqhQZCI7JFU5GuqtnJSkt7wowZDZD'
    if mtype == 1:
        response_msg = json.dumps({"recipient":{"id":fbid}, "message": {"text":recevied_message}})
    elif mtype == 2:
        response_msg = json.dumps({"message": {"attachment": {"type": "image", "payload": {"url": "https://scontent.xx.fbcdn.net/v/t39.1997-6/p100x100/851587_369239346556147_162929011_n.png?_nc_ad=z-m&oh=ad2a1e37edd885afb4acd987ad8e33c6&oe=59DEDBB0"}}}, "recipient": {"id": "1346441788784848"}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())