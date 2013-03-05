#!/usr/bin/python2.7

import pyfire
import httplib2
import collections
from urllib import urlencode
import config
import time
def incoming(message):
    user = ""
    if message.user:
        user = message.user.name

    if message.is_text():
      if message.body.strip().lower().startswith(config.campfire['name'].lower()):
        values = collections.OrderedDict()
        values['token'] = config.pushover['token']
        values['user'] = config.pushover['user']
        values['message'] = "%s: %s" % (user, message.body)
        http = httplib2.Http()
        data = urlencode(values)
        response, content = http.request("https://api.pushover.net/1/messages.json", "POST", data)


def error(e):
    print("Stream STOPPED due to ERROR: %s" % e)
    print("Press ENTER to continue")

if __name__ == '__main__':

  campfire = pyfire.Campfire(config.campfire['host'], config.campfire['user'], config.campfire['password'], ssl=True)
  rooms = []
  streams = []

  for room_name in config.campfire['rooms']:
    room = campfire.get_room_by_name(room_name)
    room.join()
    rooms.append(room)
    stream = room.get_stream(error_callback=error)
    stream.attach(incoming).start()
    streams.append(stream)

  try:
    while True:
      time.sleep(1)
  finally:
    for stream in streams:
      stream.stop().join()
    for room in rooms:
      room.leave()
