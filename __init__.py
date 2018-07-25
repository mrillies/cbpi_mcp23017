# -*- coding: utf-8 -*-
import wiringpi as mcp

from modules import cbpi, app, ActorBase

import json
import os, re, time
from modules.core.props import Property
import traceback

@cbpi.initalizer(order=0)
def initMCP(app):
    mcp.wiringPiSetup()
    #get mcp object if it exisits
    base = cbpi.get_config_parameter("MCP_wiring_Pi_Base", None)
    if base is None:
        base = "500"
        #cbpi.add_config_parameter("MCP_Wiring_Pi_Base", "500", "text", "MCP Base - change is wiring pi libary conflicts occur")
    #app.cache["mcp_base"] = base
    
    mcp.mcp23017Setup(base, "0x20")
        

@cbpi.actor
class MCP23017_TestActor(ActorBase):
    a_busad = Property.Select("Bus Address", options=["0x20","0x21","0x22","0x23","0x24","0x25","0x26","0x27"], description="Bus address setting of MCP based on A0 A1 A2.")
    b_chan = Property.Text("Channel", configurable=True, default_value="100", description="MCP Output channel 0-128")
    #c_pud = Property.Select("Pull up", options=["Off","Up"], default_value = "Off", description="Pull Up or down resisitor")
    f_inv = Property.Select("Invert Output", options=["No","Yes"], description="Invert the output so on means output at 0V")

    #initiasliser called when an actor is created or changed
    def init(self):
        try:
            self.busad = self.a_busad
            self.chan = int(self.b_chan) + 500
            if self.f_inv == "Yes":
                self.on_pol = 0
                self.off_pol = 1
            else:
                self.on_pol = 1
                self.off_pol = 0
         
            #self.check_mcp()
                 
            self.is_on = False
        
            mcp.pinMode(chan,1)
            mcp.digitalWrite(self.chan,self.off_pol)
         
        except Exception as e:
            traceback.print_exc()
            raise

    def on(self, power=100):
        self.is_on = True
        if power != None:
            self.power = power
        mcp.digitalWrite(self.chan,self.on_pol)
        
    def off(self):
        self.is_on = False
        self.mcp.digitalWrite(self.chan,self.off_pol)
        
    def set_power(self, power):
        self.power = power 
        

    @cbpi.action("TODO: Reitialise MCP system")
    def recon(self):
        pass       
