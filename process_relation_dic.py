import codecs as cs

path = r'C:\Users\dell\Desktop\relation_dic.txt'
w_path = r'C:\Users\dell\Desktop\relation_dic_processed.txt'

fp = cs.open(path,'r','utf-8')
fp_w = cs.open(w_path,'w','utf-8')

fp_w.write('dic = {\n')

lines = fp.readlines()
for line in lines:
    line = line.strip('\r\n')
    re = line.split('\t')[0]
    pre = line.split('\t')[1]
    word = pre.split('/')[0]
    fp_w.write('\t\'' + re + '\': ' + '\'' + word + '\',\n')

fp_w.write('}')

fp.close()
fp_w.close()

pass #debug


