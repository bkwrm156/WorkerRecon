import config
import re
from datetime import datetime
global sysdate

#oracle format sysdate
sysdate = (datetime.today().strftime('%Y/%m/%d'))

#write temp files in order into final file with spaces
def writeHire():
    with open(config.finalfilespacespath, "w+") as final_file_spaces:
        global loglength_tempworker
        loglength_tempworker=0
        with open(config.tempworkerfilepath) as tempworker:
            for line in tempworker:
                final_file_spaces.write(line)
                loglength_tempworker=loglength_tempworker+1
        with open(config.temppersonnamefilepath) as tempperson:
            for line in tempperson:
                final_file_spaces.write(line)
        with open(config.temppersonemailfilepath) as tempemail:
            for line in tempemail:
                final_file_spaces.write(line)
        with open(config.temppersonlegislativesfilepath) as templegislative:
            for line in templegislative:
                final_file_spaces.write(line)
        with open(config.temppersonaddressfilepath) as tempaddress:
            for line in tempaddress:
                final_file_spaces.write(line)
        with open(config.tempworkrelationshipfilepath) as temprelationship:
            for line in temprelationship:
                final_file_spaces.write(line)
        with open(config.tempworktermsfilepath) as tempworkterms:
            for line in tempworkterms:
                final_file_spaces.write(line)
        with open(config.tempworkerassignmentfilepath) as tempworkassignment:
            for line in tempworkassignment:
                final_file_spaces.write(line)
        with open(config.temppersonuserinfofilepath) as tempuser:
            for line in tempuser:
                final_file_spaces.write(line)

#read final file with spaces
    with open(config.finalfilespacespath, 'r+') as final_file_spaces:
        lines = final_file_spaces.readlines()

    #remove RH's
    with open(config.finalfilepostregexpath, 'w+') as final_file_postregex:
        for line in lines:
            #line = re.sub(r"_RH\|", "|", line)
            final_file_postregex.write(line)
    with open(config.finalfilepostregexpath, 'r+') as final_file_postregex:
        lines = final_file_postregex.readlines()
    #write final file
    with open(config.finaldatfilepath, 'w+') as final_file:
        final_file.seek(0)
        final_file.writelines(line for line in lines if line.strip())
        final_file.truncate()

#full stack of 9 metadatas for rehire date updated
def writeRehireWithHireDatesUpdated():
    with open(config.finalfilespacespath, "w+") as final_file_spaces:
        with open(config.tempworkerfilepath) as tempworker:
            for line in tempworker:
                final_file_spaces.write(line)
        with open(config.temppersonnamefilepath) as tempperson:
            for line in tempperson:
                final_file_spaces.write(line)
        with open(config.temppersonemailfilepath) as tempemail:
            for line in tempemail:
                final_file_spaces.write(line)
        with open(config.temppersonlegislativesfilepath) as templegislative:
            for line in templegislative:
                final_file_spaces.write(line)
        with open(config.temppersonaddressfilepath) as tempaddress:
            for line in tempaddress:
                final_file_spaces.write(line)
        with open(config.tempworkrelationshipfilepath) as temprelationship:
            for line in temprelationship:
                final_file_spaces.write(line)
        with open(config.tempworktermsfilepath) as tempworkterms:
            for line in tempworkterms:
                final_file_spaces.write(line)
        with open(config.tempworkerassignmentfilepath) as tempworkassignment:
            for line in tempworkassignment:
                final_file_spaces.write(line)
        with open(config.temppersonuserinfofilepath) as tempuser:
            for line in tempuser:
                final_file_spaces.write(line)

    # read final file with spaces
    with open(config.finalfilespacespath, 'r+') as final_file_spaces:
        lines = final_file_spaces.readlines()
    #write final file
    with open(config.finaldatfilepath, 'w+') as final_file:
        final_file.seek(0)
        final_file.writelines(line for line in lines if line.strip())
        final_file.truncate()

#rehire. needs conversion to function and transfer of final file builds
def writeRehire():
    with open(config.finalfilespacespath, "w+") as final_file_spaces:
        with open(config.tempworkrelationshipfilepath) as temprelationship:
            for line in temprelationship:
                final_file_spaces.write(line)
        with open(config.tempworktermsfilepath) as tempworkterms:
            for line in tempworkterms:
                final_file_spaces.write(line)
        with open(config.tempworkerassignmentfilepath) as tempworkassignment:
            for line in tempworkassignment:
                final_file_spaces.write(line)

    # read final file with spaces
    with open(config.finalfilespacespath, 'r+') as final_file_spaces:
        lines = final_file_spaces.readlines()

    with open(config.finaldatfilepath, 'w+') as final_file:
        final_file.seek(0)
        final_file.writelines(line for line in lines if line.strip())
        final_file.truncate()

#asgchange. needs conversion to function. and transfer of final file builds
def writeAsgChangeForExpenses():
    with open(config.finalfilespacespath, "w+") as final_file_spaces:
        with open(config.temppersonaddressfilepath) as tempaddress:
            for line in tempaddress:
                final_file_spaces.write(line)
        with open(config.tempworktermsfilepath) as tempworkterms:
            for line in tempworkterms:
                final_file_spaces.write(line)
        with open(config.tempworkerassignmentfilepath) as tempworkassignment:
            for line in tempworkassignment:
                final_file_spaces.write(line)

    with open(config.finalfilespacespath, 'r+') as final_file_spaces:
        lines = final_file_spaces.readlines()

    addressdateupdate = "ADDRESS|" + str(sysdate) + "||"
    worktermsdateupdate = "Y|1|" + str(sysdate) + "|Y"
    assignmentdateupdate = "ASG_CHANGE|" + str(sysdate) + "||1"
    with open(config.finalfilepostregexpath, 'w+') as final_file_postregex:
        for line in lines:
            line = re.sub(r"Y\|ASG_CHANGE\|Home", "Y||Home", line)
            line = re.sub(r"ASG_CHANGE\|1\|Y\|", "|1|Y|", line)
            line = re.sub(r"ADDRESS\|\S{10}\|\|", addressdateupdate, line)
            line = re.sub(r"Y\|1\|\S{10}\|Y", worktermsdateupdate, line)
            line = re.sub(r"ASG_CHANGE\|\S{10}\|\|1", assignmentdateupdate, line)
            final_file_postregex.write(line)

    with open(config.finalfilepostregexpath, 'r+') as final_file_postregex:
        lines = final_file_postregex.readlines()

    with open(config.finaldatfilepath, 'w+') as final_file:
        final_file.seek(0)
        final_file.writelines(line for line in lines if line.strip())
        final_file.truncate()

# asgchange. needs conversion to function. and transfer of final file builds
def writeAsgChange():
        with open(config.finalfilespacespath, "w+") as final_file_spaces:
            with open(config.tempworktermsfilepath) as tempworkterms:
                for line in tempworkterms:
                    final_file_spaces.write(line)
            with open(config.tempworkerassignmentfilepath) as tempworkassignment:
                for line in tempworkassignment:
                    final_file_spaces.write(line)

        with open(config.finalfilespacespath, 'r+') as final_file_spaces:
            lines = final_file_spaces.readlines()

        with open(config.finalfilepostregexpath, 'w+') as final_file_postregex:
            for line in lines:
                line = re.sub(r"ASG_CHANGE\|1\|Y\|", "|1|Y|", line)
                final_file_postregex.write(line)

        with open(config.finalfilepostregexpath, 'r+') as final_file_postregex:
            lines = final_file_postregex.readlines()

        with open(config.finaldatfilepath, 'w+') as final_file:
            final_file.seek(0)
            final_file.writelines(line for line in lines if line.strip())
            final_file.truncate()


def writeTerm():
    termdateupdate = "|" + str(sysdate) + "|Y|"

    with open(config.finalfilespacespath, "w+") as final_file_spaces:
        with open(config.tempworkrelationshipfilepath) as tempworkrelationship:
            for line in tempworkrelationship:
                final_file_spaces.write(line)

    with open(config.finalfilespacespath, "r+") as final_file_spaces:
        lines = final_file_spaces.readlines()

    with open(config.finalfilepostregexpath, 'w+') as final_file_postregex:
        for line in lines:
            line = re.sub(r"_RH\|", "|", line)
            line = re.sub(r"Clinic\|\S{10}\|Y", "Clinic||Y", line)
            line = re.sub(r"\|\|\|", termdateupdate, line)
            final_file_postregex.write(line)
    with open(config.finalfilepostregexpath, 'r+') as final_file_postregex:
        lines = final_file_postregex.readlines()

    with open(config.finaldatfilepath, 'w+') as final_file:
        final_file.seek(0)
        final_file.writelines(line for line in lines if line.strip())
        final_file.truncate()

def writeHistoricalTerm():
    #termdateupdate = "|" + str(sysdate) + "|Y|"

    with open(config.finalfilespacespath, "w+") as final_file_spaces:
        with open(config.tempworkrelationshipfilepath) as tempworkrelationship:
            for line in tempworkrelationship:
                final_file_spaces.write(line)

    with open(config.finalfilespacespath, "r+") as final_file_spaces:
        lines = final_file_spaces.readlines()
        ####line=line.rstrip()

    with open(config.finalfilepostregexpath, 'w+') as final_file_postregex:
        for line in lines:
            #line = re.sub(r"_RH\|", "|", line)
            line = re.sub(r"Clinic\|\S{10}\|Y", "Clinic||Y", line)
            #line = re.sub(r"\|\|\|", termdateupdate, line)
            final_file_postregex.write(line)
    with open(config.finalfilepostregexpath, 'r+') as final_file_postregex:
        lines = final_file_postregex.readlines()

    with open(config.finaldatfilepath, 'w+') as final_file:
        final_file.seek(0)
        final_file.writelines(line for line in lines if line.strip())
        final_file.truncate()

def writeLogTempFiles():
    with open(config.finallogfilepath, "a+") as log:
        log.write("\n" + str(loglength_tempworker) + " records in tempworker")