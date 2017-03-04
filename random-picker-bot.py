import os
import time
import nmap
from random import randint
from slackclient import SlackClient

# Config
BOT_ID = ""
API_TOKEN = ""

users = {
  'AC:5F:3E:6E:XX:XX' : 'daan',
  'A0:F3:C1:74:XX:XX' : 'Jan',
  '54:60:09:D9:XX:XX' : 'Piet',
}

# constants
AT_BOT = "<@" + BOT_ID + ">"

# instantiate Slack & Twilio clients
slack_client = SlackClient(API_TOKEN)


def handle_command(command, channel):

    nm = nmap.PortScanner()
    nm.scan(hosts='192.168.1.0/24', arguments='-n -sP -PE')

    hosts_list = [(x, nm[x]['addresses']) for x in nm.all_hosts()]
    mac_addresses = []

    # Gather mac addressses
    for host in hosts_list:
      if 'mac' in host[1]:
        mac_addresses.append(host[1]['mac'])

    random = randint(0, len(mac_addresses)-1)
    i = 0
    # Return available users and highlight one name
    if len(mac_addresses) > 0:
        response = ""
        for mac in mac_addresses:
            if (i == random):
                response = response + " *" + users[mac] + "* \n"
            else:
                response = response + users[mac] + "\n"
            i+=1
    else:
      response = "Nobody available"

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Randompickerbot is running")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")