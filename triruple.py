import xml.etree.ElementTree as ET
import os
import copy
import codecs as cs

dic = {
    '制定/出台/发布-01': 'formulate',
    '监督/监测-02': 'monitor',
    '管理-03': 'manage',
    '是..的一部分-04': 'is a part of',
    '位于-05': 'is located in',
    '导致-06': 'result in',
    '保障-07': 'ensure',
    '使用/雇佣-08': 'use',
    '资助-09': 'fund',
    '治疗-10': 'cure',
    '传染(病原体/疾病->人)-11': 'infect',
    '感染(人->病原体/疾病)-12': 'is infected with',
    '批准-13': 'ratify',
    '承担/承办-14': 'undertake',
    '配备(人->装备等)-15': 'is equipped with',
    '应对/处理/响应-16': 'respond to',
    '预防-17': 'prevent',
    '参与-18': 'participate',
    '执行/实施-19': 'execute',
    '合作/协议-20': 'cooperate',
    '检测-21': 'detect',
    '诊断-22': 'diagnose',
    '废止-23': 'annul',
    '重组/改革-24': 'reform',
    '建立/组织-25': 'establish',
    '指导-26': 'guide',
    '研究/调查-27': 'research',
    '讨论-28': 'discuss',
    '研发-29': 'develop',
    '爆发于-30': 'outbreak',
    '泄露-31': 'leak',
    '有..病症-32': 'have sign or symptom',
} #用于转换中英文关系词的词典


dic_patch = {
    '传染(病原体/疾病': '传染(病原体/疾病->人)',
    '感染(人': '感染(人->病原体/疾病)',
    '配备(人': '配备(人->装备等)',
} #解决spilt会将'->'也分开的问题


#path = r'C:\Users\dell\Desktop\张世奇 v3\张世奇_新突发传染病-2\新发突发传染病-2_relation' #关系存放路径
path = r'D:\relation_all'
#path = r'C:\Users\dell\Desktop\test'  #测试路径

en_path = r'C:\Users\dell\Desktop\triruple\auto_en.txt' #英文结果文件存放位置
ch_path = r'C:\Users\dell\Desktop\triruple\auto_ch.txt' #中文结果文件存放位置

dirs = os.listdir(path)
files = []

for dir in dirs:
    files.append(path + '\\' + dir)

xmls = []
for file in files: #读取目录下所有xml文件
    xml = ET.parse(file)
    xmls.append(xml)

fp_en = cs.open(en_path,'w','utf-8') #要写入结果的文件对象
fp_ch = cs.open(ch_path,'w','utf-8')

cnt_q = 1 #初始化问题序号

for xml in xmls: #对单个xml文件进行处理
    root = xml.getroot()
    facts = root.findall('fact')

    #将读入的负例关系元素过滤掉
    #deleted = [] #将过滤掉的关系元素单独存放以供debug
    #for i in range(len(facts)):    用range()方法循环没法通过使用位置i的方法删除元素



    total = list(range(len(facts))) #给每一个关系元素准备的可比较元素模板
    comp_lst = [] #存放每个元素的可比较元素列表
    for i in range(len(facts)):
        comp_lst.append(copy.deepcopy(total)) #一定要用deepcopy，否则comp_lst中指针全部都指向一个list，元素一变全跟着变

    ''' 
    0:content
    1:entitys
    2:relationtriggers
    3:relations
    '''

    targets = [] #存放可能构成两跳关系的关系元素位置对

    for i in range(len(comp_lst)): #选出 i 号关系元素的对照表进行比较
        for j in comp_lst[i]: #选出表中每一个元素进行比较
            if i == j:
                continue
            if (facts[i][0].text == facts[j][0].text and 
                (facts[i][1][0].text == facts[j][1][0].text 
                or facts[i][1][0].text == facts[j][1][1].text 
                or facts[i][1][1].text == facts[j][1][0].text 
                or facts[i][1][1].text == facts[j][1][1].text) and 
                (facts[i][3][0].attrib['type'] != 'No Relation-00' and 
                facts[j][3][0].attrib['type'] != 'No Relation-00')):
                #如果两个关系元素所在句子相同且某一个实体相同，则可能会构成两跳关系（两个关系都不能是负例）
                targets.append([i , j]) #放入存放目标关系对的列表中
            
            comp_lst[j].remove(i)    #这次已经比较过 i 和 j 了，不需要再比较 j 和 i
        pass #debug

    #将筛选结果整理输出
    for target in targets:
        q = 'Q' + str(cnt_q) + ': ' + facts[target[0]][0].text + '\n' #两个关系对应句子应该是一样的，只要记录一个就够了
        fp_en.write(q)
        fp_ch.write(q)
        fp_en.write('Ans: \n') #答案空着等人工填写
        fp_ch.write('Ans: \n')
        tri_1_en = '<' + facts[target[0]][1][0].text + '>' + '\t' \
                + '<' + dic[facts[target[0]][3][0].attrib['type']] + '>' + '\t' \
                + '<' + facts[target[0]][1][1].text + '>'
        tri_2_en = '<' + facts[target[1]][1][0].text + '>' + '\t' \
                + '<' + dic[facts[target[1]][3][0].attrib['type']] + '>' + '\t' \
                + '<' + facts[target[1]][1][1].text + '>'
        try:
            facts[target[0]][3][0].attrib['type'].split('-')[2] #测试句子中是否有'->'，如果有，split 出的 list 应该有 2 号元素
            re_type_ch_1 = dic_patch[facts[target[0]][3][0].attrib['type'].split('-')[0]] #如果没有异常，则代表句子中有'->'，使用词典来补全关系词
        except: #如果产生异常，则代表句子中没有'->'
            re_type_ch_1 = facts[target[0]][3][0].attrib['type'].split('-')[0] #取出两个关系的中文关系词
        try: #第二个关系词的处理同上
            facts[target[1]][3][0].attrib['type'].split('-')[2] 
            re_type_ch_2 = dic_patch[facts[target[1]][3][0].attrib['type'].split('-')[0]] 
        except: #如果产生异常，则代表句子中没有'->'
            re_type_ch_2 = facts[target[1]][3][0].attrib['type'].split('-')[0] 

        tri_1_ch = '<' + facts[target[0]][1][0].text + '>' + '\t' \
                + '<' + re_type_ch_1 + '>' + '\t' \
                + '<' + facts[target[0]][1][1].text + '>'
        tri_2_ch = '<' + facts[target[1]][1][0].text + '>' + '\t' \
                + '<' + re_type_ch_2 + '>' + '\t' \
                + '<' + facts[target[1]][1][1].text + '>'

    

        
        fp_en.write('triple: ' + tri_1_en + '.' + tri_2_en + '\n\n') #写三元组
        fp_ch.write('triple: ' + tri_1_ch + '.' + tri_2_ch + '\n\n')
        cnt_q += 1 #写完一个问题，问题序号 + 1



    pass #debug

fp_en.close()
fp_ch.close()
pass #debug