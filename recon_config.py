import os

#counts
fullfilecount_assignment=0


#number of worker lines created
#tempfilecount_worker=0
#tempfilecount_personname=0


#relative paths
#lookupfilepath = os.path.relpath("Lookup/Lookup.txt")
fullfilepath = os.path.relpath("FullFile/FullFile.dat")
reconfilepath = os.path.relpath("ReconReport/Recon.xlsx")


tempfilepath = os.path.relpath("TempFiles")
#tempworkerfilepath = os.path.relpath("TempFiles/1workertemp.txt")
tempworkerassignmentfilepath = os.path.relpath("TempFiles/parsedassignment.csv")
tempreconpd = os.path.relpath("TempFiles/ReconTempPD.csv")
eid_match = os.path.relpath("TempFiles/EIDlookupSBXtoReconReport.csv")

finalfilepath = os.path.relpath("FinalFiles")
finaleidcsv = os.path.relpath("FinalFiles/EID.csv")
#finalfilespacespath = os.path.relpath("FinalFiles/final_file_spaces.dat")
#finallogfilepath=os.path.relpath("FinalFiles/Log.txt")
