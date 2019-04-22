import sllurp
from sllurp import llrp
from twisted.internet import reactor
import logging
import pprint

logging.basicConfig(filename='rfid.log', filemode='w')

sllurp_logger = logging.getLogger('sllurp')
sllurp_logger.setLevel(logging.INFO)

def cb (tagReport):
    tags = tagReport.msgdict['RO_ACCESS_REPORT']['TagReportData']
    if len(tags):
        print('saw tag(s):', tags)
        sllurp_logger.info('saw tag(s): %s', pprint.pformat(tags))
    else:
        print('no tags seen')
        sllurp_logger.info('no tags seen')
        return

factory = llrp.LLRPClientFactory(duration=0.02, tx_power=0, start_inventory=True, impinj_tag_content_selector={'EnableRFPhaseAngle':True, 'EnablePeakRSSI': False, 'EnableRFDopplerFrequency': False})
factory.addTagReportCallback(cb)
reactor.connectTCP('169.254.1.1', llrp.LLRP_PORT, factory)
reactor.run()


