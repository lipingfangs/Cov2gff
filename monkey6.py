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

    with open("database/genenamelist.txt","r") as listinsidefile:
        listinsidef = list(listinsidefile.readlines())
        listinside = []
        for j in listinsidef:
            j = j.split("	")[0]
            listinside.append(j)
            
        for i in range(len(listinside)):
            listinside[i] = listinside[i].strip()
        print(listinside)
#
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
    seq_select(int(i[2])-52,int(i[3])+51,seqlines,i[1],n,outfile)
    outfile.close()

    
for i in listinside:
    #command2 = yourgenewisedir +"/genewise  ./database/" + i + " "+ yourdir +"/*" + i + ".fa" +  "  -pep> " + yourdir +"/" + i +".pep"
    command3 = yourgenewisedir +"/genewise  ./database/" + i + " "+ yourdir +"/*" + i + ".fa" +  " -quiet -kbyte 500000 -tfor  -gff -cdna > " + yourdir +"/" + i +".genewise.out"
    #command6 = yourgenewisedir +"/genewise  ./database/" + i + " "+ yourdir +"/*" + i + ".fa" +  "   -cdna > " + yourdir +"/" + i +"cdna.fa"
    print(command3);
    os.system(command3)
    #os.system(command2)
    #os.system(command3)
    command = "cat " + yourdir +"/" + i +".genewise.out | awk '/\/\/?/{b=0;n++}{if (b==0) {b=1} else{print $0 > \"" + yourdir +"/" + i +"splitret" + '"n"' + '.txt"} }' + "'"
    print(command);
    os.system(command);

command4 = "cat " + yourdir + "/QH*splitret1.txt > " + yourdir + "/" + infile + "_genewise.gff"    #need to translate the coordinates!
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
        print(i,end = "", file = genewisegffout)
genewisegffout.close()
genewisegff.close()

#commandclean = "rm " + yourdir + "/Q*  " + yourdir + "/in.fa_genewise.gff  " + yourdir + "/in.fa.gff"
#commandclean2 = "rm -rf blastout"
#os.system(commandclean)

testgo =  yourdir + "/" + infile + "_end_genewise.gff"           
selection1(testgo,yourdir,infile,listinside)
selection2(yourdir,infile,listinside)
