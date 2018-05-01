#!/usr/bin/python2.7
# encoding: utf-8

import os
import sys

d = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, d)

from src.watts import get_watts, get_time_remaining

import logging

# Apple stuff
from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper

UPDATE_INTERVAL = 5

start_time = NSDate.date()

def hide_from_dock():
    """hide icon from dock"""
    #NSApplicationActivationPolicyRegular = 0
    #NSApplicationActivationPolicyAccessory = 1
    NSApplicationActivationPolicyProhibited = 2
    NSApp.setActivationPolicy_(NSApplicationActivationPolicyProhibited)


class DocNetStatDelegate(NSObject):
    def applicationDidFinishLaunching_(self, sender):

        self.statusItem = NSStatusBar.systemStatusBar().statusItemWithLength_(
            NSVariableStatusItemLength)
        self.statusImage = NSImage.alloc()

        self.error = False
        # Icons
        mydir = os.path.dirname(os.path.abspath(__file__))
        self.statusItem.setToolTip_('Watts')
        self.statusItem.setHighlightMode_(TRUE)
        self.statusItem.setEnabled_(TRUE)


        # Menu
        self.error = True
        self.menu = NSMenu.alloc().init()

        # Longterm
        self.longterm_watts = []
        self.longterm_status = NSMenuItem.alloc().init()
        self.longterm_status.setTitle_("init W")
        self.longterm_status.setToolTip_("5 min usage")
        self.longterm_status.setKeyEquivalent_('l')
        self.menu.addItem_(self.longterm_status)

        # Sync and Quit buttons

        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            'Sync...', 'syncall:', '')
        self.menu.addItem_(menuitem)

        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            'Quit', 'terminate:', '')
        self.menu.addItem_(menuitem)
        self.statusItem.setMenu_(self.menu)
        self.timer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(
            start_time, float(UPDATE_INTERVAL), self, 'sync:', None, True)

        # Initialize Ping, Tcp and Udp

        NSRunLoop.currentRunLoop().addTimer_forMode_(self.timer,
                                                     NSDefaultRunLoopMode)
        self.timer.fire()
        NSLog("DockWatts started!")

    def syncall_(self, notification):
        self.sync_(notification)

    def sync_(self, notification):
        watts = get_watts()
        remaining = get_time_remaining()
        if watts is not None:
            self.statusItem.setTitle_(u"%.1f W %s" % (watts, remaining))
            self.longterm_watts.append(watts)

            if len(self.longterm_watts) > 60:
                 self.longterm_watts = self.longterm_watts[1:]

            longterm = sum(self.longterm_watts) / float(len(self.longterm_watts))
            self.longterm_status.setTitle_(u"%.1f W" % longterm)
        else:
            self.statusItem.setTitle_(u"E W")

    def applicationShouldTerminate_(self, notification):
        return 1

if __name__ == "__main__":
    try:
        logging.basicConfig()
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        app = NSApplication.sharedApplication()
        app.hide_(TRUE)
        delegate = DocNetStatDelegate.alloc().init()
        app.setDelegate_(delegate)
        hide_from_dock()
        AppHelper.runEventLoop()
    except KeyboardInterrupt:
        delegate.terminate_()
        AppHelper.stopEventLoop()
        pass
