import os
import sys
from covfunc import *


yourdir = sys.argv[1]
yourblastdir = sys.argv[2]
yourgenewisedir = sys.argv[3]

coman = "mkdir blastout"
os.system(coman)

seqfr(yourdir,yourblastdir)



mylist = os.listdir(yourdir)
for i in mylist:
    infile = i.strip()
    command =  yourblastdir + "/blastx -query " + yourdir+"/"+infile + " -db ./database/sarscov2 -evalue 1e-5 -num_threads 32  -outfmt 6 -out ./blastout/" + i
    print(command)
    os.system(command)
    

for m in mylist:
    file = open("blastout/"+ m,"r")
    lines = file.readlines()
    lines = list(lines)
    dic={}
    temp = ""
    namefile = lines[1].split("	")[0]

    for i in lines:
        i = i.split("	")
        i[0] =  i[1]

        if int(i[6]) > int(i[7]):
            print(i[6],i[7])
            k = i[6]
            i[6] = i[7]
            i[7] = k

        if temp != i[0]: 
            dic[i[0]] = [0,0]
            dic[i[0]][0] = i[6]
            dic[i[0]][1] = i[7]
            temp = i[0]
            camp = ""

        if temp == i[0]:
            if abs(int(i[6]) - int(dic[i[0]][0]))>2000000:
                for j in i:
                    print(j,end = ",")
                print()
                continue


            else:
                if int(i[6]) < int(dic[i[0]][0]):
                    dic[i[0]][0] = i[6]
                if int(i[7]) > int(dic[i[0]][1]):
                    dic[i[0]][1] = i[7]
    #print(dic)    
    file.close()

    listinside = ["QHD43415.1_1",
    "QHD43415.1_2",
    "QHD43416.1",
    "QHD43417.1",
    "QHD43418.1",
    "QHD43419.1",
    "QHD43420.1",
    "QHD43421.1",
    "QHD43422.1",
    "QHD43423.2",
    "QHI42199.1"
    ]
    line = list(dic.keys())

    with open(yourdir +"/" + m +".gff","w") as f :
        for j in listinside:
            print(namefile + "	" + j ,end = "	",file = f)
            print(dic[j][0],end = "	",file = f)
            print(dic[j][1],file = f)

n = infile
seqfile = open(yourdir +"/" + n,"r")
cfile = open(yourdir +"/" + n+".gff","r")

seqlines = list(seqfile.readlines())
clines = list(cfile.readlines())

for i in clines:
    i = i.split("	")
    outfile = open(yourdir +"/" + n +"_"+ i[1] + ".fa","w")
    seq_select(int(i[2])-2,int(i[3])+5,seqlines,i[1],n,outfile)
    outfile.close()

    
for i in listinside:
    #command2 = yourgenewisedir +"/genewise  ./database/" + i + " "+ yourdir +"/*" + i + ".fa" +  "  -pep> " + yourdir +"/" + i +".pep"
    command3 = yourgenewisedir +"/genewise  ./database/" + i + " "+ yourdir +"/*" + i + ".fa" +  "   -gff > " + yourdir +"/" + i +".gff"
    command6 = yourgenewisedir +"/genewise  ./database/" + i + " "+ yourdir +"/*" + i + ".fa" +  "   -cdna > " + yourdir +"/" + i +"cdna.fa"
    os.system(command6)
    #os.system(command2)
    os.system(command3)

command4 = "cat " + yourdir + "/QHD*gff > " + yourdir + "/" + infile + "_genewise.gff"   
os.system(command4)    

genewisegff = open(yourdir + "/" + infile + "_genewise.gff","r")
genewisegfflist = genewisegff.readlines()
genewisegffout = open(yourdir + "/" + infile + "_end_genewise.gff","w")
for i in list(genewisegfflist):
    if i.find("//") == -1:
        i = i.split("\t")
        q = i[0].split("-")[2]
        i[3] = str(int(i[3]) + int(q))
        i[4] = str(int(i[4]) + int(q))
        i = '	'.join(i)
        print(i,file = genewisegffout)
genewisegffout.close()
genewisegff.close()

            
        
