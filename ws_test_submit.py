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
pd_url = 'https://qa-tdc13.translations.com/PD/services'
pd_shortcode = 'GEN000006'
src_lang = 'en-US'
tgt_langs = ['de-DE', 'fr-FR']
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
    file_size = os.path.getsize(os.path.join(file_path, file_name))
    res_info = create_resource_info(doc_name=file_name, doc_size=file_size)
    print "exited create_resource_info"
    with open(os.path.join(file_path, file_name), 'r') as source_doc:
        print "opened the file " + os.path.join(file_path, file_name)
        file_contents_64 = base64.b64encode(source_doc.read(), 'utf-8')
        print "----------- Begin document info -------------"
        print doc_info
        print "----------- End document info -------------"
        print "----------- Begin resource info -------------"
        print res_info
        print "----------- End resource info -------------"
        submit_document_response = document_service.submitDocumentWithBinaryResource(documentInfo=doc_info,
                                                                                     resourceInfo=res_info,
                                                                                     data=file_contents_64,
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
    prio = document_factory.Priority(value=1)
    date = document_factory.Date(date=int(str(time.time()+86400000).split('.')[0]))
    submission_info = document_factory.SubmissionInfo(additionalCosts='', autoStartChilds=False,
                                                      clientIdentifier=client_identifier, dateRequested=date,
                                                      internalNotes='', metadata=[], name=sub_name,
                                                      projectTicket=project_ticket, critical=False, priority=prio)
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
    datereq = document_factory.Date(date=date_requested)
    if submission_ticket is not None:
        document_info = document_factory.DocumentInfo(projectTicket=project_ticket, submissionTicket=submission_ticket,
                                                      sourceLocale=src_lang, name=doc_name,
                                                      instructions=doc_instructions, clientIdentifier=client_identifier,
                                                      targetInfos=tgt_infos, dateRequested=datereq)
    else:
        document_info = document_factory.DocumentInfo(projectTicket=project_ticket, sourceLocale=src_lang,
                                                      name=doc_name, instructions=doc_instructions,
                                                      clientIdentifier=client_identifier, targetInfos=tgt_infos,
                                                      dateRequested=datereq)

    return document_info


def create_resource_info(doc_name, doc_size):
    print "entering create_resource_info"
    # ns1:ResourceInfo(classifier: xsd:string, clientIdentifier: xsd:string, description: xsd:string,
    # encoding: xsd:string, md5Checksum: xsd:string, mimeType: xsd:string, name: xsd:string, path: xsd:string,
    # resourceInfoId: xsd:long, size: xsd:long, type: ns1:ResourceType)
    resource_info = document_factory.ResourceInfo(classifier=file_classifier, clientIdentifier=client_identifier,
                                                  name=doc_name, size=doc_size, encoding='UTF-8')
    return resource_info


def create_target_info():
    print "entering create_target_info"
    # ns1:TargetInfo(dateRequested: ns1:Date, encoding: xsd:string, instructions: xsd:string, metadata: ns1:Metadata[],
    # priority: ns1:Priority, requestedDueDate: xsd:long, targetLocale: xsd:string,
    # workflowDefinitionTicket: xsd:string)
    prio = document_factory.Priority(name='Low', value=0)
    target_info_array = []
    for lang in tgt_langs:
        target_info = document_factory.TargetInfo(targetLocale=lang, requestedDueDate=0, priority=prio, encoding='UTF-8')
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
document_factory = document_client.type_factory('ns1')

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
