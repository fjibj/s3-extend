#!/usr/bin/env python3

"""
 This is the Python Banyan GUI that communicates with
 the Newland Banyan Gateway

 Copyright (c) 2019 Alan Yorinks All right reserved.

 Python Banyan is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
import argparse
import signal
from subprocess import run
import sys
import time
import logging
import pathlib
import pandas as pd

from python_banyan.gateway_base import GatewayBase

import zmq


# noinspection PyAbstractClass
class NlGateway(GatewayBase):
    """
    This class implements a Banyan gateway for the Raspberry Pi
    GPIO pins. It implements the Common Unified GPIO Message
    Specification.

    If pipgiod is not currently running, it will start it, and
    no backplane ip address was specified, a local backplane
    will be automatically started. If you specify a backplane
    ip address, you will need to start that backplane manually.
    """

    def __init__(self, *subscriber_list, **kwargs):
        """
        Initialize the class for operation
        :param subscriber_list: A list of subscription topics
        :param kwargs: Command line arguments - see bg4rpi()
                       at the bottom of this file.
        """

        # initialize the parent
        super(NlGateway, self).__init__(subscriber_list=subscriber_list,
                                         back_plane_ip_address=kwargs['back_plane_ip_address'],
                                         subscriber_port=kwargs['subscriber_port'],
                                         publisher_port=kwargs['publisher_port'],
                                         process_name=kwargs['process_name']
                                         )
        log=kwargs['log']
        self.log = log
        if self.log:
            fn = str(pathlib.Path.home()) + "/nlgw.log"
            self.logger = logging.getLogger(__name__)
            logging.basicConfig(filename=fn, filemode='w', level=logging.DEBUG)
            sys.excepthook = self.my_handler
        
        self.logger.debug("1111111111111")

        # start the banyan receive loop
        try:
            self.receive_loop()
        except KeyboardInterrupt:
            self.clean_up()
            sys.exit(0)

    def additional_banyan_messages(self, topic, payload):
        """
        This method will pass any messages not handled by this class to the
        specific gateway class. Must be overwritten by the hardware gateway
        class.
        :param topic: message topic
        :param payload: message payload
        """
        if payload['command'] == 'write_txt':
            self.write_txt(None, payload)
    
    def write_txt(self, topic, payload):
        self.logger.info("the txt_path is: {0}".format(payload['txt_path']))
        txt_path = payload['txt_path']
        a = [1,2,3]
        b = [4,5,6]    
        data = pd.DataFrame({'a':a,'b':b})
        df=pd.DataFrame(data)
        df.to_csv(txt_path,index=None,mode='a')
        self.logger.info("33333333333333333")


    def read_sonar(self):
        """
        Read the sonar device and convert value to
        centimeters. The value is then published as a report.
        """
        sonar_time = self.sonar.read()
        distance = sonar_time / 29 / 2
        distance = round(distance, 2)
        payload = {'report': 'sonar_data', 'value': distance}
        self.publish_payload(payload, 'from_nl_gateway')
    
    def init_pins_dictionary(self):
        """
        The pins dictionary is an array of dictionary items that you create
        to describe each GPIO pin. In this dictionary, you can store things
        such as the pins current mode, the last value reported for an input pin
        callback method for an input pin, etc.
        """

        # not used for robohat gateway, but must be initialized.
        self.pins_dictionary = []


    def my_handler(self, xtype, value, tb):
        """
        for logging uncaught exceptions
        :param xtype:
        :param value:
        :param tb:
        :return:
        """
        self.logger.exception("Uncaught exception: {0}".format(str(value)))

def nl_gateway():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", dest="back_plane_ip_address", default="None",
                        help="None or IP address used by Back Plane")
    parser.add_argument("-m", dest="subscriber_list", default="to_nl_gateway", nargs='+',
                        help="Banyan topics space delimited: topic1 topic2 topic3")
    parser.add_argument("-n", dest="process_name", default="NewlandGateway",
                        help="Set process name in banner")
    parser.add_argument("-p", dest="publisher_port", default='43124',
                        help="Publisher IP port")
    parser.add_argument("-s", dest="subscriber_port", default='43125',
                        help="Subscriber IP port")
    parser.add_argument("-t", dest="loop_time", default=".1",
                        help="Event Loop Timer in seconds")
    parser.add_argument("-l", dest="log", default="True",
                        help="Set to True to turn logging on.")

    args = parser.parse_args()
    if args.back_plane_ip_address == 'None':
        args.back_plane_ip_address = None

    log = args.log.lower()
    if log == 'false':
        log = False
    else:
        log = True

    kw_options = {
        'back_plane_ip_address': args.back_plane_ip_address,
        'publisher_port': args.publisher_port,
        'subscriber_port': args.subscriber_port,
        'process_name': args.process_name,
        'loop_time': float(args.loop_time),
        'log': log}
    
    

    try:
        NlGateway(args.subscriber_list, **kw_options)
    except KeyboardInterrupt:
        sys.exit()


def signal_handler(sig, frame):
    print('Exiting Through Signal Handler')
    raise KeyboardInterrupt


# listen for SIGINT
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


if __name__ == '__main__':
    # replace with name of function you defined above
    nl_gateway()
