# import modules
import re
import os
import glob
import config

def buildLookupLists():
    # read in full file
    #added encoding param on 8/22 due to historical errors for Evan (, encoding = "utf-8")
    with open(config.fullfilepath, "r", encoding = "utf-8") as file_object:
        global full_file_lines
        full_file_lines = file_object.readlines()
        global log_length_of_fullfile
        log_length_of_fullfile = len(full_file_lines)
        for line in full_file_lines:
            if "MERGE|Worker" in line:
                config.fullfilecount_worker=config.fullfilecount_worker+1
            if "MERGE|PersonName" in line:
                config.fullfilecount_personname=config.fullfilecount_personname+1
            if "MERGE|PersonEmail" in line:
                config.fullfilecount_personemail=config.fullfilecount_personemail+1
            if "MERGE|PersonLegislativeData" in line:
                config.fullfilecount_personlegislativedata=config.fullfilecount_personlegislativedata+1
            if "MERGE|PersonAddress" in line:
                config.fullfilecount_personaddress=config.fullfilecount_personaddress+1
            if "MERGE|WorkRelationship" in line:
                config.fullfilecount_workrelationship=config.fullfilecount_workrelationship+1
            if "MERGE|WorkTerms" in line:
                config.fullfilecount_workterms=config.fullfilecount_workterms+1
            if "MERGE|Assignment" in line:
                config.fullfilecount_assignment=config.fullfilecount_assignment+1
            if "MERGE|PersonUserInformation" in line:
                config.fullfilecount_personuserinformation=config.fullfilecount_personuserinformation+1

    # read in the to be lookup file and create EID underscored format
    global eid_list_underscored
    eid_list_underscored = []
    with open(config.lookupfilepath, "r") as employee_id_file:
        employee_ids = employee_id_file.readlines()
        global log_length_of_lookupfile
        log_length_of_lookupfile=len(employee_ids)
        for employee_id in employee_ids:
            employee_id = employee_id.rstrip()
            eid_string = "_" + str(employee_id) + "_"
            eid_list_underscored.append(eid_string)
        numofunderscoredemp = len(employee_ids)



    # read in the to be lookup file and create EID piped format
    global eid_list_pipe
    eid_list_pipe = []
    with open(config.lookupfilepath, "r") as employee_id_file_pipe:
        employee_ids_pipe = employee_id_file_pipe.readlines()
        for employee_id_pipe in employee_ids_pipe:
            employee_id_pipe = employee_id_pipe.rstrip()
            eid_string_pipe = "|" + str(employee_id_pipe) + "|"
            eid_list_pipe.append(eid_string_pipe)

def writeLogLookupFiles():
    with open(config.finallogfilepath, "w+") as log:
        log.write("Length of full file is: " + str(log_length_of_fullfile))
        log.write("\n\nNumber of WORKER records in the full file is: "+str(config.fullfilecount_worker))
        log.write("\nNumber of PERSONNAME records in the full file is: " + str(config.fullfilecount_personname))
        log.write("\nNumber of PERSONEMAIL records in the full file is: " + str(config.fullfilecount_personemail))
        log.write("\nNumber of PERSONLEGISLATIVEDATA records in the full file is: " + str(config.fullfilecount_personlegislativedata))
        log.write("\nNumber of PERSONADDRESS records in the full file is: " + str(config.fullfilecount_personaddress))
        log.write("\nNumber of WORKRELATIONSHIP records in the full file is: " + str(config.fullfilecount_workrelationship))
        log.write("\nNumber of WORKTERMS records in the full file is: " + str(config.fullfilecount_workterms))
        log.write("\nNumber of ASSIGNMENT records in the full file is: " + str(config.fullfilecount_assignment))
        log.write("\nNumber of PERSONUSERINFORMATION records in the full file is: " +str(config.fullfilecount_personuserinformation))
        log.write("\n\nNumber of employee IDs in lookup are: " + str(log_length_of_lookupfile))

#main parsing loop for HIRE
def parsingHire():

    #open temp files and write metadatas for HIRE files
    with open(config.tempworkerfilepath, "w") as workertemp:
        workertemp.write(
            "METADATA|Worker|SourceSystemOwner|SourceSystemId|EffectiveStartDate|EffectiveEndDate|PersonNumber|StartDate|ActionCode\n")
    with open(config.temppersonnamefilepath, "w") as personnametemp:
        personnametemp.write(
            "METADATA|PersonName|SourceSystemOwner|SourceSystemId|PersonId(SourceSystemId)|EffectiveStartDate|EffectiveEndDate|LegislationCode|NameType|FirstName|MiddleNames|LastName\n")
    with open(config.temppersonemailfilepath, "w") as personemailtemp:
        personemailtemp.write(
            "METADATA|PersonEmail|SourceSystemOwner|SourceSystemId|PersonId(SourceSystemId)|DateFrom|EmailType|EmailAddress|PrimaryFlag\n")
    with open(config.temppersonlegislativesfilepath, "w") as personlegislativedatatemp:
        personlegislativedatatemp.write(
            "METADATA|PersonLegislativeData|SourceSystemOwner|SourceSystemId|PersonId(SourceSystemId)|EffectiveStartDate|EffectiveEndDate|LegislationCode|Sex\n")
    with open(config.temppersonaddressfilepath, "w") as personaddresstemp:
        personaddresstemp.write("METADATA|PersonAddress|SourceSystemOwner|SourceSystemId|EffectiveStartDate|EffectiveEndDate|PersonId(SourceSystemId)|AddressType|AddressLine1|AddressLine2|AddressLine3|AddressLine4|TownOrCity|Region1|Region2|Region3|Country|PostalCode|PrimaryFlag\n")
        #old headers personaddresstemp.write("METADATA|PersonAddress|SourceSystemOwner|SourceSystemId|EffectiveStartDate|EffectiveEndDate|PersonId(SourceSystemId)|AddressType|AddressLine1|AddressLine2|TownOrCity|Region2|Region3|PostalCode|Country|PrimaryFlag\n")
    with open(config.tempworkrelationshipfilepath, "w") as workrelationshiptemp:
        workrelationshiptemp.write(
            "METADATA|WorkRelationship|SourceSystemOwner|SourceSystemId|PersonId(SourceSystemId)|ActualTerminationDate|TerminateWorkRelationshipFlag|LegalEmployerName|DateStart|PrimaryFlag|WorkerType|NewStartDate|ActionCode|ReasonCode\n")
    with open(config.tempworktermsfilepath, "w") as worktermstemp:
        worktermstemp.write(
            "METADATA|WorkTerms|ActionCode|SourceSystemOwner|SourceSystemId|PeriodOfServiceId(SourceSystemId)|EffectiveEndDate|EffectiveLatestChange|EffectiveSequence|EffectiveStartDate|PrimaryWorkTermsFlag\n")
    with open(config.tempworkerassignmentfilepath, "w") as workerassignmenttemp:
        workerassignmenttemp.write("METADATA|Assignment|SourceSystemOwner|SourceSystemId|ActionCode|EffectiveStartDate|EffectiveEndDate|EffectiveSequence|EffectiveLatestChange|WorkTermsAssignmentId(SourceSystemId)|AssignmentStatusTypeCode|PersonTypeCode|BusinessUnitShortCode|LocationCode|JobCode|PrimaryAssignmentFlag|DefaultExpenseAccount|ExpenseCheckSendToAddress|GradeCode\n")
    with open(config.temppersonuserinfofilepath, "w") as personuserinformationtemp:
        personuserinformationtemp.write(
            "METADATA|PersonUserInformation|PersonNumber|UserName|StartDate|UsernameMatchingFlag|EmailMatchingFlag|EmailAddress|CreateUserIfNoMatchingEmailFlag\n")

    #parsing loops for worker and personinformation for HIRE
    for employee_id_pipe in eid_list_pipe:
        # HIRE Worker loop needs HIRE action
        for line in full_file_lines:
            if employee_id_pipe in line[41:58] and "Worker|" in line:
                linestrip=line.strip()
                baseline = linestrip + "HIRE"
                # sliced_worker_line=re.sub(r"Terms\|","Terms|HIRE",line)
                # print(sliced_workterms_line)
                with open(config.tempworkerfilepath, "a") as workertemp:
                    workertemp.write(baseline + "\n")
        #            wt_hire_count=wt_hire_count+1
        #        print("WT hire count is " + str(wt_hire_count))

        # HIRE personuserinformation loop
        for line in full_file_lines:
            if employee_id_pipe in line[27:37] and "PersonUserInformation" in line:
                with open(config.temppersonuserinfofilepath, "a") as personuserinformationtemp:
                    personuserinformationtemp.write(line)

    # main parsing loop for HIRE EID underscored
    for emp_id in eid_list_underscored:

        # HIRE Personname loop
        for line in full_file_lines:
            if emp_id in line[27:45] and "PersonName" in line:
                config.tempfilecount_personname=config.tempfilecount_personname+1
                with open(config.temppersonnamefilepath, "a") as personnametemp:
                    personnametemp.write(line)

        # HIRE Personemail loop
        for line in full_file_lines:
            if emp_id in line[27:44] and "PersonEmail" in line:
                with open(config.temppersonemailfilepath, "a") as personemailtemp:
                    personemailtemp.write(line)

        # HIRE personlegislative loop
        for line in full_file_lines:
            if emp_id in line[37:55] and "PersonLegislativeData" in line:
                with open(config.temppersonlegislativesfilepath, "a") as personlegislativedatatemp:
                    personlegislativedatatemp.write(line)

        # HIRE personaddress loop
        for line in full_file_lines:
            if emp_id in line[29:51] and "PersonAddress" in line:
                with open(config.temppersonaddressfilepath, "a") as personaddresstemp:
                    personaddresstemp.write(line)

        # HIRE workrelationship loop needs HIRE action
        for line in full_file_lines:
            if emp_id in line[32:49] and "WorkRelationship" in line:
                sliced_workrelationship_line = re.sub(r"E\|\|\|", "E||HIRE|", line)
                with open(config.tempworkrelationshipfilepath, "a") as workrelationshiptemp:
                    workrelationshiptemp.write(sliced_workrelationship_line)

        # HIRE workterms loop needs HIRE action
        for line in full_file_lines:
            if emp_id in line[30:50] and "WorkTerms" in line:
                sliced_workterms_line = re.sub(r"WorkTerms\|\|", "WorkTerms|HIRE|", line)
                with open(config.tempworktermsfilepath, "a") as worktermstemp:
                    worktermstemp.write(sliced_workterms_line)

        # HIRE assignment loop needs HIRE action
        for line in full_file_lines:
            if emp_id in line[30:46] and "Assignment" in line:
                line = re.sub(r"\|\|", "|HIRE|", line)
                line = re.sub (r"\|HIRE\|1\|Y\|", "||1|Y|", line)
                with open(config.tempworkerassignmentfilepath, "a") as assignmenttemp:
                    assignmenttemp.write(line)

#main parsing loop for ASGCHANGE expenses. no lookup
def parsingASGChangeExpense():
    with open(config.temppersonaddressfilepath, "w") as personaddresstemp:
        personaddresstemp.write("METADATA|PersonAddress|SourceSystemOwner|SourceSystemId|EffectiveStartDate|EffectiveEndDate|PersonId(SourceSystemId)|AddressType|AddressLine1|AddressLine2|AddressLine3|AddressLine4|TownOrCity|Region1|Region2|Region3|Country|PostalCode|PrimaryFlag\n")
    with open(config.tempworktermsfilepath, "w") as worktermstemp:
        worktermstemp.write(
            "METADATA|WorkTerms|ActionCode|SourceSystemOwner|SourceSystemId|PeriodOfServiceId(SourceSystemId)|EffectiveEndDate|EffectiveLatestChange|EffectiveSequence|EffectiveStartDate|PrimaryWorkTermsFlag\n")
    with open(config.tempworkerassignmentfilepath, "w") as workerassignmenttemp:
        workerassignmenttemp.write("METADATA|Assignment|SourceSystemOwner|SourceSystemId|ActionCode|EffectiveStartDate|EffectiveEndDate|EffectiveSequence|EffectiveLatestChange|WorkTermsAssignmentId(SourceSystemId)|AssignmentStatusTypeCode|PersonTypeCode|BusinessUnitShortCode|LocationCode|JobCode|PrimaryAssignmentFlag|DefaultExpenseAccount|ExpenseCheckSendToAddress|GradeCode\n")
    with open(config.fullfilepath, "r+") as fullfileasgchange:
        full_asg_lines = fullfileasgchange.readlines()

    #personaddress loop for asg change
    for line in full_asg_lines:
        if "WORKDAY" in line and "PersonAddress" in line:
            with open(config.temppersonaddressfilepath, "a") as personaddresstemp:
                personaddresstemp.write(line + "\n")

    #workterms loop needs ASG_CHANGE action code
    for line in full_asg_lines:
        if "WORKDAY"in line and "WorkTerms" in line:
            sliced_workterms_line = re.sub(r"WorkTerms\|\|", "WorkTerms|ASG_CHANGE|", line)
            with open(config.tempworktermsfilepath, "a") as worktermstemp:
                worktermstemp.write(sliced_workterms_line + "\n")

    #assignment loop needs ASG_CHANGE action code
    for line in full_asg_lines:
        if "WORKDAY" in line and "Assignment" in line:
            sliced_assignment_line = re.sub(r"\|\|", "|ASG_CHANGE|", line)
            with open(config.tempworkerassignmentfilepath, "a") as assignmenttemp:
                assignmenttemp.write(sliced_assignment_line + "\n")

def parsingREHire():
    with open(config.tempworkrelationshipfilepath, "w") as workrelationshiptemp:
        workrelationshiptemp.write(
            "METADATA|WorkRelationship|SourceSystemOwner|SourceSystemId|PersonId(SourceSystemId)|ActualTerminationDate|TerminateWorkRelationshipFlag|LegalEmployerName|DateStart|PrimaryFlag|WorkerType|NewStartDate|ActionCode|ReasonCode\n")
    with open(config.tempworktermsfilepath, "w") as worktermstemp:
        worktermstemp.write(
            "METADATA|WorkTerms|ActionCode|SourceSystemOwner|SourceSystemId|PeriodOfServiceId(SourceSystemId)|EffectiveEndDate|EffectiveLatestChange|EffectiveSequence|EffectiveStartDate|PrimaryWorkTermsFlag\n")
    with open(config.tempworkerassignmentfilepath, "w") as workerassignmenttemp:
        workerassignmenttemp.write(
            "METADATA|Assignment|SourceSystemOwner|SourceSystemId|ActionCode|EffectiveStartDate|EffectiveEndDate|EffectiveSequence|EffectiveLatestChange|WorkTermsAssignmentId(SourceSystemId)|AssignmentStatusTypeCode|PersonTypeCode|BusinessUnitShortCode|LocationCode|JobCode|PrimaryAssignmentFlag|DefaultExpenseAccount|ExpenseCheckSendToAddress|GradeCode\n")

    # main parsing loop for underscored employee IDS
    for emp_id in eid_list_underscored:

        # REHIRE workrelationship loop needs REHIRE action
        for line in full_file_lines:
            if emp_id in line[32:49] and "WorkRelationship" in line:
                sliced_workrelationship_line = re.sub(r"E\|\|\|", "E||REHIRE|", line)
                with open(config.tempworkrelationshipfilepath, "a") as workrelationshiptemp:
                    workrelationshiptemp.write(sliced_workrelationship_line + "\n")

        # REHIRE workterms loop needs REHIRE action
        for line in full_file_lines:
            if emp_id in line[30:50] and "WorkTerms" in line:
                sliced_workterms_line = re.sub(r"WorkTerms\|\|", "WorkTerms|REHIRE|", line)
                with open(config.tempworktermsfilepath, "a") as worktermstemp:
                    worktermstemp.write(sliced_workterms_line + "\n")

        # REHIRE assignment loop needs REHIRE action
        for line in full_file_lines:
            if emp_id in line[30:46] and "Assignment" in line:
                sliced_assignment_line = re.sub(r"H\|\|", "H|REHIRE|", line)
                with open(config.tempworkerassignmentfilepath, "a") as assignmenttemp:
                    assignmenttemp.write(sliced_assignment_line + "\n")

def parsingTerm():
    # create temp files
    with open(config.tempworkrelationshipfilepath, "w") as workrelationshiptemp:
        workrelationshiptemp.write(
            "METADATA|WorkRelationship|SourceSystemOwner|SourceSystemId|PersonId(SourceSystemId)|ActualTerminationDate|TerminateWorkRelationshipFlag|LegalEmployerName|DateStart|PrimaryFlag|WorkerType|NewStartDate|ActionCode|ReasonCode\n")

    # main parsing loop for underscored employee IDS
    for emp_id in eid_list_underscored:

        #workrelationship loop needs RESIGNATION action
        for line in full_file_lines:
            if emp_id in line[32:49] and "WorkRelationship" in line:
                sliced_workrelationship_line = re.sub(r"E\|\|\|", "E||RESIGNATION|", line)
                with open(config.tempworkrelationshipfilepath, "a") as workrelationshiptemp:
                    workrelationshiptemp.write(sliced_workrelationship_line + "\n")

def parsingASGChange():
    with open(config.tempworktermsfilepath, "w") as worktermstemp:
        worktermstemp.write(
            "METADATA|WorkTerms|ActionCode|SourceSystemOwner|SourceSystemId|PeriodOfServiceId(SourceSystemId)|EffectiveEndDate|EffectiveLatestChange|EffectiveSequence|EffectiveStartDate|PrimaryWorkTermsFlag\n")
    with open(config.tempworkerassignmentfilepath, "w") as workerassignmenttemp:
        #this is current expense test code metadatas
        # workerassignmenttemp.write(
        workerassignmenttemp.write("METADATA|Assignment|SourceSystemOwner|SourceSystemId|ActionCode|EffectiveStartDate|EffectiveEndDate|EffectiveSequence|EffectiveLatestChange|WorkTermsAssignmentId(SourceSystemId)|AssignmentStatusTypeCode|PersonTypeCode|BusinessUnitShortCode|LocationCode|JobCode|PrimaryAssignmentFlag|DefaultExpenseAccount|ExpenseCheckSendToAddress|GradeCode\n")
    # main parsing loop for HIRE EID underscored
    for emp_id in eid_list_underscored:

        # workterms loop needs ASG_CHANGE action code
        for line in full_file_lines:
            if emp_id in line[30:50] and "WorkTerms" in line:
                sliced_workterms_line = re.sub(r"WorkTerms\|\|", "WorkTerms|ASG_CHANGE|", line)
                with open(config.tempworktermsfilepath, "a") as worktermstemp:
                    worktermstemp.write(sliced_workterms_line + "\n")

        # assignment loop needs ASG_CHANGE action code
        for line in full_file_lines:
            if emp_id in line[30:50] and "Assignment" in line:
                sliced_assignment_line = re.sub(r"\|\|", "|ASG_CHANGE|", line)
                with open(config.tempworkerassignmentfilepath, "a") as assignmenttemp:
                    assignmenttemp.write(sliced_assignment_line + "\n")

def parsingHistoricalTerm():
    # create temp files
    with open(config.tempworkrelationshipfilepath, "w") as workrelationshiptemp:
        workrelationshiptemp.write(
            "METADATA|WorkRelationship|SourceSystemOwner|SourceSystemId|PersonId(SourceSystemId)|ActualTerminationDate|TerminateWorkRelationshipFlag|LegalEmployerName|DateStart|PrimaryFlag|WorkerType|NewStartDate|ActionCode|ReasonCode\n")

    # main parsing loop for underscored employee IDS
    for emp_id in eid_list_underscored:

        #workrelationship loop needs RESIGNATION action
        for line in full_file_lines:
            if emp_id in line[32:49] and "WorkRelationship" in line:
                sliced_workrelationship_line = re.sub(r"E\|\|\|", "E||RESIGNATION|", line)
                with open(config.tempworkrelationshipfilepath, "a") as workrelationshiptemp:
                    workrelationshiptemp.write(sliced_workrelationship_line + "\n")


def writeTempFileCountsToLog():
    with open(config.finallogfilepath, "a+") as log:
        log.write("\nNumber of temp lines written for PERSONNAME is: " +str(config.tempfilecount_personname))
