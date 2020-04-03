# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 23:47:54 2020

@author: willi
"""

#import pandas as pd
import asyncio, time
import aiohttp
from aiohttp import ClientSession
import nest_asyncio
nest_asyncio.apply()
#https://stackoverflow.com/questions/38110433/using-python-and-3-aiohttp-to-find-the-url-after-redirect-when-timeout

start_time = time.time()

timeout = aiohttp.ClientTimeout(total=1)
connector = aiohttp.TCPConnector(limit=10)

origWebsites = ["e-emphasys.com", "coder.aapc.com", "aphw.com", "transparencymarketresearch.com", "flashglobal.com", "caspio.com", "datacontrolinc.com", "shippingsolutions.com", "calhospital.org", "americanoutcomes.com", "nelifecare.org", "harbinclinic.com", "hippocmms.com", "homehealthcarenews.com", "deteringconsulting.com", "hmenews.com", "kabafusion.com", "bcbsnd.com", "ieomsociety.org", "emaint.com", "harvardpilgrim.org", "brightstarcare.com", "vcmeridian.com", "springerpub.com", "azarthritis.com", "pharmacytimes.com", "medicorx.com", "acronyms.thefreedictionary.com", "semc.org", "greentangerinespa.com", "startupgrind.com", "magnatag.com", "nahc.org", "facilitiessurvey.com", "federalregister.gov", "bevnet.com", "redlinepharmacy.com", "higheredjobs.com", "constellationhb.com", "stechies.com", "dataforma.com", "elvadms.com", "orhp.com", "careprohs.com", "optimuminfo.com", "redmaple.com", "newhomeatl.com", "red74tech.com", "oley.org", "resoundenergy.com", "datafactz.com", "secondcrm.com", "wbdg.org", "knowledge.panxpan.com", "dealerscircle.com", "arifleet.com", "digitalhill.com", "genflex.com", "buildermt.com", "capecodhealth.org", "aiag.org", "manageengine.com", "oesa.org", "warrantyweek.com", "masyc.com", "metasystems.com", "regionalhc.com", "ashp.org", "uwhealth.org", "soleohealth.com", "kdwltd.com", "newmanrh.org", "contractlogix.com", "thinkhomecare.org", "provider.bluecrossma.com", "csigiv.com", "briovarxinfusion.com", "carecentrix.com", "foodsafetymagazine.com", "nascentiahealth.org", "logisticsmgmt.com", "thehill.com", "grandviewresearch.com", "iofficecorp.com", "nerej.com", "pediatrichomeservice.com", "macallister.com", "careercast.com", "sphp.com", "myoptionone.com", "chartwellpa.com", "healthforcega.com", "accredo.com", "mediware.com", "pubsonline.informs.org", "brooklyn.news12.com", "amberpharmacy.com", "nhia.org", "money.usnews.com", "industryweek.com", "posrg.com", "pharmacarehawaii.com", "msdonline.com", "carle.org", "susquehannahealth.org", "melrosewakefield.org", "hcpro.com", "vator.tv", "igi-global.com", "hypertherm.com", "jobs.sciencecareers.org", "servicechannel.com", "americaremedical.com", "achc.org", "nmccat.com", "mayfieldmedical.com", "nap.edu", "ssents.com", "maintenanceconnection.com", "maintenancecare.com", "novosolutions.com", "micromain.com", "avera.org", "boydcorp.com", "nearshoreamericas.com", "adastracorp.com", "componentcontrol.com", "tavant.com", "hnfs.com", "popcornapps.com", "eetimes.com", "bmchp.org", "morrishospital.org", "barcoding.com", "blog.qsifacilities.com", "homecaremag.com", "medicaid.ncdhhs.gov", "dhhr.wv.gov", "huntsvillehospital.org", "seniornavigator.org", "baptisthealth.com", "centralhealth.net", "pmaonline.com", "nurseregistry.com", "coramhc.com", "houstondynamic.com", "specialty.optumrx.com", "nbninfusions.com", "marketwatch.com", "qwarecmms.com", "gao.gov", "bcbsvt.com", "chapinc.org", "conservcare.net", "bluecrossnc.com", "modernhealthcare.com", "autocartruck.com", "delmar.edu", "zafire.com", "covingtonassociates.com", "adena.org", "advhomecare.org", "businesswire.com", "trinityhealthathome.org", "maintenance.org", "dphhs.mt.gov", "dukehealth.org", "mpulsesoftware.com", "froedtert.com", "msidata.com", "dpsi.com", "jjkeller.com", "b2wsoftware.com", "karmak.com", "cogz.com", "reliableplant.com", "california.jobing.com", "chiptechsolutions.com", "nexgenam.com", "pri-med.com", "mcknights.com", "caremastermedical.com", "mpofcinci.com", "government-fleet.com", "kennebecpharmacy.com", "blog.devicemagic.com", "alliancerxwp.com", "searshomeservices.com", "fiercehealthcare.com", "preferredhomecare.com", "infusionventures.com", "camcode.com", "casamba.net", "idsociety.org", "swgeneral.com", "sunflowerhomehealth.com", "plantengineering.com", "commonwealthcarealliance.org", "globenewswire.com", "urac.org", "paragonhealthcare.com", "msa-corp.com", "mapcon.com", "careersinfood.com", "bioinformant.com", "wboc.com", "floridawestcoast.sunstyledesign.com", "healthnewsreview.org", "smglobal.com", "brewbound.com", "universalss.com", "medicare.gov", "maintsmart.com", "psqh.com", "p1group.com", "help.servicedeskplus.com", "learn4good.com"]

Current_Website = []

async def checkURLs(websites):
    for ind, url in enumerate(websites):
        try:
            async with ClientSession() as session:
                async with session.get(url) as r:
                    print(r.status)
                    print(r.url)
                    r = r.url
        except:
            try:
                async with ClientSession() as session:
                    async with session.get("http://" + url) as r:
                        print(r.status)
                        print(r.url)
                        r = r.url
            except:
                print("exception")
                Current_Website.append(url)
                continue
        Current_Website.append(r)
        
    #return Current_Website

loop = asyncio.get_event_loop()

loop.run_until_complete(checkURLs(origWebsites))

print("--- %s seconds ---" % (time.time() - start_time))