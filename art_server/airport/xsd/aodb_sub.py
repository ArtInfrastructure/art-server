#!/usr/bin/env python

#
# Generated Mon Jun  8 10:52:37 2009 by generateDS.py.
#

import sys
from string import lower as str_lower
from xml.dom import minidom
from xml.sax import handler, make_parser

import ??? as supermod

#
# Globals
#

ExternalEncoding = 'ascii'

#
# Data representation classes
#

class EnvelopeSub(supermod.Envelope):
    def __init__(self, Header=None, Body=None):
        supermod.Envelope.__init__(self, Header, Body)
supermod.Envelope.subclass = EnvelopeSub
# end class EnvelopeSub


class HeaderSub(supermod.Header):
    def __init__(self, MessageSentDateTime=None, MessageSequenceNumber=None, RequestSequenceNumber=None, RequestSource=None, MessageNumber=None, TotalMessages=None, MessageFunction=None, MessageType=None, RequestType=None, SenderID=None):
        supermod.Header.__init__(self, MessageSentDateTime, MessageSequenceNumber, RequestSequenceNumber, RequestSource, MessageNumber, TotalMessages, MessageFunction, MessageType, RequestType, SenderID)
supermod.Header.subclass = HeaderSub
# end class HeaderSub


class FlightLegTypeSub(supermod.FlightLegType):
    def __init__(self, ModTime=None, FromTime=None, ToTime=None, RollingTimeWindow=None, InOutbound=None, Carrier=None, FlightNumber=None):
        supermod.FlightLegType.__init__(self, ModTime, FromTime, ToTime, RollingTimeWindow, InOutbound, Carrier, FlightNumber)
supermod.FlightLegType.subclass = FlightLegTypeSub
# end class FlightLegTypeSub


class ResAllocationSub(supermod.ResAllocation):
    def __init__(self, ModTime=None):
        supermod.ResAllocation.__init__(self, ModTime)
supermod.ResAllocation.subclass = ResAllocationSub
# end class ResAllocationSub


class BodySub(supermod.Body):
    def __init__(self, FlightLeg=None, ResourceAllocation=None, RefData=None, Fault=None):
        supermod.Body.__init__(self, FlightLeg, ResourceAllocation, RefData, Fault)
supermod.Body.subclass = BodySub
# end class BodySub


class DisplayTextSub(supermod.DisplayText):
    def __init__(self, Code=None, IdSeq=None, Text=None):
        supermod.DisplayText.__init__(self, Code, IdSeq, Text)
supermod.DisplayText.subclass = DisplayTextSub
# end class DisplayTextSub


class DisplayObjectSub(supermod.DisplayObject):
    def __init__(self, Name=None, IdSeq=None, Description=None):
        supermod.DisplayObject.__init__(self, Name, IdSeq, Description)
supermod.DisplayObject.subclass = DisplayObjectSub
# end class DisplayObjectSub


class PublicStatusRemarkSub(supermod.PublicStatusRemark):
    def __init__(self, RemarkCode=None, RemarkText=None):
        supermod.PublicStatusRemark.__init__(self, RemarkCode, RemarkText)
supermod.PublicStatusRemark.subclass = PublicStatusRemarkSub
# end class PublicStatusRemarkSub


class StaffStatusRemarkSub(supermod.StaffStatusRemark):
    def __init__(self, RemarkCode=None, RemarkText=None):
        supermod.StaffStatusRemark.__init__(self, RemarkCode, RemarkText)
supermod.StaffStatusRemark.subclass = StaffStatusRemarkSub
# end class StaffStatusRemarkSub


class FaultSub(supermod.Fault):
    def __init__(self, FaultCode=None, FaultString=None, FaultActor=None):
        supermod.Fault.__init__(self, FaultCode, FaultString, FaultActor)
supermod.Fault.subclass = FaultSub
# end class FaultSub


class AircraftIdentifierSub(supermod.AircraftIdentifier):
    def __init__(self, Identifier=None, IdentifierName=None):
        supermod.AircraftIdentifier.__init__(self, Identifier, IdentifierName)
supermod.AircraftIdentifier.subclass = AircraftIdentifierSub
# end class AircraftIdentifierSub


class AirportZoneSub(supermod.AirportZone):
    def __init__(self, ZoneType=None, ZoneName=None):
        supermod.AirportZone.__init__(self, ZoneType, ZoneName)
supermod.AirportZone.subclass = AirportZoneSub
# end class AirportZoneSub


class AircraftWeightSub(supermod.AircraftWeight):
    def __init__(self, WeightClass=None, AircraftWeight=None):
        supermod.AircraftWeight.__init__(self, WeightClass, AircraftWeight)
supermod.AircraftWeight.subclass = AircraftWeightSub
# end class AircraftWeightSub


class BagClaimInfoSub(supermod.BagClaimInfo):
    def __init__(self, BagClaimHall=None, BagClaimName=None, BagClaimStatus=None, SchedBegin=None, SchedEnd=None, ActualBegin=None, ActualEnd=None, EndTime=None, SupplementalTime=None):
        supermod.BagClaimInfo.__init__(self, BagClaimHall, BagClaimName, BagClaimStatus, SchedBegin, SchedEnd, ActualBegin, ActualEnd, EndTime, SupplementalTime)
supermod.BagClaimInfo.subclass = BagClaimInfoSub
# end class BagClaimInfoSub


class GateInfoSub(supermod.GateInfo):
    def __init__(self, GateName=None, DisplayText=None, DisplayObject=None, GateStatus=None, SchedBegin=None, SchedEnd=None, ActualBegin=None, ActualEnd=None, SupplementalTime=None):
        supermod.GateInfo.__init__(self, GateName, DisplayText, DisplayObject, GateStatus, SchedBegin, SchedEnd, ActualBegin, ActualEnd, SupplementalTime)
supermod.GateInfo.subclass = GateInfoSub
# end class GateInfoSub


class BaggageMakeUpBeltInfoSub(supermod.BaggageMakeUpBeltInfo):
    def __init__(self, BaggageMakeUpBelt=None, SchedBegin=None, SchedEnd=None, ActualBegin=None, ActualEnd=None, SupplementalTime=None):
        supermod.BaggageMakeUpBeltInfo.__init__(self, BaggageMakeUpBelt, SchedBegin, SchedEnd, ActualBegin, ActualEnd, SupplementalTime)
supermod.BaggageMakeUpBeltInfo.subclass = BaggageMakeUpBeltInfoSub
# end class BaggageMakeUpBeltInfoSub


class StandInfoSub(supermod.StandInfo):
    def __init__(self, AircraftStand=None, SchedBegin=None, SchedEnd=None, ActualBegin=None, ActualEnd=None, SupplementalTime=None):
        supermod.StandInfo.__init__(self, AircraftStand, SchedBegin, SchedEnd, ActualBegin, ActualEnd, SupplementalTime)
supermod.StandInfo.subclass = StandInfoSub
# end class StandInfoSub


class CounterAllocationSub(supermod.CounterAllocation):
    def __init__(self, FlightID=None, Carrier=None, Counter=None):
        supermod.CounterAllocation.__init__(self, FlightID, Carrier, Counter)
supermod.CounterAllocation.subclass = CounterAllocationSub
# end class CounterAllocationSub


class CounterSub(supermod.Counter):
    def __init__(self, elementIndex=None, CounterName=None, ServiceClass=None, DisplayText=None, DisplayObject=None, CheckInStatus=None, SchedBegin=None, SchedEnd=None, ActualBegin=None, ActualEnd=None, SupplementalTime=None):
        supermod.Counter.__init__(self, elementIndex, CounterName, ServiceClass, DisplayText, DisplayObject, CheckInStatus, SchedBegin, SchedEnd, ActualBegin, ActualEnd, SupplementalTime)
supermod.Counter.subclass = CounterSub
# end class CounterSub


class CargoSub(supermod.Cargo):
    def __init__(self, ExpressCargo=None, MailCargo=None, TotalCargo=None, UnusualCargo=None):
        supermod.Cargo.__init__(self, ExpressCargo, MailCargo, TotalCargo, UnusualCargo)
supermod.Cargo.subclass = CargoSub
# end class CargoSub


class CargoDataSub(supermod.CargoData):
    def __init__(self, Pieces=None, CargoWeight=None):
        supermod.CargoData.__init__(self, Pieces, CargoWeight)
supermod.CargoData.subclass = CargoDataSub
# end class CargoDataSub


class CheckInRangeSub(supermod.CheckInRange):
    def __init__(self, CheckInDeskFunction=None):
        supermod.CheckInRange.__init__(self, CheckInDeskFunction)
supermod.CheckInRange.subclass = CheckInRangeSub
# end class CheckInRangeSub


class CodeshareDataSub(supermod.CodeshareData):
    def __init__(self, elementIndex=None, Carrier=None, FlightNumber=None, Suffix=None):
        supermod.CodeshareData.__init__(self, elementIndex, Carrier, FlightNumber, Suffix)
supermod.CodeshareData.subclass = CodeshareDataSub
# end class CodeshareDataSub


class CrewDataSub(supermod.CrewData):
    def __init__(self, FlightAttendantCrewCount=None, FlightDeckCrewCount=None, TotalCrewCount=None):
        supermod.CrewData.__init__(self, FlightAttendantCrewCount, FlightDeckCrewCount, TotalCrewCount)
supermod.CrewData.subclass = CrewDataSub
# end class CrewDataSub


class FlightIDSub(supermod.FlightID):
    def __init__(self, Carrier=None, FlightNumber=None, Suffix=None, ScheduledTime=None, InOutbound=None, OriginDestinationAirport=None):
        supermod.FlightID.__init__(self, Carrier, FlightNumber, Suffix, ScheduledTime, InOutbound, OriginDestinationAirport)
supermod.FlightID.subclass = FlightIDSub
# end class FlightIDSub


class ResourceAllocationSub(supermod.ResourceAllocation):
    def __init__(self, CounterAllocation=None):
        supermod.ResourceAllocation.__init__(self, CounterAllocation)
supermod.ResourceAllocation.subclass = ResourceAllocationSub
# end class ResourceAllocationSub


class FlightLegSub(supermod.FlightLeg):
    def __init__(self, activeFlag=None, FlightID=None, ACRegistration=None, ACSubTypeCode=None, ACTypeCode=None, FleetNumber=None, PublicGate=None, PublicStand=None, BagClaim=None, GateInfo=None, StandInfo=None, Runway=None, SecurityCheck=None, Terminal=None, LinkFlight=None, BagMakeUpBelt=None, GateRemark=None, PublicStatusRemark=None, StaffStatusRemark=None, SupplementalRemark=None, PublicComment=None, OperationalComment=None, TransitFlag=None, Stopover=None, Decision=None, Estimated=None, GateOpen=None, GateClose=None, PublicEstimated=None, PushBack=None, WheelsUp=None, Touchdown=None, AtGate=None, Codeshare=None, InFlightService=None, ServicyTypeCode=None, FlightStatus=None, BagCount=None, OvernightIndicator=None, BestKnowTime=None, Irregularity=None):
        supermod.FlightLeg.__init__(self, activeFlag, FlightID, ACRegistration, ACSubTypeCode, ACTypeCode, FleetNumber, PublicGate, PublicStand, BagClaim, GateInfo, StandInfo, Runway, SecurityCheck, Terminal, LinkFlight, BagMakeUpBelt, GateRemark, PublicStatusRemark, StaffStatusRemark, SupplementalRemark, PublicComment, OperationalComment, TransitFlag, Stopover, Decision, Estimated, GateOpen, GateClose, PublicEstimated, PushBack, WheelsUp, Touchdown, AtGate, Codeshare, InFlightService, ServicyTypeCode, FlightStatus, BagCount, OvernightIndicator, BestKnowTime, Irregularity)
supermod.FlightLeg.subclass = FlightLegSub
# end class FlightLegSub


class BagClaimSub(supermod.BagClaim):
    def __init__(self, BagClaimHall=None, BagClaimName=None, BagClaimStatus=None, SchedBegin=None, SchedEnd=None, ActualBegin=None, ActualEnd=None, EndTime=None, SupplementalTime=None, elementIndex=None):
        supermod.BagClaim.__init__(self, BagClaimHall, BagClaimName, BagClaimStatus, SchedBegin, SchedEnd, ActualBegin, ActualEnd, EndTime, SupplementalTime, elementIndex)
supermod.BagClaim.subclass = BagClaimSub
# end class BagClaimSub


class BagMakeUpBeltSub(supermod.BagMakeUpBelt):
    def __init__(self, BaggageMakeUpBelt=None, SchedBegin=None, SchedEnd=None, ActualBegin=None, ActualEnd=None, SupplementalTime=None, elementIndex=None):
        supermod.BagMakeUpBelt.__init__(self, BaggageMakeUpBelt, SchedBegin, SchedEnd, ActualBegin, ActualEnd, SupplementalTime, elementIndex)
supermod.BagMakeUpBelt.subclass = BagMakeUpBeltSub
# end class BagMakeUpBeltSub


class InFlightServiceSub(supermod.InFlightService):
    def __init__(self, Cabin=None, Service=None):
        supermod.InFlightService.__init__(self, Cabin, Service)
supermod.InFlightService.subclass = InFlightServiceSub
# end class InFlightServiceSub


class ServiceSub(supermod.Service):
    def __init__(self, elementIndex=None, valueOf_=''):
        supermod.Service.__init__(self, elementIndex)
supermod.Service.subclass = ServiceSub
# end class ServiceSub


class FlightLegKeySub(supermod.FlightLegKey):
    def __init__(self, Carrier=None, FlightNumber=None, Suffix=None, ScheduledDateTime=None, InOutbound=None, OriginDestinationAirportCode=None):
        supermod.FlightLegKey.__init__(self, Carrier, FlightNumber, Suffix, ScheduledDateTime, InOutbound, OriginDestinationAirportCode)
supermod.FlightLegKey.subclass = FlightLegKeySub
# end class FlightLegKeySub


class FlightLinkDataSub(supermod.FlightLinkData):
    def __init__(self, FlightID=None):
        supermod.FlightLinkData.__init__(self, FlightID)
supermod.FlightLinkData.subclass = FlightLinkDataSub
# end class FlightLinkDataSub


class IrregularitySub(supermod.Irregularity):
    def __init__(self, IATAIrregularityCode=None, IrregularityText=None):
        supermod.Irregularity.__init__(self, IATAIrregularityCode, IrregularityText)
supermod.Irregularity.subclass = IrregularitySub
# end class IrregularitySub


class NoiseClassificationSub(supermod.NoiseClassification):
    def __init__(self, NoiseValue=None, NoiseCategoryUnits=None):
        supermod.NoiseClassification.__init__(self, NoiseValue, NoiseCategoryUnits)
supermod.NoiseClassification.subclass = NoiseClassificationSub
# end class NoiseClassificationSub


class SeatingCapacitySub(supermod.SeatingCapacity):
    def __init__(self, CapacityData=None):
        supermod.SeatingCapacity.__init__(self, CapacityData)
supermod.SeatingCapacity.subclass = SeatingCapacitySub
# end class SeatingCapacitySub


class CapacityDataSub(supermod.CapacityData):
    def __init__(self, Cabin=None, SeatCount=None):
        supermod.CapacityData.__init__(self, Cabin, SeatCount)
supermod.CapacityData.subclass = CapacityDataSub
# end class CapacityDataSub


class SupplementaryPassengerDataSub(supermod.SupplementaryPassengerData):
    def __init__(self, Cabin=None, PassengerType=None, PassengerCount=None):
        supermod.SupplementaryPassengerData.__init__(self, Cabin, PassengerType, PassengerCount)
supermod.SupplementaryPassengerData.subclass = SupplementaryPassengerDataSub
# end class SupplementaryPassengerDataSub


class StationSub(supermod.Station):
    def __init__(self, Airport=None, StationPublicRemark=None):
        supermod.Station.__init__(self, Airport, StationPublicRemark)
supermod.Station.subclass = StationSub
# end class StationSub


class RIDSRemarkSub(supermod.RIDSRemark):
    def __init__(self, GeneralInformation=None, MaintenanceCode=None, RadioFrequency=None, ServiceCode=None):
        supermod.RIDSRemark.__init__(self, GeneralInformation, MaintenanceCode, RadioFrequency, ServiceCode)
supermod.RIDSRemark.subclass = RIDSRemarkSub
# end class RIDSRemarkSub


class WeightDataSub(supermod.WeightData):
    def __init__(self, Weight=None, WeightUnit=None):
        supermod.WeightData.__init__(self, Weight, WeightUnit)
supermod.WeightData.subclass = WeightDataSub
# end class WeightDataSub


class StopoverSub(supermod.Stopover):
    def __init__(self, Airport=None, StationPublicRemark=None, elementIndex=None):
        supermod.Stopover.__init__(self, Airport, StationPublicRemark, elementIndex)
supermod.Stopover.subclass = StopoverSub
# end class StopoverSub


class UnusualCargoSub(supermod.UnusualCargo):
    def __init__(self, Pieces=None, CargoWeight=None, UnusualCargoType=None):
        supermod.UnusualCargo.__init__(self, Pieces, CargoWeight, UnusualCargoType)
supermod.UnusualCargo.subclass = UnusualCargoSub
# end class UnusualCargoSub



#
# SAX handler used to determine the top level element.
#
class SaxSelectorHandler(handler.ContentHandler):
    def __init__(self):
        self.topElementName = None
    def getTopElementName(self):
        return self.topElementName
    def startElement(self, name, attrs):
        self.topElementName = name
        raise StopIteration


def parseSelect(inFileName):
    infile = file(inFileName, 'r')
    topElementName = None
    parser = make_parser()
    documentHandler = SaxSelectorHandler()
    parser.setContentHandler(documentHandler)
    try:
        try:
            parser.parse(infile)
        except StopIteration:
            topElementName = documentHandler.getTopElementName()
        if topElementName is None:
            raise RuntimeError, 'no top level element'
        topElementName = topElementName.replace('-', '_').replace(':', '_')
        if topElementName not in supermod.__dict__:
            raise RuntimeError, 'no class for top element: %s' % topElementName
        topElement = supermod.__dict__[topElementName]
        infile.seek(0)
        doc = minidom.parse(infile)
    finally:
        infile.close()
    rootNode = doc.childNodes[0]
    rootObj = topElement.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0)
    return rootObj


def saxParse(inFileName):
    parser = make_parser()
    documentHandler = supermod.Sax_EonvelopeHandler()
    parser.setDocumentHandler(documentHandler)
    parser.parse('file:%s' % inFileName)
    rootObj = documentHandler.getRoot()
    #sys.stdout.write('<?xml version="1.0" ?>\n')
    #rootObj.export(sys.stdout, 0)
    return rootObj


def saxParseString(inString):
    parser = make_parser()
    documentHandler = supermod.SaxContentHandler()
    parser.setDocumentHandler(documentHandler)
    parser.feed(inString)
    parser.close()
    rootObj = documentHandler.getRoot()
    #sys.stdout.write('<?xml version="1.0" ?>\n')
    #rootObj.export(sys.stdout, 0)
    return rootObj


def parse(inFilename):
    doc = minidom.parse(inFilename)
    rootNode = doc.documentElement
    rootObj = supermod.Envelope.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_="Eonvelope",
        namespacedef_='')
    doc = None
    return rootObj


def parseString(inString):
    doc = minidom.parseString(inString)
    rootNode = doc.documentElement
    rootObj = supermod.Envelope.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_="Eonvelope",
        namespacedef_='')
    return rootObj


def parseLiteral(inFilename):
    doc = minidom.parse(inFilename)
    rootNode = doc.documentElement
    rootObj = supermod.Envelope.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('from ??? import *\n\n')
    sys.stdout.write('rootObj = Eonvelope(\n')
    rootObj.exportLiteral(sys.stdout, 0, name_="Eonvelope")
    sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""

def usage():
    print USAGE_TEXT
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    root = parse(infilename)


if __name__ == '__main__':
    main()
    #import pdb
    #pdb.run('main()')


