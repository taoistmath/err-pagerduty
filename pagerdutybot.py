#!/usr/bin/python
import requests
import json
from errbot import botcmd, BotPlugin
from config import PAGERDUTY_TOKEN

__author__ = 'taoistmath'

class JenkinsBot(BotPlugin):

    def pagerduty_oncall(self):
        self.oncall = requests.get("https://dnb-atc.pagerduty.com/api/v1/users/on_call", headers={'Authorization': 'Token token='+PAGERDUTY_TOKEN})

    def pagerduty_contact(self, user_url):
        print "https://dnb-atc.pagerduty.com/api/v1" + user_url + "/contact_methods"
        self.contact = requests.get("https://dnb-atc.pagerduty.com/api/v1" + user_url + "/contact_methods", headers={'Authorization': 'Token token=YTeCYnnjYucByhXzzxqX'})

    @botcmd
    def oncall(self, mess, args):
        """List who is On-Call for Malibu DevOps"""
        self.pagerduty_oncall()

        mydict = json.loads(self.oncall.text)

        primary = self.get_primary_contact(mydict)
        secondary = self.get_secondary_contact(mydict)

        return primary + '\n' + secondary 

    def get_primary_contact(self, mydict):
        count = 0
        while (count < len(mydict)+1):
            if mydict['users'][count]['on_call'][0]['escalation_policy']['name'] == 'Malibu DevOps' and mydict['users'][count]['on_call'][0]['level'] == 1:
                phone_number = self.get_phone_number(mydict['users'][count]['user_url'])
                return 'Primary Contact: ' + mydict['users'][count]['name'] + ' ' + phone_number
            count = count + 1

    def get_secondary_contact(self, mydict):
        count = 0
        while (count < len(mydict)+1):
            if mydict['users'][count]['on_call'][0]['escalation_policy']['name'] == 'Malibu DevOps' and mydict['users'][count]['on_call'][0]['level'] == 2:
                phone_number = self.get_phone_number(mydict['users'][count]['user_url'])
                return 'Secondary Contact: ' + mydict['users'][count]['name'] + ' ' + phone_number
            count = count + 1   

    def get_phone_number(self, user_url):
        self.pagerduty_contact(user_url)
        mydict = json.loads(self.contact.text)
        phone =  mydict['contact_methods'][1]['phone_number']
        return "+1(" + phone[0:3] + ")" + phone[3:6] + "-" + phone[6:10]
        