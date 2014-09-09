import pdb
import binascii
import traceback

class KZDecodeException(Exception):
        pass

class KillerZeeDecode:

    # Taken from http://wiki.micasaverde.com/index.php/ZWave_Command_Classes
    COMMAND_CLASS_NO_OPERATION = 0x00 
    COMMAND_CLASS_BASIC = 0x20  
    COMMAND_CLASS_CONTROLLER_REPLICATION = 0x21  
    COMMAND_CLASS_APPLICATION_STATUS = 0x22  
    COMMAND_CLASS_ZIP_SERVICES = 0x23  
    COMMAND_CLASS_ZIP_SERVER = 0x24  
    COMMAND_CLASS_SWITCH_BINARY = 0x25  
    COMMAND_CLASS_SWITCH_MULTILEVEL = 0x26  
    COMMAND_CLASS_SWITCH_MULTILEVEL_V2 = 0x26  
    COMMAND_CLASS_SWITCH_ALL = 0x27  
    COMMAND_CLASS_SWITCH_TOGGLE_BINARY = 0x28  
    COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL = 0x29  
    COMMAND_CLASS_CHIMNEY_FAN = 0x2A  
    COMMAND_CLASS_SCENE_ACTIVATION = 0x2B  
    COMMAND_CLASS_SCENE_ACTUATOR_CONF = 0x2C  
    COMMAND_CLASS_SCENE_CONTROLLER_CONF = 0x2D  
    COMMAND_CLASS_ZIP_CLIENT = 0x2E  
    COMMAND_CLASS_ZIP_ADV_SERVICES = 0x2F  
    COMMAND_CLASS_SENSOR_BINARY = 0x30  
    COMMAND_CLASS_SENSOR_MULTILEVEL = 0x31  
    COMMAND_CLASS_SENSOR_MULTILEVEL_V2 = 0x31  
    COMMAND_CLASS_METER = 0x32  
    COMMAND_CLASS_ZIP_ADV_SERVER = 0x33  
    COMMAND_CLASS_ZIP_ADV_CLIENT = 0x34  
    COMMAND_CLASS_METER_PULSE = 0x35  
    COMMAND_CLASS_METER_TBL_CONFIG = 0x3C  
    COMMAND_CLASS_METER_TBL_MONITOR = 0x3D  
    COMMAND_CLASS_METER_TBL_PUSH = 0x3E  
    COMMAND_CLASS_THERMOSTAT_HEATING = 0x38  
    COMMAND_CLASS_THERMOSTAT_MODE = 0x40  
    COMMAND_CLASS_THERMOSTAT_OPERATING_STATE = 0x42  
    COMMAND_CLASS_THERMOSTAT_SETPOINT = 0x43  
    COMMAND_CLASS_THERMOSTAT_FAN_MODE = 0x44  
    COMMAND_CLASS_THERMOSTAT_FAN_STATE = 0x45  
    COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE = 0x46  
    COMMAND_CLASS_THERMOSTAT_SETBACK = 0x47  
    COMMAND_CLASS_DOOR_LOCK_LOGGING = 0x4C  
    COMMAND_CLASS_SCHEDULE_ENTRY_LOCK = 0x4E  
    COMMAND_CLASS_BASIC_WINDOW_COVERING = 0x50  
    COMMAND_CLASS_MTP_WINDOW_COVERING = 0x51  
    COMMAND_CLASS_MULTI_CHANNEL_V2 = 0x60  
    COMMAND_CLASS_MULTI_INSTANCE = 0x60  
    COMMAND_CLASS_DOOR_LOCK = 0x62  
    COMMAND_CLASS_USER_CODE = 0x63  
    COMMAND_CLASS_CONFIGURATION = 0x70   
    COMMAND_CLASS_CONFIGURATION_V2 = 0x70   
    COMMAND_CLASS_ALARM = 0x71   
    COMMAND_CLASS_MANUFACTURER_SPECIFIC = 0x72   
    COMMAND_CLASS_POWERLEVEL = 0x73   
    COMMAND_CLASS_PROTECTION = 0x75   
    COMMAND_CLASS_PROTECTION_V2 = 0x75   
    COMMAND_CLASS_LOCK = 0x76   
    COMMAND_CLASS_NODE_NAMING = 0x77   
    COMMAND_CLASS_FIRMWARE_UPDATE_MD = 0x7A   
    COMMAND_CLASS_GROUPING_NAME = 0x7B   
    COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE = 0x7C   
    COMMAND_CLASS_REMOTE_ASSOCIATION = 0x7D   
    COMMAND_CLASS_BATTERY = 0x80   
    COMMAND_CLASS_CLOCK = 0x81   
    COMMAND_CLASS_HAIL = 0x82   
    COMMAND_CLASS_WAKE_UP = 0x84   
    COMMAND_CLASS_WAKE_UP_V2 = 0x84   
    COMMAND_CLASS_ASSOCIATION = 0x85   
    COMMAND_CLASS_ASSOCIATION_V2 = 0x85   
    COMMAND_CLASS_VERSION = 0x86   
    COMMAND_CLASS_INDICATOR = 0x87   
    COMMAND_CLASS_PROPRIETARY = 0x88   
    COMMAND_CLASS_LANGUAGE = 0x89   
    COMMAND_CLASS_TIME = 0x8A   
    COMMAND_CLASS_TIME_PARAMETERS = 0x8B   
    COMMAND_CLASS_GEOGRAPHIC_LOCATION = 0x8C   
    COMMAND_CLASS_COMPOSITE = 0x8D   
    COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION_V2 = 0x8E   
    COMMAND_CLASS_MULTI_INSTANCE_ASSOCIATION = 0x8E   
    COMMAND_CLASS_MULTI_CMD = 0x8F   
    COMMAND_CLASS_ENERGY_PRODUCTION = 0x90   
    COMMAND_CLASS_MANUFACTURER_PROPRIETARY = 0x91   
    COMMAND_CLASS_SCREEN_MD = 0x92   
    COMMAND_CLASS_SCREEN_MD_V2 = 0x92   
    COMMAND_CLASS_SCREEN_ATTRIBUTES = 0x93   
    COMMAND_CLASS_SCREEN_ATTRIBUTES_V2 = 0x93   
    COMMAND_CLASS_SIMPLE_AV_CONTROL = 0x94   
    COMMAND_CLASS_AV_CONTENT_DIRECTORY_MD = 0x95   
    COMMAND_CLASS_AV_RENDERER_STATUS = 0x96   
    COMMAND_CLASS_AV_CONTENT_SEARCH_MD = 0x97   
    COMMAND_CLASS_SECURITY = 0x98   
    COMMAND_CLASS_AV_TAGGING_MD = 0x99   
    COMMAND_CLASS_IP_CONFIGURATION = 0x9A   
    COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION = 0x9B   
    COMMAND_CLASS_SENSOR_ALARM = 0x9C   
    COMMAND_CLASS_SILENCE_ALARM = 0x9D   
    COMMAND_CLASS_SENSOR_CONFIGURATION = 0x9E   
    COMMAND_CLASS_MARK = 0xEF   
    COMMAND_CLASS_NON_INTEROPERABLE = 0xF0    
    
    COMMAND_CLASSES = {
        COMMAND_CLASS_NO_OPERATION: "NO_OPERATION",
        COMMAND_CLASS_BASIC: "BASIC",
        COMMAND_CLASS_CONTROLLER_REPLICATION: "CONTROLLER_REPLICATION",
        COMMAND_CLASS_APPLICATION_STATUS: "APPLICATION_STATUS",
        COMMAND_CLASS_ZIP_SERVICES: "ZIP_SERVICES",
        COMMAND_CLASS_ZIP_SERVER: "ZIP_SERVER",
        COMMAND_CLASS_SWITCH_BINARY: "SWITCH_BINARY",
        COMMAND_CLASS_SWITCH_MULTILEVEL: "SWITCH_MULTILEVEL",
        COMMAND_CLASS_SWITCH_MULTILEVEL_V2: "SWITCH_MULTILEVEL_V2",
        COMMAND_CLASS_SWITCH_ALL: "SWITCH_ALL",
        COMMAND_CLASS_SWITCH_TOGGLE_BINARY: "SWITCH_TOGGLE_BINARY",
        COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL: "SWITCH_TOGGLE_MULTILEVEL",
        COMMAND_CLASS_CHIMNEY_FAN: "CHIMNEY_FAN",
        COMMAND_CLASS_SCENE_ACTIVATION: "SCENE_ACTIVATION",
        COMMAND_CLASS_SCENE_ACTUATOR_CONF: "SCENE_ACTUATOR_CONF",
        COMMAND_CLASS_SCENE_CONTROLLER_CONF: "SCENE_CONTROLLER_CONF",
        COMMAND_CLASS_ZIP_CLIENT: "ZIP_CLIENT",
        COMMAND_CLASS_ZIP_ADV_SERVICES: "ZIP_ADV_SERVICES",
        COMMAND_CLASS_SENSOR_BINARY: "SENSOR_BINARY",
        COMMAND_CLASS_SENSOR_MULTILEVEL: "SENSOR_MULTILEVEL",
        COMMAND_CLASS_SENSOR_MULTILEVEL_V2: "SENSOR_MULTILEVEL_V2",
        COMMAND_CLASS_METER: "METER",
        COMMAND_CLASS_ZIP_ADV_SERVER: "ZIP_ADV_SERVER",
        COMMAND_CLASS_ZIP_ADV_CLIENT: "ZIP_ADV_CLIENT",
        COMMAND_CLASS_METER_PULSE: "METER_PULSE",
        COMMAND_CLASS_METER_TBL_CONFIG: "METER_TBL_CONFIG",
        COMMAND_CLASS_METER_TBL_MONITOR: "METER_TBL_MONITOR",
        COMMAND_CLASS_METER_TBL_PUSH: "METER_TBL_PUSH",
        COMMAND_CLASS_THERMOSTAT_HEATING: "THERMOSTAT_HEATING",
        COMMAND_CLASS_THERMOSTAT_MODE: "THERMOSTAT_MODE",
        COMMAND_CLASS_THERMOSTAT_OPERATING_STATE: "THERMOSTAT_OPERATING_STATE",
        COMMAND_CLASS_THERMOSTAT_SETPOINT: "THERMOSTAT_SETPOINT",
        COMMAND_CLASS_THERMOSTAT_FAN_MODE: "THERMOSTAT_FAN_MODE",
        COMMAND_CLASS_THERMOSTAT_FAN_STATE: "THERMOSTAT_FAN_STATE",
        COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE: "CLIMATE_CONTROL_SCHEDULE",
        COMMAND_CLASS_THERMOSTAT_SETBACK: "THERMOSTAT_SETBACK",
        COMMAND_CLASS_DOOR_LOCK_LOGGING: "DOOR_LOCK_LOGGING",
        COMMAND_CLASS_SCHEDULE_ENTRY_LOCK: "SCHEDULE_ENTRY_LOCK",
        COMMAND_CLASS_BASIC_WINDOW_COVERING: "BASIC_WINDOW_COVERING",
        COMMAND_CLASS_MTP_WINDOW_COVERING: "MTP_WINDOW_COVERING",
        COMMAND_CLASS_MULTI_CHANNEL_V2: "MULTI_CHANNEL_V2",
        COMMAND_CLASS_MULTI_INSTANCE: "MULTI_INSTANCE",
        COMMAND_CLASS_DOOR_LOCK: "DOOR_LOCK",
        COMMAND_CLASS_USER_CODE: "USER_CODE",
        COMMAND_CLASS_CONFIGURATION: "CONFIGURATION",
        COMMAND_CLASS_CONFIGURATION_V2: "CONFIGURATION_V2",
        COMMAND_CLASS_ALARM: "ALARM",
        COMMAND_CLASS_MANUFACTURER_SPECIFIC: "MANUFACTURER_SPECIFIC",
        COMMAND_CLASS_POWERLEVEL: "POWERLEVEL",
        COMMAND_CLASS_PROTECTION: "PROTECTION",
        COMMAND_CLASS_PROTECTION_V2: "PROTECTION_V2",
        COMMAND_CLASS_LOCK: "LOCK",
        COMMAND_CLASS_NODE_NAMING: "NODE_NAMING",
        COMMAND_CLASS_FIRMWARE_UPDATE_MD: "FIRMWARE_UPDATE_MD",
        COMMAND_CLASS_GROUPING_NAME: "GROUPING_NAME",
        COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE: "REMOTE_ASSOCIATION_ACTIVATE",
        COMMAND_CLASS_REMOTE_ASSOCIATION: "REMOTE_ASSOCIATION",
        COMMAND_CLASS_BATTERY: "BATTERY",
        COMMAND_CLASS_CLOCK: "CLOCK",
        COMMAND_CLASS_HAIL: "HAIL",
        COMMAND_CLASS_WAKE_UP: "WAKE_UP",
        COMMAND_CLASS_WAKE_UP_V2: "WAKE_UP_V2",
        COMMAND_CLASS_ASSOCIATION: "ASSOCIATION",
        COMMAND_CLASS_ASSOCIATION_V2: "ASSOCIATION_V2",
        COMMAND_CLASS_VERSION: "VERSION",
        COMMAND_CLASS_INDICATOR: "INDICATOR",
        COMMAND_CLASS_PROPRIETARY: "PROPRIETARY",
        COMMAND_CLASS_LANGUAGE: "LANGUAGE",
        COMMAND_CLASS_TIME: "TIME",
        COMMAND_CLASS_TIME_PARAMETERS: "TIME_PARAMETERS",
        COMMAND_CLASS_GEOGRAPHIC_LOCATION: "GEOGRAPHIC_LOCATION",
        COMMAND_CLASS_COMPOSITE: "COMPOSITE",
        COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION_V2: "MULTI_CHANNEL_ASSOCIATION_V2",
        COMMAND_CLASS_MULTI_INSTANCE_ASSOCIATION: "MULTI_INSTANCE_ASSOCIATION",
        COMMAND_CLASS_MULTI_CMD: "MULTI_CMD",
        COMMAND_CLASS_ENERGY_PRODUCTION: "ENERGY_PRODUCTION",
        COMMAND_CLASS_MANUFACTURER_PROPRIETARY: "MANUFACTURER_PROPRIETARY",
        COMMAND_CLASS_SCREEN_MD: "SCREEN_MD",
        COMMAND_CLASS_SCREEN_MD_V2: "SCREEN_MD_V2",
        COMMAND_CLASS_SCREEN_ATTRIBUTES: "SCREEN_ATTRIBUTES",
        COMMAND_CLASS_SCREEN_ATTRIBUTES_V2: "SCREEN_ATTRIBUTES_V2",
        COMMAND_CLASS_SIMPLE_AV_CONTROL: "SIMPLE_AV_CONTROL",
        COMMAND_CLASS_AV_CONTENT_DIRECTORY_MD: "AV_CONTENT_DIRECTORY_MD",
        COMMAND_CLASS_AV_RENDERER_STATUS: "AV_RENDERER_STATUS",
        COMMAND_CLASS_AV_CONTENT_SEARCH_MD: "AV_CONTENT_SEARCH_MD",
        COMMAND_CLASS_SECURITY: "SECURITY",
        COMMAND_CLASS_AV_TAGGING_MD: "AV_TAGGING_MD",
        COMMAND_CLASS_IP_CONFIGURATION: "IP_CONFIGURATION",
        COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION: "ASSOCIATION_COMMAND_CONFIGURATION",
        COMMAND_CLASS_SENSOR_ALARM: "SENSOR_ALARM",
        COMMAND_CLASS_SILENCE_ALARM: "SILENCE_ALARM",
        COMMAND_CLASS_SENSOR_CONFIGURATION: "SENSOR_CONFIGURATION",
        COMMAND_CLASS_MARK: "MARK",
        COMMAND_CLASS_NON_INTEROPERABLE: "NON_INTEROPERABLE"
    }

    THERMOSTAT_MODE_OFF = "\x00"
    THERMOSTAT_MODE_HEAT = "\x01"
    THERMOSTAT_MODE_COOL = "\x02"
    THERMOSTAT_MODE_AUTO = "\x03"

    def get_thermostat_mode(self, payload):
        if len(payload) >= 3 and ord(payload[0]) == self.COMMAND_CLASS_THERMOSTAT_MODE:
            mode=payload[2]
            if (mode == self.THERMOSTAT_MODE_OFF):
                return "Off"
            elif (mode == self.THERMOSTAT_MODE_COOL):
                return "Cooling"
            elif (mode == self.THERMOSTAT_MODE_HEAT):
                return "Heating"
            elif (mode == self.THERMOSTAT_MODE_AUTO):
                return "Automatic"
            else:
                return "Unknown mode (%d)"%mode
        return ''
    
    # Returns a string describing the payload attributes
    def payloaddecode(self, payload):
        if len(payload) == 0:
            return ""
    
        commandclass = ord(payload[0])
        try:
            desc = self.COMMAND_CLASSES[commandclass];
        except KeyError:
            desc = "COMMAND_CLASS_UNKNOWN_0X" + payload[0].encode('hex')
    
        if len(payload) == 1:
            return desc
    
        # Processing payload data that we know a little more about
        commandclasscmd = ord(payload[1])
        payloadmsg = ""
    
        # Wow.  This is hideous.
        # According to open-zwave, the byte that follows the command class is the
        # command class command.  In many cases, the command class command is
        # 1=Set, 2=Get, 3=Report -- but not always.  We end up having to decode the
        # command class command for each command class.
        if commandclass == self.COMMAND_CLASS_SWITCH_ALL:
            if commandclasscmd == 1:
                desc += " Set"
            elif commandclasscmd == 2:
                desc += " Get"
            elif commandclasscmd == 3:
                desc += " Report"
            elif commandclasscmd == 4:
                desc += " On"
            elif commandclasscmd == 5:
                desc += " Off"
            else:
                desc += " InvalidSwitchAllCmd"
        elif commandclass == self.COMMAND_CLASS_CLOCK:
            if commandclasscmd == 4:
                desc += " Set"
            elif commandclasscmd == 5:
                desc += " Get"
            elif commandclasscmd == 6:
                desc += " Report"
            else:
                desc += " InvalidClockCmd"
        elif commandclass == self.COMMAND_CLASS_THERMOSTAT_MODE:
            if commandclasscmd == 1:
                desc += " Set"
                if len(payload) >= 3:
                    desc += " Mode:" + self.get_thermostat_mode(payload)
            elif commandclasscmd == 2:
                desc += " Get"
            elif commandclasscmd == 3:
                desc += " Report"
                if len(payload) >= 3:
                    desc += " Mode:" + self.get_thermostat_mode(payload)
            elif commandclasscmd == 4:
                desc += " SupportedGet"
            elif commandclasscmd == 5:
                desc += " SupportedReport"
            else:
                desc += " InvalidThermostatModeCmd"
        elif commandclass == self.COMMAND_CLASS_THERMOSTAT_SETPOINT:
            if commandclasscmd == 1:
                desc += " Set"
                if len(payload) >= 4:
                    desc += " (Temp %d F)"%ord(payload[4])
            elif commandclasscmd == 2:
                desc += " Get"
            elif commandclasscmd == 3:
                desc += " Report"
                if len(payload) >= 4:
                    desc += " (Temp %d F)"%ord(payload[4])
            elif commandclasscmd == 4:
                desc += " SupportedGet"
            elif commandclasscmd == 5:
                desc += " SupportedReport"
            else:
                desc += " InvalidThermostatSetPointCmd"

        elif commandclass == self.COMMAND_CLASS_THERMOSTAT_FAN_MODE:
            if commandclasscmd == 1:
                desc += " Set"
                if len(payload) >= 3:
                    if payload[1] == "\x00":
                        desc += " (Off)"
                    else:
                        desc += " (On)"
            elif commandclasscmd == 2:
                desc += " Get"
            elif commandclasscmd == 3:
                desc += " Report"
                if len(payload) >= 3:
                    if payload[1] == "\x00":
                        desc += " (Off)"
                    else:
                        desc += " (On)"
            elif commandclasscmd == 4:
                desc += " SupportedGet"
            elif commandclasscmd == 5:
                desc += " SupportedReport"
            else:
                desc += " InvalidThermostatFanModeCmd"

        elif commandclass == self.COMMAND_CLASS_THERMOSTAT_OPERATING_STATE:
            if commandclasscmd == 1:
                desc += " Set"
            elif commandclasscmd == 2:
                desc += " Get"
            elif commandclasscmd == 3:
                desc += " Report"
            elif commandclasscmd == 4:
                desc += " SupportedGet"
            elif commandclasscmd == 5:
                desc += " SupportedReport"
            else:
                desc += " InvalidThermostatOperatingStateCmd"

        elif commandclass == self.COMMAND_CLASS_BASIC:
            if commandclasscmd == 1:
                desc += " Set"
            elif commandclasscmd == 2:
                desc += " Get"
            elif commandclasscmd == 3:
                desc += " Report"
            else:
                desc += " odeCmd"
            if len(payload) > 2 and commandclass == 1:
                eventcmd = ord(payload[2])
                if (eventcmd == 0):
                    desc += " Off"
                else:
                    desc += " On"
        elif commandclass == self.COMMAND_CLASS_SWITCH_MULTILEVEL_V2:
            if commandclasscmd == 1:
                desc += " Set"
            elif commandclasscmd == 2:
                desc += " Get"
            elif commandclasscmd == 3:
                desc += " Report"
            else:
                desc += " InvalidSwitchMultiLevelModeCmd"
            if len(payload) > 2 and commandclass == 1:
                eventcmd = ord(payload[2])
                if (eventcmd == 0):
                    desc += " Off"
                else:
                    desc += " On"
    
        return desc
    

    def decode_r1(self, packet):
        descline = ''
        try:

            # First make sure it's not a beam frame
            if packet[0] == "\x55":
                return "Beam frame, DestID:%2x"%ord(packet[1])

            homeid=packet[0:4]
            source=packet[4]
            fc=packet[5:7]

            # Check for multicast frame, changes packet format
            if (ord(fc[0]) & 0x0F) == 2:
                mcastpacket=True
            else:
                mcastpacket=False

            plen=(ord(packet[7]))
            dest=packet[8]

            if not mcastpacket:
                payload=packet[9:-1]
            else:
                mcastdest=ord(packet[9])
                mcastaddroffset = (mcastdest & 0b11100000) >> 5
                mcastnummaskbytes = (mcastdest & 0b00011111)
                payload=packet[9+mcastnummaskbytes:-1]

            fcdesc=""
            fcint = int(binascii.hexlify(packet[5:7]), 16)
            fctype = (fcint & 0b0000111100000000) >> 8
            if fctype == 1:
                fcdesc += "Singlecast "
            elif fctype == 2:
                fcdesc += "Multicast "
            elif fctype == 3:
                fcdesc += "ACK "
            elif fctype == 8:
                fcdesc += "Routed "
            else:
                fcdesc += "Reserved  "
            if fcint & 0b1000000000000000:
                fcdesc += "Routed "
            if fcint & 0b0100000000000000:
                fcdesc += "ACK-Reqd "
            if fcint & 0b0010000000000000:
                fcdesc += "Low-Power "
            if fcint & 0b0001000000000000:
                fcdesc += "Speed-Modified "
            if fcint & 0b0000000010000000:
                fcdesc += "Rsvd-Bit1 "
            if (fcint & 0b0000000011000000) != 0:
                fcdesc += "Beam Wakeup "
            if fcint & 0b0000000000010000:
                fcdesc += "Rsvd-Bit2 "
            fcseqnum = fcint & 0b0000000000001111
            fcdesc += "Seq#%d"%fcseqnum

            descline = "HomeID:"
            descline += homeid.encode('hex')
            descline += " SourceID:"
            descline += source.encode('hex')
            descline += " DestID:"
            descline += dest.encode('hex')
            descline += " FC:(" + fcdesc
            descline += ") Len:"
            descline += "%d"%plen + " "

            if mcastpacket:
                descline += "Multicast:%02x "%mcastdest
                descline += "(Offset %d, Mask Byte Count %d) "%(mcastaddroffset, mcastnummaskbytes)

            descline += self.payloaddecode(payload)
        except (TypeError,IndexError) as e:
            print traceback.format_exc()
            return descline + " -- bad packet, skipping"

        return descline


    def decode_r2(self, packet):
        return self.decode_r1(packet)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
