# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 13:54:13 2020

@author: William Barber
"""
import re, requests
import time
import asyncio
from fn import _
from fn.iters import flatten, filter
from util import force_async, force_sync
start_time = time.time()

def getPageContent(url):   
    result = {
        'code': None,
        'status': None,
        'content': None,
        'headers': None,
        'realurl': url
    }
    #conside adding timeout=
    res = requests.Session().get(url, allow_redirects=True)
    
    
    result['headers'] = dict()
    for header, value in res.headers.items():
        if type(header) != str:
            header = str(header)

        if type(value) != str:
            value = str(value)

    result['headers'][header.lower()] = value
    result['realurl'] = res.url
    result['code'] = str(res.status_code)
    result['content'] = res.content.decode("utf-8")
    return result

def parseEmails(data):
    emails = set()
    matches = re.findall(r'([\%a-zA-Z\.0-9_\-\+]+@[a-zA-Z\.0-9\-]+\.[a-zA-Z\.0-9\-]+)', data)

    for match in matches:
        #print("Found possible email: " + match)

        # Handle false positive matches
        if len(match) < 5:
            print("Skipped likely invalid email address.")
            continue

        # Handle messed up encodings
        if "%" in match:
            print("Skipped invalid email address: " + match)
            continue

        # Handle truncated emails
        if "..." in match:
            print("Skipped incomplete e-mail address: " + match)
            continue

        emails.add(match)

    return list(emails)

@force_async
def getEmails(domain):
    print('Receiving emails from %s', domain)
    res = getPageContent("http://www.skymem.info/srch?q=" + domain)
    
    # Extract emails from results page
    emails = parseEmails(res['content'])
    
    # Loop through first 20 pages of results
    domain_ids = re.findall(r'<a href="/domain/([a-z0-9]+)\?p=', res['content'])

    if not domain_ids:
        return None

    domain_id = domain_ids[0]

    for page in range(1, 21):
        res = getPageContent("http://www.skymem.info/domain/" + domain_id + "?p=" + str(page))

        if res['content'] is None:
            break

        emails = parseEmails(res['content'])

        # Check if we're on the last page of results
        max_page = 0
        pages = re.findall(r'/domain/' + domain_id + '\?p=(\d+)', res['content'])
        for p in pages:
            if int(p) >= max_page:
                max_page = int(p)
            if page >= max_page:
                break

        if emails is None:
            return None
        else:
            return emails

allEmails = []

domains = ["e-emphasys.com", "coder.aapc.com", "aphw.com", "transparencymarketresearch.com", "flashglobal.com", "caspio.com", "datacontrolinc.com", "shippingsolutions.com", "calhospital.org", "americanoutcomes.com", "nelifecare.org", "harbinclinic.com", "hippocmms.com", "homehealthcarenews.com", "deteringconsulting.com", "hmenews.com", "kabafusion.com", "bcbsnd.com", "ieomsociety.org", "emaint.com", "harvardpilgrim.org", "brightstarcare.com", "vcmeridian.com", "springerpub.com", "azarthritis.com", "pharmacytimes.com", "medicorx.com", "acronyms.thefreedictionary.com", "semc.org", "greentangerinespa.com", "startupgrind.com", "magnatag.com", "nahc.org", "facilitiessurvey.com", "federalregister.gov", "bevnet.com", "redlinepharmacy.com", "higheredjobs.com", "constellationhb.com", "stechies.com", "dataforma.com", "elvadms.com", "orhp.com", "careprohs.com", "optimuminfo.com", "redmaple.com", "newhomeatl.com", "red74tech.com", "oley.org", "resoundenergy.com", "datafactz.com", "secondcrm.com", "wbdg.org", "knowledge.panxpan.com", "dealerscircle.com", "arifleet.com", "digitalhill.com", "genflex.com", "buildermt.com", "capecodhealth.org", "aiag.org", "manageengine.com", "oesa.org", "warrantyweek.com", "masyc.com", "metasystems.com", "regionalhc.com", "ashp.org", "uwhealth.org", "soleohealth.com", "kdwltd.com", "newmanrh.org", "contractlogix.com", "thinkhomecare.org", "provider.bluecrossma.com", "csigiv.com", "briovarxinfusion.com", "carecentrix.com", "foodsafetymagazine.com", "nascentiahealth.org", "logisticsmgmt.com", "thehill.com", "grandviewresearch.com", "iofficecorp.com", "nerej.com", "pediatrichomeservice.com", "macallister.com", "careercast.com", "sphp.com", "myoptionone.com", "chartwellpa.com", "healthforcega.com", "accredo.com", "mediware.com", "pubsonline.informs.org", "brooklyn.news12.com", "amberpharmacy.com", "nhia.org", "money.usnews.com", "industryweek.com", "posrg.com", "pharmacarehawaii.com", "msdonline.com", "carle.org", "susquehannahealth.org", "melrosewakefield.org", "hcpro.com", "vator.tv", "igi-global.com", "hypertherm.com", "jobs.sciencecareers.org", "servicechannel.com", "americaremedical.com", "achc.org", "nmccat.com", "mayfieldmedical.com", "nap.edu", "ssents.com", "maintenanceconnection.com", "maintenancecare.com", "novosolutions.com", "micromain.com", "avera.org", "boydcorp.com", "nearshoreamericas.com", "adastracorp.com", "componentcontrol.com", "tavant.com", "hnfs.com", "popcornapps.com", "eetimes.com", "bmchp.org", "morrishospital.org", "barcoding.com", "blog.qsifacilities.com", "homecaremag.com", "medicaid.ncdhhs.gov", "dhhr.wv.gov", "huntsvillehospital.org", "seniornavigator.org", "baptisthealth.com", "centralhealth.net", "pmaonline.com", "nurseregistry.com", "coramhc.com", "houstondynamic.com", "specialty.optumrx.com", "nbninfusions.com", "marketwatch.com", "qwarecmms.com", "gao.gov", "bcbsvt.com", "chapinc.org", "conservcare.net", "bluecrossnc.com", "modernhealthcare.com", "autocartruck.com", "delmar.edu", "zafire.com", "covingtonassociates.com", "adena.org", "advhomecare.org", "businesswire.com", "trinityhealthathome.org", "maintenance.org", "dphhs.mt.gov", "dukehealth.org", "mpulsesoftware.com", "froedtert.com", "msidata.com", "dpsi.com", "jjkeller.com", "b2wsoftware.com", "karmak.com", "cogz.com", "reliableplant.com", "california.jobing.com", "chiptechsolutions.com", "nexgenam.com", "pri-med.com", "mcknights.com", "caremastermedical.com", "mpofcinci.com", "government-fleet.com", "kennebecpharmacy.com", "blog.devicemagic.com", "alliancerxwp.com", "searshomeservices.com", "fiercehealthcare.com", "preferredhomecare.com", "infusionventures.com", "camcode.com", "casamba.net", "idsociety.org", "swgeneral.com", "sunflowerhomehealth.com", "plantengineering.com", "commonwealthcarealliance.org", "globenewswire.com", "urac.org", "paragonhealthcare.com", "msa-corp.com", "mapcon.com", "careersinfood.com", "bioinformant.com", "wboc.com", "floridawestcoast.sunstyledesign.com", "healthnewsreview.org", "smglobal.com", "brewbound.com", "universalss.com", "medicare.gov", "maintsmart.com", "psqh.com", "p1group.com", "help.servicedeskplus.com", "learn4good.com"]

#tested on 97 domains, results were 0.35560 seconds
domainsToSearch = len(domains)

print("predicted completion in " + str(round((0.35560*domainsToSearch)/60, 2)) + " mins, aka " +
      str(round((0.35560*domainsToSearch)/(60*60), 2)) + " hours")

@force_sync
async def main():
    domain_requests = []
    for domain in domains:
        domain_requests.append(getEmails(domain))

    allEmails = await asyncio.gather(*domain_requests)
    validEmails = list(filter(_ != None, flatten(allEmails)))

    print(validEmails)

main()

print("--- %s seconds ---" % (time.time() - start_time))
print("Average number of seconds per domain search: " + str((time.time() - start_time)/domainsToSearch))
