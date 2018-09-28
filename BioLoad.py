# BioLoad By Vasco Varas

# Imports
#region
import sys
import os
import subprocess
from os import listdir
from os.path import isfile, join
from pathlib import Path
import math
import mysql.connector
import getpass
#endregion

# Variables
#region
db_name = "db_bioload"
db_tara_table_name = "tb_taraPCs"
db_prots_table_name = "tb_prots"

db_host = "localhost"
db_user = "root"
db_passwd=""
db_auth_plugin="mysql_native_password"
db_port=3306

tb_virS = "tb_virs";
tb_Tov = "tb_tov";
tb_info = "tb_info";

tb_virS_index = "idx_virs";
tb_Tov_index = "idx_tov";
tb_info_index = "idx_info";

Version = "V1.0.0"
#endregion

def bestFileName(FileName):
    if not os.path.exists(FileName) and os.path.isfile(FileName):
        return FileName
    else:
        ind = 1;
        while os.path.exists(FileName + "_" + str(ind)) and os.path.isfile(FileName + "_" + str(ind)):
            ind += 1
        return FileName + "_" + str(ind)

def stringtowrite(protein, eklist, pkey):
    writestring = ""

    sql = "SELECT * FROM " + tb_Tov + " WHERE proteins LIKE '" + protein + "'"
    mycursor.execute(sql)
    cluster = mycursor.fetchone()

    sql = "SELECT * FROM " + tb_info + " WHERE pkey LIKE '" + pkey + "'"
    mycursor.execute(sql)
    info = mycursor.fetchone()
    
    if(cluster is not None and info is not None):
        for i in range(0, eklist.__len__()):
            writestring += eklist[i]
            if(i < eklist.__len__()):
                writestring += ","
        writestring += cluster[1] + "\t"
        writestring += protein + "\t"
        for i in range(1, info.__len__()):
            writestring += info[i].strip("\n")
            if(i < info.__len__()):
                writestring += "\t"

    return (writestring)

if len(sys.argv) < 3:
    print("BioLoad Suite " + Version + " by Vasco Varas")
    print("Usage: python BioLoad.py <Tara PCs> <info file> [Protein Clusters... (CD-HIT Output)]")
else:
    if (os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1])) and (os.path.exists(sys.argv[2]) and os.path.isfile(sys.argv[2])):
        # User input
        #region
        print("BioLoad " + Version + " by Vasco Varas")
        
        print('Please enter the DataBase ip: (leave empty for '+db_host + ")")
        print('>', end='')
        new_db_host = input();
        if new_db_host != "":
            db_host = new_db_host
        
        print('Please enter the DataBase port: (leave empty for '+str(db_port) + ")")
        print('>', end='')
        new_db_port = input();
        if new_db_port != "":
            db_port = new_db_port
        
        print('Please enter the DataBase User: (leave empty for ' + str(db_user) + ')')
        print('>', end='')
        new_db_user = input();
        if new_db_user != "":
            db_user = new_db_user
        
        print('DataBase Password: (Input is hidden!)')
        print('>', end='')
        db_passwd = pw = getpass.getpass()
        
        #print('Please enter DataBase auth_plugin: (leave empty for '+db_auth_plugin + ')')
        #print('>', end='')
        #new_db_auth_plugin = input();
        #if new_db_auth_plugin != "":
        #    db_auth_plugin = new_db_auth_plugin
        
        print("")
        print("")
        print("")
        print("")
        #endregion

        # MYSQL Setup
        # region
        # Log to MySQL Server
        print("Logging into MySQL Server")
        mydb = mysql.connector.connect(
        host=db_host,
        user=db_user,
        passwd=db_passwd,
        auth_plugin=db_auth_plugin,
        port=db_port
        )
        mycursor = mydb.cursor()

        print('Delete and re-create previous databases? (y/n):')
        reCreatedb = input();
        print('Delete and re-create previous CD-HIT database? (y/n):')
        reCreatedbcdhit = input();

        # Delete database if exists
        if(reCreatedb == "y"):
            print("Deleting database \"" + db_name + "\" if exists")
            mycursor.execute("DROP DATABASE IF EXISTS " + db_name)

        # create database
        if(reCreatedb == "y"):
            print("Creating \"" + db_name + "\"");
            mycursor.execute("CREATE DATABASE " + db_name)

        print("Using \"" + db_name + "\" database")

        mycursor.execute("USE " + db_name)

        #Create table
        if(reCreatedb == "y"):
            # Create tara table
            print("Creating table \""+tb_Tov+"\" into database \"" + db_name + "\"")
            mycursor.execute("CREATE TABLE "+ tb_Tov +" (proteins VARCHAR(255), cluster VARCHAR(255))")
            # Create VirS table
            print("Creating table \""+tb_virS+"\" into database \"" + db_name + "\"")
            mycursor.execute("CREATE TABLE "+ tb_virS +" (proteins VARCHAR(255), ekproteins VARCHAR(255), ercluster VARCHAR(255), pkey VARCHAR(255))")
            # Create infofile table
            print("Creating table \""+tb_info+"\" into database \"" + db_name + "\"")
            mycursor.execute("CREATE TABLE "+ tb_info +
                " (pkey VARCHAR(255), " + 
                "depth VARCHAR(255), "+
                "region VARCHAR(255), "+
                "temperature VARCHAR(255), "+
                "salinity VARCHAR(255), "+
                "oxygen VARCHAR(255), "+
                "chlorophyl VARCHAR(255), "+
                "nitrite VARCHAR(255), "+
                "phosphate VARCHAR(255), "+
                "nitrite_nitrate VARCHAR(255), "+
                "silica VARCHAR(255), "+
                "synechococcus VARCHAR(255), "+
                "prochlorococcus VARCHAR(255), "+
                "bacteria VARCHAR(255), "+
                "low_dna_bacteria VARCHAR(255), "+
                "high_dna_bacteria VARCHAR(255), "+
                "high_dna_bacteria_pers VARCHAR(255))")


        nfClusters = 0

        if(reCreatedb == "y"):
            # Read and add TARA PCs into the database
            print("Adding TARA PCs into the database")
            TaraPCs = open(sys.argv[1], "r")
            TaraLines = TaraPCs.readlines()
            TaraLen = TaraLines.__len__() - 1
            TaraPCs.close()

            count = 0
            clustername = "";
            sql = "INSERT INTO " + tb_Tov + " (proteins, cluster) VALUES (%s, %s)"

            while(count < TaraLen):
                if(">" in TaraLines[count]):
                    clustername = TaraLines[count][1:-2].split("\t")[0]
                else:
                    val = (TaraLines[count][:-1], clustername)
                    mycursor.execute(sql, val)
                count += 1
                if count % 50000 == 0:
                    print(str(math.floor((float(count) / float(TaraLen)) * 100.0)) + "%" + " ("+str(count)+"/" + str(TaraLen) + ")")
            print("Commiting to database")
            mydb.commit()
            TaraPCs.close()
            TaraLines = ""
            print("Done Adding TARA PCs to the database")




            # Read and add info into the database
            print("Adding Info file into the database")
            InfoFile = open(sys.argv[2], "r")
            InfoLines = InfoFile.readlines()
            InfoLen = InfoLines.__len__() - 1

            count = 0
            clustername = "";
            sql = "INSERT INTO " + tb_info + " ("
            sql += "pkey, "
            sql += "depth, "
            sql += "region, "
            sql += "temperature, "
            sql += "salinity, "
            sql += "oxygen, "
            sql += "chlorophyl, "
            sql += "nitrite, "
            sql += "phosphate, "
            sql += "nitrite_nitrate, "
            sql += "silica, "
            sql += "synechococcus, "
            sql += "prochlorococcus, "
            sql += "bacteria, "
            sql += "low_dna_bacteria, "
            sql += "high_dna_bacteria, "
            sql += "high_dna_bacteria_pers"
            sql += ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            
            while(count < InfoLen):
                wl = InfoLines[count].split("\t")
                val = (wl[1][5:].lstrip('0').replace("_","").replace("SRF","SUR"), wl[8], wl[10], wl[12], wl[13], wl[14], wl[15], wl[16], wl[17], wl[18], wl[19], wl[20], wl[21], wl[22], wl[23], wl[24], wl[25])
                mycursor.execute(sql, val)
                count += 1
                if count % 10 == 0:
                    print(str(math.floor((float(count) / float(InfoLen)) * 100.0)) + "%" + " ("+str(count)+"/" + str(InfoLen) + ")")
            print("Commiting to database")
            mydb.commit()
            InfoFile.close()
            InfoLines = ""
            print("Done Adding Info file to the database")
	
        if(reCreatedbcdhit == "y"):
            # Read and add all PCs into the database
            print("Adding PCs into the database")
            readingfile = 3
            while readingfile < sys.argv.__len__():
                print("Adding \"" + sys.argv[readingfile] + "\" PCs into the database")
                usefile = open(sys.argv[readingfile], "r")
                useLines = usefile.readlines()
                useLen = useLines.__len__() - 1
                usefile.close()

                count = 0
                clustername = "";
                sql = "INSERT INTO " + tb_virS + " ("
                sql += "proteins, "
                sql += "ekproteins, "
                sql += "ercluster, "
                sql += "pkey"
                sql += ") VALUES (%s, %s, %s, %s)"
            
                while(count < useLen):
                    wl = useLines

                    if "Cluster" in wl[count]:
                        cluster = wl[count][1:-1]
                        count += 1
                        
                        prot = wl[count].split(">")[1][:-6]
                        count += 1

                        if "Cluster" not in wl[count]:
                            while("Cluster" not in wl[count]):
                                ekprot = wl[count].split(">")[1].split(".")[0]
                                val = (prot, ekprot, sys.argv[readingfile].split(".")[0] + "_" + cluster, (prot.split("_")[0]).lstrip('0'))
                                mycursor.execute(sql, val)
                                count += 1

                    count += 1
                    if count % 10000 == 0:
                        print(str(math.floor((float(count) / float(useLen)) * 100.0)) + "%" + " ("+str(count)+"/" + str(useLen) + ")")
                readingfile += 1
            print("Commiting to database")
            mydb.commit()
            print("Done Adding PCs to the database")


            # Index databases
            print("Indexing databases")
            if(reCreatedb == "y"):
            	sql = "create unique index " + tb_info_index + " on " + tb_info + " (pkey)"
            	mycursor.execute(sql)
            	sql = "create unique index " + tb_Tov_index + " on " + tb_Tov + " (proteins)"
            	mycursor.execute(sql)
            if(reCreatedbcdhit == "y"):
            	sql = "create index " + tb_virS_index + " on " + tb_virS + " (ercluster)"
            	mycursor.execute(sql)
            print("Done indexing databases")
        print("Done initializing MySQL DataBase")
        
        print("")
        print("")
        print("")
        print("")
        #endregion

        # Make tables and create file
        #region
        
        print("Getting all clusters!")
        sql = "SELECT * FROM " + tb_virS + " ORDER BY ercluster"
        mycursor.execute(sql)
        erclusters = mycursor.fetchall()
        print("TOTAL CLUSTERS: " + str(erclusters.__len__()) + "!")

        print("==== Starting file writing ====")
        ex = 0

        last_ercluster = ""
        ekproteinlist = []

        PCsFile = open(bestFileName("PCs"), "w+")

        PCsFile.write("tara_cluster\ttara_protein\tdepth\tregion\ttemperature\tsalinity\toxygen\tchlorophyl\tnitrite\tphosphate\tnitrite_nitrate\tsilica\tsynechococcus\tprochlorococcus\tbacteria\tlow_dna_bacteria\thigh_dna_bacteria\thigh_dna_bacteria_pers\tuser_proteins...\n")

        while ex < erclusters.__len__():
            if ex % 1000 == 0:
                print(str(ex/erclusters.__len__()*100) + "%" + " (" + str(ex) + "/" + str(erclusters.__len__()) + ")")
            protein = erclusters[ex][0]
            ekprotein = erclusters[ex][1]
            myercluster = erclusters[ex][2]
            pkey = erclusters[ex][3]
            
            if (last_ercluster != myercluster and last_ercluster != ""):
                writing = stringtowrite(protein, ekproteinlist, pkey)
                if(writing != ""):
                        PCsFile.write(writing + "\n")
                last_ercluster = myercluster
                ekproteinlist.clear()
                ekproteinlist.append(ekprotein)
            else:
                ekproteinlist.append(ekprotein)
            last_ercluster = myercluster
            ex+=1
        writing = stringtowrite(protein, ekproteinlist, pkey)
        if(writing != ""):
                PCsFile.write(writing + "\n")
        PCsFile.close()
        #endregion

    else:
        print(sys.argv[1]+" Not a valid file!")

    print("Thanks for using the BioLoad Suite " + Version + " By Vasco Varas")
