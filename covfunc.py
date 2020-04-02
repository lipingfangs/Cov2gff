import os
import sys
def seqfr(yourdir,yourblastdir):
    ATGC_dict = {
             'A': 'T',
            'T': 'A',
            'G': 'C',
             'C': 'G',
             'a': 't',
             't': 'a',
             'g': 'c',
            'c': 'g',"N":"N","n":"n"}
    mylist = os.listdir(yourdir)
    for i in mylist:
        infile = i.strip()
        command =  yourblastdir + "/blastx -query " + yourdir+"/"+infile + " -db ./database/sarscov2 -evalue 1e-5 -num_threads 32  -outfmt 6 -out ./blastout/" + i+"_test"
        print(command)
        os.system(command)

    for m in mylist:
        file = open("blastout/"+ m +"_test","r")
        lines = file.readlines()
        lines = list(lines)
        dic={}
        temp = ""
        namefile = lines[1].split("	")[0]

        i = lines[0].split("	")
        i[0] =  i[1]
        if int(i[6]) > int(i[7]):
            infiles = open(infile , "r")
            infiless = list(infiles.readlines())
            for i in infiless:
                if i.startswith(">"):
                    temp = i.strip()[1:]
                    dic2[temp] = ""
                else:
                    dic2[temp] = dic[temp] + i.strip() 
            infiles.close()

            def reverse_seq(a):
                bases = ""
                for base in a:
                    bases = bases + ATGC_dict[base]
                bases = list(bases)
                bases.reverse()
                bases = ''.join(bases)
                return bases

                dic2[temp] = reverse_seq(dic2[temp])
                outfiles = open(infile , "w")
                print(">"+temp,file = outfiles)
                print(dic2[temp], file = outfiles)
                outfiles.close()
                
                
def seq_select(goin,endin,allreal,gggg,m,k):
    dic = ""
    dicr = {}
    goin = goin
    endin = endin
    golinenum = int(goin / (len(allreal[1])-1))
    golocationnum = int(goin % (len(allreal[1])-1))
    outlinenum = int(endin / (len(allreal[1])-1)) 
    outlocationnum = int(endin % (len(allreal[1])-1))
    cclist = list(allreal[golinenum+1:outlinenum+2])
    for i in cclist:
        dic = dic + i.strip()    
    dicout = dic[golocationnum:]
    dicout = dicout[:-(len(allreal[1])-outlocationnum-1)]
    print(">"+ m +"-"+str(gggg)+"-"+ str(goin)+"-"+str(endin),file = k)
    print(dicout,file = k)
    return ">"+m+str(gggg)+"-"+ str(goin)+"-"+str(endin)+dicout


def selection1(testgo,yourdir,infile,listinside):
    selectfile = open(testgo,"r")
    temp = 0
    for i in list(selectfile.readlines()):
        i = i.split("	")
        if i[2].strip() == "cds":
            temp = temp + 1
    selectfile.close()
    if temp > len(listinside) or temp < len(listinside):
        f = open(testgo,"w")
        print("error!",file = f)
        f.close()
        
def selection2(yourdir,infile,listinside):
    with open("database/genenamelist.txt","r") as listinsidefile:
        dic = {}
        for i in list(listinsidefile.readlines()):
            i = i.split("	")
            print(i)
            dic[i[0].strip()] = i[1].strip()
    for j in listinside:
        ginfile = open(yourdir + "/" + infile +"_" + j +".fa","r")
        ginfileline = list(ginfile)
        if abs(int(len(ginfileline[1]))/int(dic[j])) > 1.1 or abs(int(len(ginfileline[1]))/int(dic[j])) < 0.9:
            f = open(yourdir + "/" + infile + "_end_genewise.gff","w")
            print("error!",file = f)
            f.close()
            break
        
        
        
            
            
 
