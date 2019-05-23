import unittest
import time

import ghidra_bridge
from . import bridge # just for default server port - TODO fix that up...

class TestGhidraBridge(unittest.TestCase):
    """ Assumes there's a ghidra bridge server running at DEFAULT_SERVER_PORT """

    def test_interactive_currentAddress(self):
        """ confirm that the current address (and ideally, the other current* vars - TODO) are updated when
            interactive mode is enabled """
        with ghidra_bridge.GhidraBridge(namespace=globals(), connect_to_port=bridge.DEFAULT_SERVER_PORT, interactive_mode=True):            
            # record the current address as an int
            curr_addr = currentAddress.getOffset()
            
            # move the current address
            setCurrentLocation(currentAddress.add(0x10))
            
            # add a little sleep, so there's enough time for the update to make it back to us (interactive_mode isn't meant to be scripted...)
            time.sleep(0.5)
            
            # check the new address has changed (not sure exactly what it's changed to, because instruction alignments might change exactly where we go)
            self.assertNotEqual(curr_addr, currentAddress.getOffset())
      
    def test_interactive_getState_fix(self):
        """ confirm that getState is updated, and doesn't cause a reset to old values when interactive mode is enabled """
        with ghidra_bridge.GhidraBridge(namespace=globals(), connect_to_port=bridge.DEFAULT_SERVER_PORT, interactive_mode=True):
            # record the current address as an int
            curr_addr = currentAddress.getOffset()
            
            # move the current address
            setCurrentLocation(currentAddress.add(0x10))
            
            # call getState
            new_state = getState()
            
            # check the new address has changed (not sure exactly what it's changed to, because instruction alignments might change exactly where we go)
            self.assertNotEqual(curr_addr, currentAddress.getOffset())
            
            # check that the state address matches
            self.assertEqual(currentAddress.getOffset(), new_state.getCurrentAddress().getOffset())
      
    def test_non_interactive_currentAddress(self):
        """ confirm that the current address (and ideally, the other current* vars - TODO) are NOT updated when
            interactive mode is disabled """
        with ghidra_bridge.GhidraBridge(namespace=globals(), connect_to_port=bridge.DEFAULT_SERVER_PORT, interactive_mode=False):
            # get the actual current address
            actual_current_addr = ghidra_bridge.ghidra_bridge.find_ProgramPlugin(state.getTool()).getProgramLocation().getAddress().getOffset()
        
            # record the "current" address as an int
            curr_addr = currentAddress.getOffset()
            
            # move the current address
            setCurrentLocation(currentAddress.add(0x10))
            
            # check the address has changed
            new_actual_current_addr = ghidra_bridge.ghidra_bridge.find_ProgramPlugin(state.getTool()).getProgramLocation().getAddress().getOffset()
            self.assertNotEqual(actual_current_addr, new_actual_current_addr)
            
            # check the currentAddress hasn't changed
            self.assertEqual(curr_addr, currentAddress.getOffset())

    def test_namespace_cleanup(self):
        with ghidra_bridge.GhidraBridge(namespace=globals(), connect_to_port=bridge.DEFAULT_SERVER_PORT):
            self.assertTrue("currentAddress" in globals())
        
        self.assertTrue("currentAddress" not in globals())