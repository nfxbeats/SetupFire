# SetupFire.py
#
# Author: Nelson F. Fernandez Jr. (aka NFX)
# Created: 2024-July-26
#
# Purpose:
#   Setup the FL STUDIO FIRE by turning off all pads/button and optionally
#   coloring the pads in a specific pattern
#

import mido
import mido.backends.rtmidi
import configparser
import ast

# constants
ManufacturerIDConst = 0x47
DeviceIDBroadCastConst = 0x7F
ProductIDConst = 0x43
MsgIDGetAllButtonStates = 0x40
MsgIDGetPowerOnButtonStates = 0x41
MsgIDSetRGBPadLedState = 0x65
MsgIDSetManufacturingData = 0x79
MsgIDDrawScreenText = 0x08
MsgIDDrawBarControl = 0x09
MsgIDFillOLEDDiplay = 0x0D
MsgIDSendPackedOLEDData = 0x0E
MsgIDSendUnpackedOLEDData = 0x0F
MIDI_BEGINSYSEX = 0xF0
MIDI_ENDSYSEX = 0xF7
FIRE_DEVICE = 'FL STUDIO FIRE'
SYSEX_START = [MIDI_BEGINSYSEX, ManufacturerIDConst, DeviceIDBroadCastConst, ProductIDConst]
SYSEX_END   = [MIDI_ENDSYSEX]

def read_ini(file_path, section, key, default_value=None):
    """
    Reads a value from an .INI file and converts it to a Python literal.
    """
    # Create a ConfigParser instance
    config = configparser.ConfigParser()
    
    # Read the .INI file
    config.read(file_path)
    
    # Get the value as a string
    value_str = config[section][key]
    
    try:
        # Try to evaluate the string to a Python literal
        return ast.literal_eval(value_str)
    except (ValueError, SyntaxError):
        # If literal_eval fails, return the string as is
        return default_value

def scale_rgb_255_to_127(r, g, b):
    """
    Scale RGB values from max 255 to max 127. Fire only supports 0x000000 - 0x7F7F7F.
    """
    scale_factor = 127 / 255
    return int(r * scale_factor), int(g * scale_factor), int(b * scale_factor)

def get_fire_port_name():
    """
    Returns the name of the Fire MIDI port.
    """
    return find_port_by_partial_name(FIRE_DEVICE)

def send_sysex_msg(msgBytes):
    """
    Sends a SysEx message to the Fire.
    """
    msg = []
    msg.extend(SYSEX_START)
    msg.extend(msgBytes)
    msg.extend(SYSEX_END)

    portName = find_port_by_partial_name(FIRE_DEVICE)
    
    outport = mido.open_output(portName)
    outport.send(mido.Message.from_bytes(msg))
    outport.close()
    
    print("SysEx message sent: " + str(msg))

def send_midi_cc(port_name, control, value, channel=0):
    """
    Sends a MIDI CC message to the specified MIDI port.
    
    Parameters:
        port_name (str): The name of the MIDI output port.
        control (int): The control number (0-127).
        value (int): The control value (0-127).
        channel (int): The MIDI channel (0-15). Default is 0.
    
    Returns:
        None
    """
    with mido.open_output(port_name) as outport:
        msg = mido.Message('control_change', channel=channel, control=control, value=value)
        outport.send(msg)
        # print(f"MIDI CC message sent successfully: control={control}, value={value}, channel={channel}")

def find_port_by_partial_name(partial_name, port_type='output'):
    """
    Finds and returns the port name based on a partial match of the name.
    
    Parameters:
        partial_name (str): The partial name to search for.
        port_type (str): The type of port to search ('input' or 'output'). Default is 'output'.
    
    Returns:
        str: The matched port name or None if no match is found.
    """
    if port_type == 'input':
        ports = mido.get_input_names()
    else:
        ports = mido.get_output_names()
    
    for port in ports:
        if partial_name.lower() in port.lower():
            return port
    
    return None

def set_pad_rgb(pad, r, g, b):
    """
    Set the pad color using an RGB tuple.
    
    Args:
        pad (int): The pad identifier.
        r (int): The red value (0-255).
        g (int): The green value (0-255).
        b (int): The blue value (0-255).
    """
    r, g, b = scale_rgb_255_to_127(r, g, b)
    send_sysex_msg([MsgIDSetRGBPadLedState, 0x00, 0x04, pad, r, g, b])

def set_pad_color(pad, color):
    """
    Set the pad color using either an RGB tuple or a hex value in Python form (0xRRGGBB).
    
    Args:
        pad (int): The pad identifier.
        color (tuple or hex): A tuple (r, g, b) with RGB values, a hex value like 0xRRGGBB.
    """
    if isinstance(color, tuple) and len(color) == 3:
        r, g, b = color
    elif isinstance(color, int) and (0x000000 <= color <= 0xFFFFFF):
        r, g, b = (color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF
    else:
        r, g, b = 0,0,0
    
    set_pad_rgb(pad, r, g, b)

if __name__ == "__main__":
    midi_channel = 0 

    # clear the fire 
    send_midi_cc(get_fire_port_name(), 0x7f, 0x00, channel=midi_channel)

    # check if pattern is used and set accordingly
    if( read_ini('SetupFire.ini', 'Fire', 'UsePattern', False) ):
        colors = read_ini('SetupFire.ini', 'Pattern', 'colors', [])
        row1 = read_ini('SetupFire.ini', 'Pattern', 'row1', [])
        row2 = read_ini('SetupFire.ini', 'Pattern', 'row2', [])
        row3 = read_ini('SetupFire.ini', 'Pattern', 'row3', [])
        row4 = read_ini('SetupFire.ini', 'Pattern', 'row4', [])
        allrows = row1 + row2 + row3 + row4

        for pad, coloridx in enumerate(allrows):
            padcolor = colors[coloridx]
            set_pad_color(pad, padcolor)   

