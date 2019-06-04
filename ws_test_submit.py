import zeep
import random
import time
from zeep.exceptions import Error as zError
import os
import base64
from zeep import xsd
import pprint
from lxml import etree
import json

client_identifier = str(time.time()).split('.')[0]
date_requested = int(str(time.time()+86400000).split('.')[0])
file_size=100000
pd_url = 'https://qa-tdc13.translations.com/PD/services'
pd_shortcode = 'GEN000006'
pa_client_ticket = '4YESyxwCtA2h2qoZYudcMsnpTWF1uB/q'
src_lang = 'en_US'
tgt_langs = ['de_DE', 'fr_FR']
mime_type = 'application/msword'
file_classifier = 'word_txml'
project_ticket = ''
pd_username = 'testuser1010'
pd_password = 'password1!'
file_path = "C:\\a4"
file_list = ["Thisisatest1.docx"]


def submit_document_with_binary_resource(file_name, token):
    print "entering submit_document_with_binary_resource"
    # ns0:submitDocumentWithBinaryResource(documentInfo: ns1:DocumentInfo, resourceInfo: ns1:ResourceInfo,
    # data: ns2:base64Binary, userId: xsd:string)
    doc_info = create_document_info(doc_name=file_name, doc_instructions='')
    # file_size = os.path.getsize(os.path.join(file_path, file_name))
    res_info = create_resource_info(doc_name=file_name, doc_size=file_size)
    print "exited create_resource_info"
    with open(os.path.join(file_path, file_name), 'rb') as source_doc:
        print "opened the file " + os.path.join(file_path, file_name)
        file_contents = source_doc.read()
        print "----------- Begin document info -------------"
        print doc_info
        print "----------- End document info -------------"
        print "----------- Begin resource info -------------"
        print res_info
        print "----------- End resource info -------------"
        submit_message = document_client.create_message(document_service, 'submitDocumentWithBinaryResource',
                                       documentInfo=doc_info, resourceInfo=res_info,
                                       data=file_contents, userId=token)
        print "----------- Begin submit message -------------"
        print etree.tostring(submit_message, pretty_print=True)
        print "----------- End submit message -------------"
        submit_document_response = document_service.submitDocumentWithBinaryResource(documentInfo=doc_info,
                                                                                     resourceInfo=res_info,
                                                                                     data=file_contents,
                                                                                     userId=token)
        print "Document submitted " + file_name + " with ticket " + submit_document_response['ticketId']
    return submit_document_response['ticketId']


def create_submission_info(sub_name):
    print "entering create_submission_info"
    # ns1:SubmissionInfo(additionalCosts: xsd:string, autoStartChilds: xsd:boolean, claimScope: ns1:ClaimScopeEnum,
    # clientIdentifier: xsd:string, dateRequested: ns1:Date, internalNotes: xsd:string, metadata: ns1:Metadata[],
    # name: xsd:string, officeName: xsd:string, paClientTicket: xsd:string, paJobNumber: xsd:string,
    # priority: ns1:Priority, projectTicket: xsd:string, revenue: xsd:double, submissionBackground: xsd:string,
    # submissionCustomFields: ns1:SubmissionCustomFields[], submitters: xsd:string[],
    # workflowDefinitionTicket: xsd:string)
    #
    # ns1:Date(critical: xsd:boolean, date: xsd:long)
    #
    # ns1:Priority(name: xsd:string, value: xsd:int)
    prio_type = document_client.get_type('ns1:Priority')
    prio_wrap = xsd.Element('Priority', prio_type)
    prio_value = prio_wrap(name='', value=1)

    date_type = document_client.get_type('ns1:Date')
    date_wrap = xsd.Element('Date', date_type)
    date_value = date_wrap(critical=False, date=date_requested)

    # date_req = document_factory.Date(critical=zeep.xsd.Nil, date=date_requested)
    subinfo_type = document_client.get_type('ns1:SubmissionInfo')
    subinfo_wrap = xsd.Element('SubmissionInfo', subinfo_type)
    submission_info = subinfo_wrap(additionalCosts=zeep.xsd.Nil,
                                   autoStartChilds=zeep.xsd.Nil,
                                   claimScope=zeep.xsd.Nil,
                                   clientIdentifier=client_identifier,
                                   dateRequested=date_value,
                                   internalNotes=zeep.xsd.Nil,
                                   metadata=[],
                                   name=sub_name,
                                   officeName=zeep.xsd.Nil,
                                   paClientTicket=pa_client_ticket,
                                   paJobNumber=zeep.xsd.Nil,
                                   priority=prio_value,
                                   projectTicket=project_ticket,
                                   revenue=zeep.xsd.Nil,
                                   submissionBackground=zeep.xsd.Nil,
                                   submissionCustomFields=zeep.xsd.Nil,
                                   submitters=zeep.xsd.Nil,
                                   workflowDefinitionTicket=zeep.xsd.Nil)
    print "--------------- Begin submission info ---------------"
    print submission_info
    print "--------------- Begin submission info ---------------"
    return submission_info


def create_document_info(doc_name, doc_instructions):
    print "entering create_document_info"
    # ns1:DocumentInfo(childDocumentInfos: ns1:DocumentInfo[], clientIdentifier: xsd:string, dateRequested: ns1:Date,
    # instructions: xsd:string, metadata: ns1:Metadata[], name: xsd:string, projectTicket: xsd:string,
    # sourceLocale: xsd:string, submissionTicket: xsd:string, targetInfos: ns1:TargetInfo[], wordCount: xsd:int)
    tgt_infos = create_target_info()
    date_type = document_client.get_type('ns1:Date')
    date_wrap = xsd.Element('Date', date_type)
    date_value = date_wrap(critical=False, date=date_requested)

    docinfo_type = document_client.get_type('ns1:DocumentInfo')
    docinfo_wrap = xsd.Element('DocumentInfo', docinfo_type)
    if submission_ticket is not None:
        document_info = docinfo_wrap(childDocumentInfos=zeep.xsd.Nil,
                                     clientIdentifier=client_identifier,
                                     dateRequested=date_value,
                                     instructions=zeep.xsd.Nil,
                                     metadata=[],
                                     name=doc_name,
                                     projectTicket=project_ticket,
                                     sourceLocale=src_lang,
                                     submissionTicket=submission_ticket,
                                     targetInfos=tgt_infos,
                                     wordCount=zeep.xsd.Nil)
    else:
        document_info = docinfo_wrap(childDocumentInfos=zeep.xsd.Nil,
                                     clientIdentifier=client_identifier,
                                     dateRequested=date_value,
                                     instructions=zeep.xsd.Nil,
                                     metadata=[],
                                     name=doc_name,
                                     projectTicket=project_ticket,
                                     sourceLocale=src_lang,
                                     submissionTicket=zeep.xsd.Nil,
                                     targetInfos=tgt_infos,
                                     wordCount=zeep.xsd.Nil)
    return document_info


def create_resource_info(doc_name, doc_size):
    print "entering create_resource_info"
    # ns1:ResourceInfo(classifier: xsd:string, clientIdentifier: xsd:string, description: xsd:string,
    # encoding: xsd:string, md5Checksum: xsd:string, mimeType: xsd:string, name: xsd:string, path: xsd:string,
    # resourceInfoId: xsd:long, size: xsd:long, type: ns1:ResourceType)

    restype_type = document_client.get_type('ns1:ResourceType')
    restype_wrap = xsd.Element('ResourceType', restype_type)
    resource_type = restype_wrap(value=zeep.xsd.Nil)

    resinfo_type = document_client.get_type('ns1:ResourceInfo')
    resinfo_wrap = xsd.Element('ResourceInfo', resinfo_type)
    resource_info = resinfo_wrap(classifier=file_classifier,
                                 clientIdentifier=client_identifier,
                                 description=zeep.xsd.Nil,
                                 encoding=zeep.xsd.Nil,
                                 md5Checksum=zeep.xsd.Nil,
                                 mimeType=zeep.xsd.Nil,
                                 name=doc_name,
                                 path=zeep.xsd.Nil,
                                 resourceInfoId=zeep.xsd.Nil,
                                 size=doc_size,
                                 type=resource_type)
    return resource_info


def create_target_info():
    print "entering create_target_info"
    # ns1:TargetInfo(dateRequested: ns1:Date, encoding: xsd:string, instructions: xsd:string, metadata: ns1:Metadata[],
    # priority: ns1:Priority, requestedDueDate: xsd:long, targetLocale: xsd:string,
    # workflowDefinitionTicket: xsd:string)
    prio_type = document_client.get_type('ns1:Priority')
    prio_wrap = xsd.Element('Priority', prio_type)
    prio_value = prio_wrap(name='', value=1)

    date_type = document_client.get_type('ns1:Date')
    date_wrap = xsd.Element('Date', date_type)
    date_value = date_wrap(critical=False, date=date_requested)

    target_info_array = []
    for lang in tgt_langs:
        target_type = document_client.get_type('ns1:TargetInfo')
        target_wrap = xsd.Element('TargetInfo', target_type)

        target_info = target_wrap(dateRequested=date_value,
                                  encoding='UTF-8',
                                  instructions=zeep.xsd.Nil,
                                  metadata=[],
                                  priority=prio_value,
                                  requestedDueDate=0,
                                  targetLocale=lang,
                                  workflowDefinitionTicket=zeep.xsd.Nil)
        target_info_array.append(target_info)
    return target_info_array


# Create services
session_client = zeep.Client(pd_url + '/wsdl/PDService2/SessionService2_4180.wsdl')
session_service = session_client.create_service('{http://impl.services2.service.ws.projectdirector.gs4tr.org}SessionService2Soap12Binding',
                                                pd_url + '/SessionService2_4180.SessionService2HttpSoap12Endpoint')

submission_client = zeep.Client(pd_url + '/wsdl/PDService2/SubmissionService2_4180.wsdl')
submission_service = submission_client.create_service('{http://impl.services2.service.ws.projectdirector.gs4tr.org}SubmissionService2Soap12Binding',
                                                      pd_url + '/SubmissionService2_4180.SubmissionService2HttpSoap12Endpoint')

workflow_client = zeep.Client(pd_url + '/wsdl/PDService2/WorkflowService2_4180.wsdl')
workflow_service = workflow_client.create_service('{http://impl.services2.service.ws.projectdirector.gs4tr.org}WorkflowService2Soap12Binding',
                                                  pd_url + '/WorkflowService2_4180.WorkflowService2HttpSoap12Endpoint')

project_client = zeep.Client(pd_url + '/wsdl/PDService2/ProjectService2_4180.wsdl')
project_service = project_client.create_service('{http://impl.services2.service.ws.projectdirector.gs4tr.org}ProjectService2Soap12Binding',
                                                  pd_url + '/ProjectService2_4180.ProjectService2HttpSoap12Endpoint')

document_client = zeep.Client(pd_url + '/wsdl/PDService2/DocumentService2_4180.wsdl')
document_service = document_client.create_service('{http://impl.services2.service.ws.projectdirector.gs4tr.org}DocumentService2Soap12Binding',
                                                  pd_url + '/DocumentService2_4180.DocumentService2HttpSoap12Endpoint')

target_client = zeep.Client(pd_url + '/wsdl/PDService2/TargetService2_4180.wsdl')
target_service = target_client.create_service('{http://impl.services2.service.ws.projectdirector.gs4tr.org}TargetService2Soap12Binding',
                                              pd_url + '/TargetService2_4180.TargetService2HttpSoap12Endpoint')

# Get the show on the road
try:
    # First, login
    token = session_service.login(username=pd_username, password=pd_password)
    print "Login token: " + token

    # Second, find project by short code
    project = project_service.findProjectByShortCode(projectShortCode=pd_shortcode, userId=token)
    print "Project ticket: " + project['ticket']
    project_ticket = project['ticket']

    # Third, send files one by one
    submission_ticket = None
    for f in file_list:
        submission_ticket = submit_document_with_binary_resource(f, token)
        print "after submission_ticket"

    # Fourth, start the submission
    # startSubmission(submissionId: xsd:string, submissionInfo: ns1:SubmissionInfo, userId: xsd:string)
    sub_info = create_submission_info(sub_name='Test_Submission_Python_1')
    sub = submission_service.startSubmission(submissionId=submission_ticket, submissionInfo=sub_info, userId=token)
    print "Submission ticket returned: " + sub

    # Finally, logout
    session_service.logout(token)
    print "Successfully logged out."

except zError as e:
    print "Something's wrong: " + e.message
