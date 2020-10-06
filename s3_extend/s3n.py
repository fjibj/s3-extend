import atexit
import signal
import subprocess
import sys
import time

import psutil


# import webbrowser


class S3N:
    """
    This class starts the Banyan server to support the Scratch 3 OneGPIO NewLand Python
    extension for local mode.

    It will start the backplane, NewLand Python gateway and websocket gateway.
    """

    def __init__(self):
        """
        Prepare for launching the Nl extension
        """

        self.proc_bp = None
        self.proc_awg = None
        self.proc_hwg = None

        self.skip_backplane = False


        #print("Only run this script on a Raspberry Pi!")

        # start backplane
        self.proc_bp = self.start_backplane()
        if self.proc_bp:
            print('backplane started')

        else:
            print('backplane start failed - exiting')
            sys.exit(0)

        self.proc_awg = self.start_wsgw()
        if self.proc_awg:
            print('Websocket Gateway started')
        else:
            print('WebSocket Gateway start failed - exiting')
            sys.exit(0)
        
        # start nl gateway
        self.proc_hwg = self.start_nlgw()
        if self.proc_hwg:
            print('Nl Gateway started ')
            print('To exit this program, press Control-c')

        else:
            print('Nl Gateway start failed - exiting')
            sys.exit(0)
        
        atexit.register(self.killall)

        while True:
            try:
                if not self.skip_backplane:
                    if self.proc_bp.poll() is not None:
                        self.proc_bp = None
                        print('backplane exited...')
                        self.killall()
                if self.proc_awg.poll() is not None:
                    self.proc_awg = None
                    print('Websocket Gateway exited...')
                    self.killall()
                if self.proc_hwg.poll() is not None:
                    self.proc_hwg = None
                    print('Nl Gateway exited.')
                    self.killall()
                # allow some time between polls
                time.sleep(.4)
            except KeyboardInterrupt:
                self.killall()

    def killall(self):
        """
        Kill all running processes
        """

        # check for missing processes
        if self.proc_bp:
            try:
                if sys.platform.startswith('win32'):
                    subprocess.run(['taskkill', '/F', '/t', '/PID', str(self.proc_bp.pid)],
                                   creationflags=subprocess.CREATE_NEW_PROCESS_GROUP |
                                                 subprocess.CREATE_NO_WINDOW
                                   )
                else:
                    self.proc_bp.kill()
                self.proc_bp = None
            except:
                pass
        if self.proc_awg:
            try:
                if sys.platform.startswith('win32'):
                    subprocess.run(['taskkill', '/F', '/t', '/pid', str(self.proc_awg.pid)],
                                   creationflags=subprocess.CREATE_NEW_PROCESS_GROUP |
                                                 subprocess.CREATE_NO_WINDOW
                                   )
                else:
                    self.proc_awg.kill()
                self.proc_awg = None
            except:
                pass
        if self.proc_hwg:
            try:
                if sys.platform.startswith('win32'):
                    subprocess.run(['taskkill', '/F', '/t', '/PID', str(self.proc_hwg.pid)],
                                   creationflags=subprocess.CREATE_NEW_PROCESS_GROUP |
                                                 subprocess.CREATE_NO_WINDOW
                                   )
                else:
                    self.proc_hwg.kill()
                self.proc_hwg = None
            except:
                pass
        sys.exit(0)

    def start_backplane(self):
        """
        Start the backplane
        """

        # check to see if the backplane is already running
        try:
            for proc in psutil.process_iter(attrs=['pid', 'name']):
                info = proc.info
                if info and info['name'] and 'backplane' in info['name']:
                    self.skip_backplane = True
                    # its running - return its pid
                    return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

        # backplane is not running, so start one
        if sys.platform.startswith('win32'):
            return subprocess.Popen(['backplane'],
                                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP |
                                                  subprocess.CREATE_NO_WINDOW)
        else:
            return subprocess.Popen(['backplane'],
                                    stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                    stdout=subprocess.PIPE)

    def start_wsgw(self):
        """
        Start the websocket gateway
        """
        if sys.platform.startswith('win32'):
            return subprocess.Popen(['wsgw', '-i', '9001'],
                                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                                                  |
                                                  subprocess.CREATE_NO_WINDOW)
        else:
            return subprocess.Popen(['wsgw', '-i', '9001'],
                                    stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                    stdout=subprocess.PIPE)
    
    def start_nlgw(self):
        """
        Start the Nl gateway
        """
        if sys.platform.startswith('win32'):
            return subprocess.Popen(['nlgw'], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP |
                                                             subprocess.CREATE_NO_WINDOW)
        else:
            return subprocess.Popen(['nlgw'], stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                    stdout=subprocess.PIPE)
    

def signal_handler(sig, frame):
    print('Exiting Through Signal Handler')
    raise KeyboardInterrupt


def s3nx():
    """
    Start the extension
    :return:
    """
    S3N()


# listen for SIGINT
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    # replace with name of function you defined above
    s3nx()
