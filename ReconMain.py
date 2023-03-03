#import modules
import pandas as pd
import recon_config as config


#create and/or import directories and files
# report from oracle
# full file from workday sandbox 

#read in full file
with open(config.fullfilepath, "r", encoding = "utf-8") as file_object:
    global full_file_lines
    full_file_lines = file_object.readlines()
    global log_length_of_fullfile
    log_length_of_fullfile = len(full_file_lines)
    for line in full_file_lines:

        if "|Assignment|" in line:
            config.fullfilecount_assignment=config.fullfilecount_assignment+1

#function to create temp file with parsed assignment header and data
def assignmentParseFromSBX():
    with open(config.tempworkerassignmentfilepath, "w") as workerassignmenttemp:
      workerassignmenttemp.write("METADATA|Assignment|SourceSystemOwner|SourceSystemId|ActionCode|EffectiveStartDate|EffectiveEndDate|EffectiveSequence|EffectiveLatestChange|WorkTermsAssignmentId(SourceSystemId)|AssignmentStatusTypeCode|PersonTypeCode|BusinessUnitShortCode|LocationCode|JobCode|PrimaryAssignmentFlag|DefaultExpenseAccount|ExpenseCheckSendToAddress|GradeCode\n")

    # parsed assignment write to temp file
    for line in full_file_lines:
        if "|Assignment|WORKDAY|" in line:
            with open(config.tempworkerassignmentfilepath, "a") as assignmenttemp:
                assignmenttemp.write(line)

#assignmentParseFromSBX()

#sbx assignment temp  to dataframe, columns dropped, column names matched
df_sbx_asg = pd.read_csv(config.tempworkerassignmentfilepath, sep="|")
#print("This is df of the parsed SBX file\n")
#print(df_sbx_asg.head())

df_sbx_asg.drop(columns=["METADATA","Assignment","SourceSystemOwner","ActionCode","EffectiveStartDate","EffectiveEndDate","EffectiveSequence","EffectiveLatestChange","WorkTermsAssignmentId(SourceSystemId)","AssignmentStatusTypeCode","BusinessUnitShortCode","LocationCode","PrimaryAssignmentFlag","ExpenseCheckSendToAddress","GradeCode"], axis=1, inplace=True)
#print("This is df of the parsed SBX file, columns dropped\n")
#print(df_sbx_asg.head())

df_sbx_asg[['WORKDAY','PERSON_NUMBER','ASG','RH']] = df_sbx_asg.SourceSystemId.apply(lambda x: pd.Series(str(x).split("_")))
#print("DF modified with SSID parsed\n")
#print(df_sbx_asg.head())

df_sbx_asg.drop(columns=["SourceSystemId","WORKDAY","ASG"], axis=1, inplace=True)
#print("DF modified with  columns dropped\n")
#print(df_sbx_asg.head())

new_asgcolumns = ["PERSON_NUMBER","RH","PersonTypeCode","JobCode","DefaultExpenseAccount"]
df_sbx_asg=df_sbx_asg[new_asgcolumns]
#print("\nDF modified columns rearranged\n")
#print(df_sbx_asg.head())

df_sbx_asg.rename(columns={'PersonTypeCode': 'USER_PERSON_TYPE', 'JobCode': 'JOB_CODE', 'DefaultExpenseAccount' :'DEFAULT_ACCOUNT'}, inplace = True)
#print("\nColumns renamed\n")
print(df_sbx_asg.head())

#read in report from oracle into dataframe
#create dataframe (then csv) for each use case
#removed index col due to none of the key are in the axis name
df_recon_report = pd.read_excel(config.reconfilepath)
#df_recon_report = pd.read_excel(config.reconfilepath)

#df_recon_report.rename(columns = {'0': 'PERSON_NUMBER','1': 'EMP_STATUS','2':'RH','3':'USERNAME','4':'EMAIL_ADDRESS','5':'FULL_NAME','6':'USER_PERSON_TYPE','7':'WR_SSID','8':'LEGAL_EMPLOYER','9':'DEFAULT_ACCOUNT','10':'JOB_CODE','11':'BUSINESS_UNIT','12':'MANAGER_NAME','13':'MANAGER_PERSON_NUMBER','14':'MANAGER_EMAIL','15':'MANAGER_STATUS'}, inplace=True)
#print(df_recon_report.head())
#df_recon_report.drop(0,inplace=True)
print(df_recon_report.head())

df_recon_report.to_csv(config.tempreconpd)

#print(df_sbx_asg.index)
#print(df_recon_report.index)
#print(df_recon_report.index)

df_eid_match = pd.merge(df_sbx_asg, df_recon_report[['PERSON_NUMBER', 'EMP_STATUS']], on = 'PERSON_NUMBER', how = 'left')
print(df_eid_match.head())
df_eid_match.to_csv(config.eid_match)
#vlookup in python per use case

#create csv file from vlookup dataframe


