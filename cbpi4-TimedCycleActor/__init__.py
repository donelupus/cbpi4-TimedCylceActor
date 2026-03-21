
# -*- coding: utf-8 -*-
import os
from aiohttp import web
import logging
from unittest.mock import MagicMock, patch
import asyncio
import random
from cbpi.api import *
from cbpi.api.dataclasses import NotificationAction, NotificationType
import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)

@parameters([Property.Actor(label="Actor",  description="Select the actor that will be switched off depending on the GPIO state."),
            Property.Select(label="GPIOstate", options=["High", "Low"],description="Switches the actor on for on_time seconds every cycle_time min."),
            Property.Select(label="on_time", options=["High", "Low"],description="The time in seconds the actor will be switched on every cycle_time min."),
            Property.Select(label="cycle_time", options=["High", "Low"],description="The time in minutes between every on_time period."),
            Property.Select(label="notification", options=["Yes", "No"], description="Will show notification when GPIO switches actor off")])

class GPIODependentActor(CBPiActor):

    async def wait_for_input(self):
        while not self.interrupt:
            await self.cbpi.actor.on(self.base)
            self.state = True
            await asyncio.sleep(self.on_time)
            await self.cbpi.actor.off(self.base)
            self.state = False
            await asyncio.sleep(self.cycle_time * 60 - self.on_time)
            if self.interrupt:
                break

    def on_start(self):
        self.state = False
        self.base = self.props.get("Actor", None)
        try:
            self.name = (self.cbpi.actor.find_by_id(self.base).name)
        except:
            self.name = ""
        self.gpio_upper = self.props.get("GPIO_Upper", None)
        self.gpio_lower = self.props.get("GPIO_Lower", None)
        self.dependency_type = self.props.get("GPIOstate", "High")
        self.notification = self.props.get("notification", "Yes")
        self.interrupt = False
        mode = GPIO.getmode()
        logging.error("GPIODependentActor: on_start GPIO mode: %s", mode)
        if (mode == None):
            GPIO.setmode(GPIO.BCM)
        if self.gpio_upper is not None:
            GPIO.setup(int(self.gpio_upper), GPIO.IN)
        if self.gpio_lower is not None:
            GPIO.setup(int(self.gpio_lower), GPIO.IN)
        else:
            pass

        pass

    async def on(self, power=0):
        logging.error("GPIODependentActor: on")
        self.interrupt = False
        await self.cbpi.actor.on(self.base)
        self._task = asyncio.create_task(self.wait_for_input())
        self.state = True

    async def off(self):
        logging.error("ACTOR %s OFF " % self.base)
        await self.cbpi.actor.off(self.base)
        self.interrupt = True
        self.state = False

    def get_state(self):
        logging.error("GPIODependentActor: get_state: %s", self.state)
        return self.state
    
    async def run(self):
        logging.error("GPIODependentActor: run")
        pass


def setup(cbpi):
    cbpi.plugin.register("GPIO Dependent Actor", GPIODependentActor)
    pass

