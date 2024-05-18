import mysql.connector
from datetime import datetime, timedelta
import schedule
import time
import requests
import json
import time
import asyncio
import aiohttp

def get_whatsapp_business_api_setting(client_id, location_id):
    conn_epion = mysql.connector.connect(user='root', password='rational', host='localhost', database='cashlessai')
    cursor = conn_epion.cursor(dictionary=True)
    whatsapp_data = {}
    try:
        # check if client has purchased whatsapp api and needs to send opd no near mesaage on whatsapp
        query = "SELECT `Key`, `Value` FROM msgwhatsappbusinessapi WHERE Activate = 1 AND ClientID = %s AND LocationID = %s"
        cursor.execute(query, (client_id, location_id))
        dt_whatsapp = cursor.fetchall()
        # print("dt_whatsapp:", dt_whatsapp)
        if dt_whatsapp:  # check if client has whatsapp related data
            # setting values from whatsapp api table
            for row in dt_whatsapp:
                key = row['Key']
                value = row['Value']

                if key == 'WhatsappBusinessAPIKey':
                    APIKey = value
                elif key == 'WhatsappBusinessAPI':
                    WhatsappBusinessAPI = value
                elif key == 'UserName':
                    UserName = value
                elif key == 'APIUrl':
                    APIUrl = value
                elif key == 'Near_TokenNo_CampaignName':
                    Near_Token_CampaignName = value
                elif key == 'OPD_Started_CampaignName':
                    OPD_Started_CampaignName = value
                elif key == 'OPD_Cancelled_CampaignName':
                    OPD_Cancelled_CampaignName = value
                elif key == 'Cashless_Admission_Salus_CampaignName':
                    Cashless_Admission_Salus_CampaignName = value
                elif key == 'Cashless_Admission_Salus_ContactNo':
                    Cashless_Admission_Salus_ContactNo = value
                elif key== 'cashless_preauth_approval':
                    Cashless_Preauth_Approval = value
                elif key=='cashless_preauth_rejection':
                    Cashless_Preauth_Rejection = value
                elif key=='cashless_preauth_query':
                    Cashless_Preauth_Query = value
                elif key== "cashless_enhancement_approval":
                    Cashless_Enhancement_Approval = value
                elif key=='cashless_enhancement_query2':
                    Cashless_Enhancement_Query = value
                elif key=='cashless_enhancement_rejection':
                    Cashless_Enhancement_Rejection = value


            WhatsBusinessAPIString = f"""{APIKey}#{WhatsappBusinessAPI}#{UserName}#{APIUrl}#{Near_Token_CampaignName}#{OPD_Started_CampaignName}#{OPD_Cancelled_CampaignName}#{Cashless_Admission_Salus_CampaignName}#{Cashless_Admission_Salus_ContactNo}#{Cashless_Preauth_Approval}#{Cashless_Preauth_Rejection}#{Cashless_Preauth_Query}#{Cashless_Enhancement_Approval}#{Cashless_Enhancement_Rejection}#{Cashless_Enhancement_Query}"""
            # print(WhatsBusinessAPIString)
            return WhatsBusinessAPIString
    except mysql.connector.Error as err:
        print("Error: {}".format(err))

    finally:
        cursor.close()
        conn_epion.close()

    return whatsapp_data

client_id=2
location_id=2

WhatsBusinessAPIStringCall=get_whatsapp_business_api_setting(client_id, location_id)
print(WhatsBusinessAPIStringCall)

async def send_whatsapp_messages_async(Cashless_Admission_Salus_ContactNos, APIKey, CampaignName, Param, UserName, APIUrl):
    try:
        for Cashless_Admission_Salus_ContactNo in Cashless_Admission_Salus_ContactNos:
            await send_message_to_whatsapp_async(Cashless_Admission_Salus_ContactNo, APIKey, CampaignName, Param, UserName, APIUrl)
            # print(send_message_to_whatsapp_async)
    except Exception as ex:
        return ex

async def send_message_to_whatsapp_async(Cashless_Admission_Salus_ContactNo, APIKey, CampaignName, Param, UserName, APIUrl):
    try:
        # Your code to send WhatsApp message using WhatsApp API
        await call_whatsapp_api_campaign(APIKey, CampaignName, Cashless_Admission_Salus_ContactNo, Param, UserName, APIUrl)
        # print(response)
        await asyncio.sleep(0.1)  # Simulated delay
    except Exception as ex:
        # Assuming objCommonRepository.LogError is a method to log errors
        return ex

async def call_whatsapp_api_campaign(APIKey, CampaignName, GSM, Param, UserName, APIUrl):
    result = ''
    apiUrl = APIUrl
    # print(apiUrl)
    GSM = '91' + GSM
    jsonData = {
        "apiKey": APIKey,
        "campaignName": CampaignName,
        "destination": GSM,
        "userName": UserName,
        "templateParams": Param,
        "source": "new-landing-page form",
        "media": {},
        "buttons": [],
        "carouselCards": [],
        "location": {}
    }
    # print(jsonData)
    jsonDataString = json.dumps(jsonData)
    headers = {'Content-Type': 'application/json'}
    async with aiohttp.ClientSession() as session:
        async with session.post(apiUrl, data=jsonDataString, headers=headers) as response:
            if response.status == 200:
                print("Message sent successfully!")
            else:
                print(f"Failed to send message. Status code: {response.status}")


def Preauth():
    conn1 = mysql.connector.connect(host="localhost",user="root",password="rational",database="cashlessai")
    cursor1 = conn1.cursor()
    sql1 = """SELECT 
    IFNULL(trnadmission.PatientName, '') AS PatientName,
    IFNULL(trnadmission.ADMNo, '') AS ADMNo,
    IFNULL(trnadmission.ADMDateTime, '') AS ADMDateTime,
    IFNULL(trnadmission.SponsorName, '') AS SponsorName,
    IFNULL(trnadmission.PolicyDetails, '') AS PolicyDetails,
    IFNULL(trnpreauthresponses.TotalAuthorizedAmt, 0) AS TotalAuthorizedAmt,
    IFNULL(auditemailsent.Type, '') AS Type
FROM 
    trnadmission
Inner JOIN 
    trnpreauthresponses ON trnadmission.AdmissionID = trnpreauthresponses.AdmissionID
INNER JOIN 
    auditemailsent ON auditemailsent.AdmissionID = trnadmission.AdmissionID
WHERE 
    auditemailsent.Type IN ('PreAuth', 'PreAuth Query Reply', 'PreAuth Rejection Reply');"""

    cursor1.execute(sql1)
    rows = cursor1.fetchall()
    print(rows)
    for row in rows:
        WhatsBusinessAPIsplitvalues = WhatsBusinessAPIStringCall.split('#')
        APIKEY=WhatsBusinessAPIsplitvalues[0]
        WhatsappBusinessAPI =WhatsBusinessAPIsplitvalues[1]
        UserName =WhatsBusinessAPIsplitvalues[2]
        APIUrl =WhatsBusinessAPIsplitvalues[3]
        Near_Token_CampaignName =WhatsBusinessAPIsplitvalues[4]
        OPD_Started_CampaignName =WhatsBusinessAPIsplitvalues[5]
        OPD_Cancelled_CampaignName =WhatsBusinessAPIsplitvalues[6]
        Cashless_Admission_Salus_CampaignName =WhatsBusinessAPIsplitvalues[7]
        Cashless_Admission_Salus_ContactNo =WhatsBusinessAPIsplitvalues[8]
        Cashless_Admission_Salus_ContactNos = Cashless_Admission_Salus_ContactNo.split(',')
        Cashless_Preauth_Approval=WhatsBusinessAPIsplitvalues[9]
        Cashless_Preauth_Rejected=WhatsBusinessAPIsplitvalues[10]
        Cashless_Preauth_Query=WhatsBusinessAPIsplitvalues[11]
        Cashless_Enhancement_Approval=WhatsBusinessAPIsplitvalues[12]
        Cashless_Enhancement_Rejected=WhatsBusinessAPIsplitvalues[13]
        Cashless_Enhancement_Query=WhatsBusinessAPIsplitvalues[14]
        CampaignName = " "
        Template_Cashless_Admission_Param=[""]*6
        async def main():
            # Your code to set up variables and environment
            if WhatsappBusinessAPI.strip().upper() == "TRUE":
                if APIKEY.strip() and UserName.strip() and APIUrl.strip():
                    Template_Cashless_Admission_Param[0] = str(row[0]).upper()
                    Template_Cashless_Admission_Param[1] = str(row[1]).upper()
                    Template_Cashless_Admission_Param[2] = str(row[2]).upper()
                    Template_Cashless_Admission_Param[3] = str(row[3]).upper()
                    Template_Cashless_Admission_Param[4] = str(row[4]).upper()
                    Template_Cashless_Admission_Param[5] = str(row[5]).upper()
                CampaignName = Cashless_Preauth_Approval
                # print(Template_Cashless_Admission_Para   
                    # Await the coroutine here
                await send_whatsapp_messages_async(Cashless_Admission_Salus_ContactNos, APIKEY, CampaignName, Template_Cashless_Admission_Param, UserName, APIUrl)
        
                result = "OK"
                print(result)
        asyncio.run(main())
#     sql2="""select adm.PatientName, adm.ADMNo,adm.ADMDateTime,adm.SponsorName,PolicyDetails, res.Value,Action , res.ReasonType,sen.Type 
# from cashlessai.trnadmission adm
#     inner join auditpreauthqueries res on res.AdmissionID=adm.AdmissionID  AND res.ReasonType = 'Reject'
#     inner join auditemailsent sen on sen.AdmissionID=adm.AdmissionID
# """
#     cursor1.execute(sql2)
#     rows2 = cursor1.fetchall()
#     for row in rows2:
#         WhatsBusinessAPIsplitvalues = WhatsBusinessAPIStringCall.split('#')
#         APIKEY=WhatsBusinessAPIsplitvalues[0]
#         WhatsappBusinessAPI =WhatsBusinessAPIsplitvalues[1]
#         UserName =WhatsBusinessAPIsplitvalues[2]
#         APIUrl =WhatsBusinessAPIsplitvalues[3]
#         Near_Token_CampaignName =WhatsBusinessAPIsplitvalues[4]
#         OPD_Started_CampaignName =WhatsBusinessAPIsplitvalues[5]
#         OPD_Cancelled_CampaignName =WhatsBusinessAPIsplitvalues[6]
#         Cashless_Admission_Salus_CampaignName =WhatsBusinessAPIsplitvalues[7]
#         Cashless_Admission_Salus_ContactNo =WhatsBusinessAPIsplitvalues[8]
#         Cashless_Admission_Salus_ContactNos = Cashless_Admission_Salus_ContactNo.split(',')
#         Cashless_Preauth_Approval=WhatsBusinessAPIsplitvalues[9]
#         Cashless_Preauth_Rejected=WhatsBusinessAPIsplitvalues[10]
#         Cashless_Preauth_Query=WhatsBusinessAPIsplitvalues[11]
#         Cashless_Enhancement_Approval=WhatsBusinessAPIsplitvalues[12]
#         Cashless_Enhancement_Rejected=WhatsBusinessAPIsplitvalues[13]
#         Cashless_Enhancement_Query=WhatsBusinessAPIsplitvalues[14]
#         CampaignName = " "
#         Template_Cashless_Admission_Param=[""]*6
#         async def main():
#             # Your code to set up variables and environment
#             if WhatsappBusinessAPI.strip().upper() == "TRUE":
#                 if APIKEY.strip() and UserName.strip() and APIUrl.strip():
#                     Template_Cashless_Admission_Param[0] = str(row[0]).upper()
#                     Template_Cashless_Admission_Param[1] = str(row[1]).upper()
#                     Template_Cashless_Admission_Param[2] = str(row[2]).upper()
#                     Template_Cashless_Admission_Param[3] = str(row[3]).upper()
#                     Template_Cashless_Admission_Param[4] = str(row[4]).upper()
#                     Template_Cashless_Admission_Param[5] = str(row[5]).upper()
#                 CampaignName = Cashless_Preauth_Rejected
#                 print(Template_Cashless_Admission_Param)  
#                     # Await the coroutine here
#                 await send_whatsapp_messages_async(Cashless_Admission_Salus_ContactNos, APIKEY, CampaignName, Template_Cashless_Admission_Param, UserName, APIUrl)
#         asyncio.run(main())
#     sql3="""
# select adm.PatientName, adm.ADMNo,adm.ADMDateTime,adm.SponsorName,PolicyDetails,res.Value,Action , res.ReasonType,sen.Type 
# from cashlessai.trnadmission adm
#     inner join auditpreauthqueries res on res.AdmissionID=adm.AdmissionID  AND res.ReasonType = 'Query'
#     inner join auditemailsent sen on sen.AdmissionID=adm.AdmissionID
#     where  (sen.Type = 'PreAuth' or sen.Type = 'PreAuth Query Reply' or sen.Type='PreAuth Rejection Reply');
# """
#     cursor1.execute(sql3)
#     rows3 = cursor1.fetchall()
#     for row in rows3:
#         WhatsBusinessAPIsplitvalues = WhatsBusinessAPIStringCall.split('#')
#         APIKEY=WhatsBusinessAPIsplitvalues[0]
#         WhatsappBusinessAPI =WhatsBusinessAPIsplitvalues[1]
#         UserName =WhatsBusinessAPIsplitvalues[2]
#         APIUrl =WhatsBusinessAPIsplitvalues[3]
#         Near_Token_CampaignName =WhatsBusinessAPIsplitvalues[4]
#         OPD_Started_CampaignName =WhatsBusinessAPIsplitvalues[5]
#         OPD_Cancelled_CampaignName =WhatsBusinessAPIsplitvalues[6]
#         Cashless_Admission_Salus_CampaignName =WhatsBusinessAPIsplitvalues[7]
#         Cashless_Admission_Salus_ContactNo =WhatsBusinessAPIsplitvalues[8]
#         Cashless_Admission_Salus_ContactNos = Cashless_Admission_Salus_ContactNo.split(',')
#         Cashless_Preauth_Approval=WhatsBusinessAPIsplitvalues[9]
#         Cashless_Preauth_Rejected=WhatsBusinessAPIsplitvalues[10]
#         Cashless_Preauth_Query=WhatsBusinessAPIsplitvalues[11]
#         Cashless_Enhancement_Approval=WhatsBusinessAPIsplitvalues[12]
#         Cashless_Enhancement_Rejected=WhatsBusinessAPIsplitvalues[13]
#         Cashless_Enhancement_Query=WhatsBusinessAPIsplitvalues[14]
#         CampaignName = " "
#         Template_Cashless_Admission_Param=[""]*6
#         async def main():
#             # Your code to set up variables and environment
#             if WhatsappBusinessAPI.strip().upper() == "TRUE":
#                 if APIKEY.strip() and UserName.strip() and APIUrl.strip():
#                     Template_Cashless_Admission_Param[0] = str(row[0]).upper()
#                     Template_Cashless_Admission_Param[1] = str(row[1]).upper()
#                     Template_Cashless_Admission_Param[2] = str(row[2]).upper()
#                     Template_Cashless_Admission_Param[3] = str(row[3]).upper()
#                     Template_Cashless_Admission_Param[4] = str(row[4]).upper()
#                     Template_Cashless_Admission_Param[5] = str(row[5]).upper()
#                 CampaignName = Cashless_Preauth_Query
#                 # print(Template_Cashless_Admission_Para   
#                     # Await the coroutine here
#                 await send_whatsapp_messages_async(Cashless_Admission_Salus_ContactNos, APIKEY, CampaignName, Template_Cashless_Admission_Param, UserName, APIUrl)
#         asyncio.run(main())




def Enhance():
    #latest approved
    conn1 = mysql.connector.connect(host="localhost",user="root",password="rational",database="cashlessai")
    cursor1 = conn1.cursor()
    sql4="""SELECT 
    IFNULL(trnadmission.PatientName, '') AS PatientName,
    IFNULL(trnadmission.ADMNo, '') AS ADMNo,
    IFNULL(trnadmission.ADMDateTime, '') AS ADMDateTime,
    IFNULL(trnadmission.SponsorName, '') AS SponsorName,
    IFNULL(trnpreauthresponses.TotalAuthorizedAmt, 0) AS TotalAuthorizedAmt,
    IFNULL(auditemailsent.Type, '') AS Type
FROM 
    trnadmission
Inner JOIN 
    trnpreauthresponses ON trnadmission.AdmissionID = trnpreauthresponses.AdmissionID
INNER JOIN 
    auditemailsent ON auditemailsent.AdmissionID = trnadmission.AdmissionID
WHERE 
    auditemailsent.Type IN ('Enhancement', 'Enhancement Rejection' ,'Enhancement Rejection Reply');"""
    cursor1.execute(sql4)
    rows4 = cursor1.fetchall()
    for row in rows4:
        WhatsBusinessAPIsplitvalues = WhatsBusinessAPIStringCall.split('#')
        APIKEY=WhatsBusinessAPIsplitvalues[0]
        WhatsappBusinessAPI =WhatsBusinessAPIsplitvalues[1]
        UserName =WhatsBusinessAPIsplitvalues[2]
        APIUrl =WhatsBusinessAPIsplitvalues[3]
        Near_Token_CampaignName =WhatsBusinessAPIsplitvalues[4]
        OPD_Started_CampaignName =WhatsBusinessAPIsplitvalues[5]
        OPD_Cancelled_CampaignName =WhatsBusinessAPIsplitvalues[6]
        Cashless_Admission_Salus_CampaignName =WhatsBusinessAPIsplitvalues[7]
        Cashless_Admission_Salus_ContactNo =WhatsBusinessAPIsplitvalues[8]
        Cashless_Admission_Salus_ContactNos = Cashless_Admission_Salus_ContactNo.split(',')
        Cashless_Preauth_Approval=WhatsBusinessAPIsplitvalues[9]
        Cashless_Preauth_Rejected=WhatsBusinessAPIsplitvalues[10]
        Cashless_Preauth_Query=WhatsBusinessAPIsplitvalues[11]
        Cashless_Enhancement_Approval=WhatsBusinessAPIsplitvalues[12]
        Cashless_Enhancement_Rejected=WhatsBusinessAPIsplitvalues[13]
        Cashless_Enhancement_Query=WhatsBusinessAPIsplitvalues[14]
        CampaignName = " "
        Template_Cashless_Admission_Param=[""]*5
        async def main():
            # Your code to set up variables and environment
            if WhatsappBusinessAPI.strip().upper() == "TRUE":
                if APIKEY.strip() and UserName.strip() and APIUrl.strip():
                    Template_Cashless_Admission_Param[0] = str(row[0]).upper()
                    Template_Cashless_Admission_Param[1] = str(row[1]).upper()
                    Template_Cashless_Admission_Param[2] = str(row[2]).upper()
                    Template_Cashless_Admission_Param[3] = str(row[3]).upper()
                    Template_Cashless_Admission_Param[4] = str(row[4]).upper()
                CampaignName = Cashless_Enhancement_Approval
                # print(Template_Cashless_Admission_Para   
                    # Await the coroutine here
                await send_whatsapp_messages_async(Cashless_Admission_Salus_ContactNos, APIKEY, CampaignName, Template_Cashless_Admission_Param, UserName, APIUrl)
        asyncio.run(main())

    # sql5="""select adm.PatientName, adm.ADMNo,adm.ADMDateTime,adm.SponsorName,res.Value,Action  from trnadmission adm
    # inner join auditpreauthqueries res on res.AdmissionID=adm.AdmissionID
    # inner join auditemailsent sen on sen.AdmissionID=adm.AdmissionID
    # where ReasonType='Reject' and sen.Type='Enhancement' or sen.Type='Enhancement Rejection' or sen.Type='Enhancement Rejection Reply';
    # """
    # cursor1.execute(sql5)
    # rows5 = cursor1.fetchall()
    # for row in rows5:
    #     WhatsBusinessAPIsplitvalues = WhatsBusinessAPIStringCall.split('#')
    #     APIKEY=WhatsBusinessAPIsplitvalues[0]
    #     WhatsappBusinessAPI =WhatsBusinessAPIsplitvalues[1]
    #     UserName =WhatsBusinessAPIsplitvalues[2]
    #     APIUrl =WhatsBusinessAPIsplitvalues[3]
    #     Near_Token_CampaignName =WhatsBusinessAPIsplitvalues[4]
    #     OPD_Started_CampaignName =WhatsBusinessAPIsplitvalues[5]
    #     OPD_Cancelled_CampaignName =WhatsBusinessAPIsplitvalues[6]
    #     Cashless_Admission_Salus_CampaignName =WhatsBusinessAPIsplitvalues[7]
    #     Cashless_Admission_Salus_ContactNo =WhatsBusinessAPIsplitvalues[8]
    #     Cashless_Admission_Salus_ContactNos = Cashless_Admission_Salus_ContactNo.split(',')
    #     Cashless_Preauth_Approval=WhatsBusinessAPIsplitvalues[9]
    #     Cashless_Preauth_Rejected=WhatsBusinessAPIsplitvalues[10]
    #     Cashless_Preauth_Query=WhatsBusinessAPIsplitvalues[11]
    #     Cashless_Enhancement_Approval=WhatsBusinessAPIsplitvalues[12]
    #     Cashless_Enhancement_Rejected=WhatsBusinessAPIsplitvalues[13]
    #     Cashless_Enhancement_Query=WhatsBusinessAPIsplitvalues[14]
    #     CampaignName = " "
    #     Template_Cashless_Admission_Param=[""]*6
    #     async def main():
    #         # Your code to set up variables and environment
    #         if WhatsappBusinessAPI.strip().upper() == "TRUE":
    #             if APIKEY.strip() and UserName.strip() and APIUrl.strip():
    #                 Template_Cashless_Admission_Param[0] = str(row[0]).upper()
    #                 Template_Cashless_Admission_Param[1] = str(row[1]).upper()
    #                 Template_Cashless_Admission_Param[2] = str(row[2]).upper()
    #                 Template_Cashless_Admission_Param[3] = str(row[3]).upper()
    #                 Template_Cashless_Admission_Param[4] = str(row[4]).upper()
    #                 Template_Cashless_Admission_Param[5] = str(row[5]).upper()
    #             CampaignName = Cashless_Preauth_Query
    #             # print(Template_Cashless_Admission_Para   
    #                 # Await the coroutine here
    #             await send_whatsapp_messages_async(Cashless_Admission_Salus_ContactNos, APIKEY, CampaignName, Template_Cashless_Admission_Param, UserName, APIUrl)
    #     # asyncio.run(main())

    # sql6="""select adm.PatientName, adm.ADMNo,adm.ADMDateTime,adm.SponsorName,res.Value,Action  from trnadmission adm
    # inner join auditpreauthqueries res on res.AdmissionID=adm.AdmissionID
    # inner join auditemailsent sen on sen.AdmissionID=adm.AdmissionID
    # where ReasonType='Query' and sen.Type='Enhancement' or sen.Type='Enhancement Rejection' or sen.Type='Enhancement Rejection Reply';"""
    # cursor1.execute(sql6)
    # rows6 = cursor1.fetchall()
    # for row in rows6:
    #     WhatsBusinessAPIsplitvalues = WhatsBusinessAPIStringCall.split('#')
    #     APIKEY=WhatsBusinessAPIsplitvalues[0]
    #     WhatsappBusinessAPI =WhatsBusinessAPIsplitvalues[1]
    #     UserName =WhatsBusinessAPIsplitvalues[2]
    #     APIUrl =WhatsBusinessAPIsplitvalues[3]
    #     Near_Token_CampaignName =WhatsBusinessAPIsplitvalues[4]
    #     OPD_Started_CampaignName =WhatsBusinessAPIsplitvalues[5]
    #     OPD_Cancelled_CampaignName =WhatsBusinessAPIsplitvalues[6]
    #     Cashless_Admission_Salus_CampaignName =WhatsBusinessAPIsplitvalues[7]
    #     Cashless_Admission_Salus_ContactNo =WhatsBusinessAPIsplitvalues[8]
    #     Cashless_Admission_Salus_ContactNos = Cashless_Admission_Salus_ContactNo.split(',')
    #     Cashless_Preauth_Approval=WhatsBusinessAPIsplitvalues[9]
    #     Cashless_Preauth_Rejected=WhatsBusinessAPIsplitvalues[10]
    #     Cashless_Preauth_Query=WhatsBusinessAPIsplitvalues[11]
    #     Cashless_Enhancement_Approval=WhatsBusinessAPIsplitvalues[12]
    #     Cashless_Enhancement_Rejected=WhatsBusinessAPIsplitvalues[13]
    #     Cashless_Enhancement_Query=WhatsBusinessAPIsplitvalues[14]
    #     CampaignName = " "
    #     Template_Cashless_Admission_Param=[""]*6
    #     async def main():
    #         # Your code to set up variables and environment
    #         if WhatsappBusinessAPI.strip().upper() == "TRUE":
    #             if APIKEY.strip() and UserName.strip() and APIUrl.strip():
    #                 Template_Cashless_Admission_Param[0] = str(row[0]).upper()
    #                 Template_Cashless_Admission_Param[1] = str(row[1]).upper()
    #                 Template_Cashless_Admission_Param[2] = str(row[2]).upper()
    #                 Template_Cashless_Admission_Param[3] = str(row[3]).upper()
    #                 Template_Cashless_Admission_Param[4] = str(row[4]).upper()
    #                 Template_Cashless_Admission_Param[5] = str(row[5]).upper()

    #             CampaignName = Cashless_Preauth_Query
    #             # print(Template_Cashless_Admission_Para   
    #                 # Await the coroutine here
    #             await send_whatsapp_messages_async(Cashless_Admission_Salus_ContactNos, APIKEY, CampaignName, Template_Cashless_Admission_Param, UserName, APIUrl)
    #     asyncio.run(main())

def FinalApp():
    conn1 = mysql.connector.connect(host="localhost",user="root",password="rational",database="cashlessai")
    cursor1 = conn1.cursor()
    sql7="""SELECT 
    IFNULL(trnadmission.PatientName, '') AS PatientName,
    IFNULL(trnadmission.ADMNo, '') AS ADMNo,
    IFNULL(trnadmission.ADMDateTime, '') AS ADMDateTime,
    IFNULL(trnadmission.SponsorName, '') AS SponsorName,
    IFNULL(trnpreauthresponses.TotalAuthorizedAmt, 0) AS TotalAuthorizedAmt,
    IFNULL(auditemailsent.Type, '') AS Type
FROM 
    trnadmission
Inner JOIN 
    trnpreauthresponses ON trnadmission.AdmissionID = trnpreauthresponses.AdmissionID
INNER JOIN 
    auditemailsent ON auditemailsent.AdmissionID = trnadmission.AdmissionID
WHERE 
    auditemailsent.Type IN ('Final Approval' ,'Final Approval Query Reply' ,'Final Approval Rejection Reply');
    """
    cursor1.execute(sql7)
    rows7 = cursor1.fetchall()
    for row in rows7:
        WhatsBusinessAPIsplitvalues = WhatsBusinessAPIStringCall.split('#')
        APIKEY=WhatsBusinessAPIsplitvalues[0]
        WhatsappBusinessAPI =WhatsBusinessAPIsplitvalues[1]
        UserName =WhatsBusinessAPIsplitvalues[2]
        APIUrl =WhatsBusinessAPIsplitvalues[3]
        Near_Token_CampaignName =WhatsBusinessAPIsplitvalues[4]
        OPD_Started_CampaignName =WhatsBusinessAPIsplitvalues[5]
        OPD_Cancelled_CampaignName =WhatsBusinessAPIsplitvalues[6]
        Cashless_Admission_Salus_CampaignName =WhatsBusinessAPIsplitvalues[7]
        Cashless_Admission_Salus_ContactNo =WhatsBusinessAPIsplitvalues[8]
        Cashless_Admission_Salus_ContactNos = Cashless_Admission_Salus_ContactNo.split(',')
        Cashless_Preauth_Approval=WhatsBusinessAPIsplitvalues[9]
        Cashless_Preauth_Rejected=WhatsBusinessAPIsplitvalues[10]
        Cashless_Preauth_Query=WhatsBusinessAPIsplitvalues[11]
        Cashless_Enhancement_Approval=WhatsBusinessAPIsplitvalues[12]
        Cashless_Enhancement_Rejected=WhatsBusinessAPIsplitvalues[13]
        Cashless_Enhancement_Query=WhatsBusinessAPIsplitvalues[14]
        CampaignName = " "
        Template_Cashless_Admission_Param=[""]*5
        async def main():
            # Your code to set up variables and environment
            if WhatsappBusinessAPI.strip().upper() == "TRUE":
                if APIKEY.strip() and UserName.strip() and APIUrl.strip():
                    Template_Cashless_Admission_Param[0] = str(row[0]).upper()
                    Template_Cashless_Admission_Param[1] = str(row[1]).upper()
                    Template_Cashless_Admission_Param[2] = str(row[2]).upper()
                    Template_Cashless_Admission_Param[3] = str(row[3]).upper()
                    Template_Cashless_Admission_Param[4] = str(row[4]).upper()
                CampaignName = Cashless_Preauth_Query
                # print(Template_Cashless_Admission_Para   
                    # Await the coroutine here
                await send_whatsapp_messages_async(Cashless_Admission_Salus_ContactNos, APIKEY, CampaignName, Template_Cashless_Admission_Param, UserName, APIUrl)

    sql8="""select adm.PatientName, adm.ADMNo,adm.ADMDateTime,adm.SponsorName,res.Value,sen.Type  from trnadmission adm
        inner join auditpreauthqueries res on res.AdmissionID=adm.AdmissionID
        inner join auditemailsent sen on sen.AdmissionID=adm.AdmissionID
        where ReasonType='Query' and sen.Type='Final Approval' or sen.Type='Final Approval Query Reply' or sen.Type='Final Approval Rejection Reply';
    """
    cursor1.execute(sql8)
    rows8 = cursor1.fetchall()
    for row in rows8:
        WhatsBusinessAPIsplitvalues = WhatsBusinessAPIStringCall.split('#')
        APIKEY=WhatsBusinessAPIsplitvalues[0]
        WhatsappBusinessAPI =WhatsBusinessAPIsplitvalues[1]
        UserName =WhatsBusinessAPIsplitvalues[2]
        APIUrl =WhatsBusinessAPIsplitvalues[3]
        Near_Token_CampaignName =WhatsBusinessAPIsplitvalues[4]
        OPD_Started_CampaignName =WhatsBusinessAPIsplitvalues[5]
        OPD_Cancelled_CampaignName =WhatsBusinessAPIsplitvalues[6]
        Cashless_Admission_Salus_CampaignName =WhatsBusinessAPIsplitvalues[7]
        Cashless_Admission_Salus_ContactNo =WhatsBusinessAPIsplitvalues[8]
        Cashless_Admission_Salus_ContactNos = Cashless_Admission_Salus_ContactNo.split(',')
        Cashless_Preauth_Approval=WhatsBusinessAPIsplitvalues[9]
        Cashless_Preauth_Rejected=WhatsBusinessAPIsplitvalues[10]
        Cashless_Preauth_Query=WhatsBusinessAPIsplitvalues[11]
        Cashless_Enhancement_Approval=WhatsBusinessAPIsplitvalues[12]
        Cashless_Enhancement_Rejected=WhatsBusinessAPIsplitvalues[13]
        Cashless_Enhancement_Query=WhatsBusinessAPIsplitvalues[14]
        CampaignName = " "
        Template_Cashless_Admission_Param=[""]*5
        async def main():
            # Your code to set up variables and environment
            if WhatsappBusinessAPI.strip().upper() == "TRUE":
                if APIKEY.strip() and UserName.strip() and APIUrl.strip():
                    Template_Cashless_Admission_Param[0] = str(row[0]).upper()
                    Template_Cashless_Admission_Param[1] = str(row[1]).upper()
                    Template_Cashless_Admission_Param[2] = str(row[2]).upper()
                    Template_Cashless_Admission_Param[3] = str(row[3]).upper()
                    Template_Cashless_Admission_Param[4] = str(row[4]).upper()
                CampaignName = Cashless_Preauth_Query
                # print(Template_Cashless_Admission_Para   
                    # Await the coroutine here
                await send_whatsapp_messages_async(Cashless_Admission_Salus_ContactNos, APIKEY, CampaignName, Template_Cashless_Admission_Param, UserName, APIUrl)


    sql9="""select adm.PatientName, adm.ADMNo,adm.ADMDateTime,adm.SponsorName,res.Value,Action  from trnadmission adm
    inner join auditpreauthqueries res on res.AdmissionID=adm.AdmissionID
    inner join auditemailsent sen on sen.AdmissionID=adm.AdmissionID
    where   ReasonType='Reject' and sen.Type='Final Approval' or sen.Type='Final Approval Query Reply' or sen.Type='Final Approval Rejection Reply';
    """
    cursor1.execute(sql9)
    rows9 = cursor1.fetchall()
    for row in rows9:
        WhatsBusinessAPIsplitvalues = WhatsBusinessAPIStringCall.split('#')
        APIKEY=WhatsBusinessAPIsplitvalues[0]
        WhatsappBusinessAPI =WhatsBusinessAPIsplitvalues[1]
        UserName =WhatsBusinessAPIsplitvalues[2]
        APIUrl =WhatsBusinessAPIsplitvalues[3]
        Near_Token_CampaignName =WhatsBusinessAPIsplitvalues[4]
        OPD_Started_CampaignName =WhatsBusinessAPIsplitvalues[5]
        OPD_Cancelled_CampaignName =WhatsBusinessAPIsplitvalues[6]
        Cashless_Admission_Salus_CampaignName =WhatsBusinessAPIsplitvalues[7]
        Cashless_Admission_Salus_ContactNo =WhatsBusinessAPIsplitvalues[8]
        Cashless_Admission_Salus_ContactNos = Cashless_Admission_Salus_ContactNo.split(',')
        Cashless_Preauth_Approval=WhatsBusinessAPIsplitvalues[9]
        Cashless_Preauth_Rejected=WhatsBusinessAPIsplitvalues[10]
        Cashless_Preauth_Query=WhatsBusinessAPIsplitvalues[11]
        Cashless_Enhancement_Approval=WhatsBusinessAPIsplitvalues[12]
        Cashless_Enhancement_Rejected=WhatsBusinessAPIsplitvalues[13]
        Cashless_Enhancement_Query=WhatsBusinessAPIsplitvalues[14]
        CampaignName = " "
        Template_Cashless_Admission_Param=[""]*5
        async def main():
            # Your code to set up variables and environment
            if WhatsappBusinessAPI.strip().upper() == "TRUE":
                if APIKEY.strip() and UserName.strip() and APIUrl.strip():
                    Template_Cashless_Admission_Param[0] = str(row[0]).upper()
                    Template_Cashless_Admission_Param[1] = str(row[1]).upper()
                    Template_Cashless_Admission_Param[2] = str(row[2]).upper()
                    Template_Cashless_Admission_Param[3] = str(row[3]).upper()
                    Template_Cashless_Admission_Param[4] = str(row[4]).upper()
                CampaignName = Cashless_Preauth_Query
                # print(Template_Cashless_Admission_Para   
                    # Await the coroutine here
                await send_whatsapp_messages_async(Cashless_Admission_Salus_ContactNos, APIKEY, CampaignName, Template_Cashless_Admission_Param, UserName, APIUrl)

def Settlefightback():
    #latest approved
    conn1 = mysql.connector.connect(host="localhost",user="root",password="rational",database="cashlessai")
    cursor1 = conn1.cursor()
    sql10="""SELECT 
    IFNULL(trnadmission.PatientName, '') AS PatientName,
    IFNULL(trnadmission.ADMNo, '') AS ADMNo,
    IFNULL(trnadmission.ADMDateTime, '') AS ADMDateTime,
    IFNULL(trnadmission.SponsorName, '') AS SponsorName,
    IFNULL(trnpreauthresponses.TotalAuthorizedAmt, 0) AS TotalAuthorizedAmt,
    IFNULL(auditemailsent.Type, '') AS Type
FROM 
    trnadmission
Inner JOIN 
    trnpreauthresponses ON trnadmission.AdmissionID = trnpreauthresponses.AdmissionID
INNER JOIN 
    auditemailsent ON auditemailsent.AdmissionID = trnadmission.AdmissionID
WHERE 
    auditemailsent.Type IN ('Settlement Fightback' ,'Settlement Fightback Query Reply' ,'Settlement Fightback Rejection Reply');
    """
    cursor1.execute(sql10)
    rows10 = cursor1.fetchall()
    for row in rows10:
        WhatsBusinessAPIsplitvalues = WhatsBusinessAPIStringCall.split('#')
        APIKEY=WhatsBusinessAPIsplitvalues[0]
        WhatsappBusinessAPI =WhatsBusinessAPIsplitvalues[1]
        UserName =WhatsBusinessAPIsplitvalues[2]
        APIUrl =WhatsBusinessAPIsplitvalues[3]
        Near_Token_CampaignName =WhatsBusinessAPIsplitvalues[4]
        OPD_Started_CampaignName =WhatsBusinessAPIsplitvalues[5]
        OPD_Cancelled_CampaignName =WhatsBusinessAPIsplitvalues[6]
        Cashless_Admission_Salus_CampaignName =WhatsBusinessAPIsplitvalues[7]
        Cashless_Admission_Salus_ContactNo =WhatsBusinessAPIsplitvalues[8]
        Cashless_Admission_Salus_ContactNos = Cashless_Admission_Salus_ContactNo.split(',')
        Cashless_Preauth_Approval=WhatsBusinessAPIsplitvalues[9]
        Cashless_Preauth_Rejected=WhatsBusinessAPIsplitvalues[10]
        Cashless_Preauth_Query=WhatsBusinessAPIsplitvalues[11]
        Cashless_Enhancement_Approval=WhatsBusinessAPIsplitvalues[12]
        Cashless_Enhancement_Rejected=WhatsBusinessAPIsplitvalues[13]
        Cashless_Enhancement_Query=WhatsBusinessAPIsplitvalues[14]
        CampaignName = " "
        Template_Cashless_Admission_Param=[""]*5
        async def main():
            # Your code to set up variables and environment
            if WhatsappBusinessAPI.strip().upper() == "TRUE":
                if APIKEY.strip() and UserName.strip() and APIUrl.strip():
                    Template_Cashless_Admission_Param[0] = str(row[0]).upper()
                    Template_Cashless_Admission_Param[1] = str(row[1]).upper()
                    Template_Cashless_Admission_Param[2] = str(row[2]).upper()
                    Template_Cashless_Admission_Param[3] = str(row[3]).upper()
                    Template_Cashless_Admission_Param[4] = str(row[4]).upper()
                CampaignName = Cashless_Preauth_Query
                # print(Template_Cashless_Admission_Para   
                    # Await the coroutine here
                await send_whatsapp_messages_async(Cashless_Admission_Salus_ContactNos, APIKEY, CampaignName, Template_Cashless_Admission_Param, UserName, APIUrl)


    sql11="""select adm.PatientName, adm.ADMNo,adm.ADMDateTime,adm.SponsorName,res.Value,sen.Type  from trnadmission adm
    inner join auditpreauthqueries res on res.AdmissionID=adm.AdmissionID
    inner join auditemailsent sen on sen.AdmissionID=adm.AdmissionID
    where ReasonType='Query' and sen.Type='Settlement Fightback' or sen.Type='Settlement Fightback Query Reply' or sen.Type='Settlement Fightback Rejection Reply';
    """
    cursor1.execute(sql11)
    rows11 = cursor1.fetchall()
    for row in rows11:
        WhatsBusinessAPIsplitvalues = WhatsBusinessAPIStringCall.split('#')
        APIKEY=WhatsBusinessAPIsplitvalues[0]
        WhatsappBusinessAPI =WhatsBusinessAPIsplitvalues[1]
        UserName =WhatsBusinessAPIsplitvalues[2]
        APIUrl =WhatsBusinessAPIsplitvalues[3]
        Near_Token_CampaignName =WhatsBusinessAPIsplitvalues[4]
        OPD_Started_CampaignName =WhatsBusinessAPIsplitvalues[5]
        OPD_Cancelled_CampaignName =WhatsBusinessAPIsplitvalues[6]
        Cashless_Admission_Salus_CampaignName =WhatsBusinessAPIsplitvalues[7]
        Cashless_Admission_Salus_ContactNo =WhatsBusinessAPIsplitvalues[8]
        Cashless_Admission_Salus_ContactNos = Cashless_Admission_Salus_ContactNo.split(',')
        Cashless_Preauth_Approval=WhatsBusinessAPIsplitvalues[9]
        Cashless_Preauth_Rejected=WhatsBusinessAPIsplitvalues[10]
        Cashless_Preauth_Query=WhatsBusinessAPIsplitvalues[11]
        Cashless_Enhancement_Approval=WhatsBusinessAPIsplitvalues[12]
        Cashless_Enhancement_Rejected=WhatsBusinessAPIsplitvalues[13]
        Cashless_Enhancement_Query=WhatsBusinessAPIsplitvalues[14]
        CampaignName = " "
        Template_Cashless_Admission_Param=[""]*5
        async def main():
            # Your code to set up variables and environment
            if WhatsappBusinessAPI.strip().upper() == "TRUE":
                if APIKEY.strip() and UserName.strip() and APIUrl.strip():
                    Template_Cashless_Admission_Param[0] = str(row[0]).upper()
                    Template_Cashless_Admission_Param[1] = str(row[1]).upper()
                    Template_Cashless_Admission_Param[2] = str(row[2]).upper()
                    Template_Cashless_Admission_Param[3] = str(row[3]).upper()
                    Template_Cashless_Admission_Param[4] = str(row[4]).upper()
                CampaignName = Cashless_Preauth_Query
                # print(Template_Cashless_Admission_Para   
                    # Await the coroutine here
                await send_whatsapp_messages_async(Cashless_Admission_Salus_ContactNos, APIKEY, CampaignName, Template_Cashless_Admission_Param, UserName, APIUrl)

    sql12="""select adm.PatientName, adm.ADMNo,adm.ADMDateTime,adm.SponsorName,res.Value,Action  from trnadmission adm
    inner join auditpreauthqueries res on res.AdmissionID=adm.AdmissionID
    inner join auditemailsent sen on sen.AdmissionID=adm.AdmissionID
    where ReasonType='Reject' and sen.Type='Settlement Fightback' or sen.Type='Settlement Fightback Query Reply' or sen.Type='Settlement Fightback Rejection Reply';
    """
    cursor1.execute(sql12)
    rows12 = cursor1.fetchall()
    for row in rows12:
        WhatsBusinessAPIsplitvalues = WhatsBusinessAPIStringCall.split('#')
        APIKEY=WhatsBusinessAPIsplitvalues[0]
        WhatsappBusinessAPI =WhatsBusinessAPIsplitvalues[1]
        UserName =WhatsBusinessAPIsplitvalues[2]
        APIUrl =WhatsBusinessAPIsplitvalues[3]
        Near_Token_CampaignName =WhatsBusinessAPIsplitvalues[4]
        OPD_Started_CampaignName =WhatsBusinessAPIsplitvalues[5]
        OPD_Cancelled_CampaignName =WhatsBusinessAPIsplitvalues[6]
        Cashless_Admission_Salus_CampaignName =WhatsBusinessAPIsplitvalues[7]
        Cashless_Admission_Salus_ContactNo =WhatsBusinessAPIsplitvalues[8]
        Cashless_Admission_Salus_ContactNos = Cashless_Admission_Salus_ContactNo.split(',')
        Cashless_Preauth_Approval=WhatsBusinessAPIsplitvalues[9]
        Cashless_Preauth_Rejected=WhatsBusinessAPIsplitvalues[10]
        Cashless_Preauth_Query=WhatsBusinessAPIsplitvalues[11]
        Cashless_Enhancement_Approval=WhatsBusinessAPIsplitvalues[12]
        Cashless_Enhancement_Rejected=WhatsBusinessAPIsplitvalues[13]
        Cashless_Enhancement_Query=WhatsBusinessAPIsplitvalues[14]
        CampaignName = " "
        Template_Cashless_Admission_Param=[""]*5
        async def main():
            # Your code to set up variables and environment
            if WhatsappBusinessAPI.strip().upper() == "TRUE":
                if APIKEY.strip() and UserName.strip() and APIUrl.strip():
                    Template_Cashless_Admission_Param[0] = str(row[0]).upper()
                    Template_Cashless_Admission_Param[1] = str(row[1]).upper()
                    Template_Cashless_Admission_Param[2] = str(row[2]).upper()
                    Template_Cashless_Admission_Param[3] = str(row[3]).upper()
                    Template_Cashless_Admission_Param[4] = str(row[4]).upper()
                CampaignName = Cashless_Preauth_Query
                # print(Template_Cashless_Admission_Para   
                    # Await the coroutine here
                await send_whatsapp_messages_async(Cashless_Admission_Salus_ContactNos, APIKEY, CampaignName, Template_Cashless_Admission_Param, UserName, APIUrl)



Enhance()


