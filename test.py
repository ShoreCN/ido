import json
a = [1]
b = a[2:]
a = json.loads('[[[\"97095c98-0587-973b-bdd3-607ef94abf8a_2\", \"97095c98-0587-973b-bdd3-607ef94abf8a_2\", \"假标签\", 1, 0],[\"ce261285-113a-2fcc-75c3-a1817f161f95_2\", \"97095c98-0587-973b-bdd3-607ef94abf8a_2\", \"1\", 1, 0],[\"7f152ba6-354d-578d-1290-069c6a239839_2\", \"ce261285-113a-2fcc-75c3-a1817f161f95_2\", \"e\", 1, 0],[\"6fecb387-d8d8-afc8-0bec-ba4d1e95666f_2\", \"7f152ba6-354d-578d-1290-069c6a239839_2\", \"hh\", 1, 0],[\"005b9bdf-ed31-b757-5026-03dcc64765d8_2\", \"97095c98-0587-973b-bdd3-607ef94abf8a_2\", \"2\", 1, 0],[\"91b96097-3e38-9638-c9ea-28d644a16539_2\", \"97095c98-0587-973b-bdd3-607ef94abf8a_2\", \"3\", 1, 0],[\"7d022f98-d89e-091c-b760-2876cd4fe017_2\", \"97095c98-0587-973b-bdd3-607ef94abf8a_2\", \"4 #我们\", 1, 0]],[[\"2e176f50-a3cd-2a0e-c7b0-7be2feebb5c6_2\", \"ce9e7550-d58e-c56d-0cdf-2ff2dc6dd4aa_2\", \"#继续标签\", 2, 0],[\"1fd6b376-9d45-96e3-b8ce-66520974b197_2\", \"2e176f50-a3cd-2a0e-c7b0-7be2feebb5c6_2\", \"r1, #r\", 2, 0],[\"57bd0a52-99a9-7ff5-4540-24221b9db3cd_2\", \"2e176f50-a3cd-2a0e-c7b0-7be2feebb5c6_2\", \"r2 #r2\", 2, 0]]]'
)
b = 3
def FilterLabel(szContent):
    Labels = []
    label = ''
    iFirstLabelPos = None
    preChar = None
    iPos = -1
    iTempPos = -1
    i = 0
    for item in szContent:
        i += 1
        if item == ' ':
            if len(label) > 1:
                Labels.append(label)
                label = ''
                if iPos == -1:
                    iPos = iTempPos
            else:
                label = ''
            preChar = item
            continue
        elif (item == '@' or item == '#') and preChar == ' ':
            iTempPos = i
            label = item
            if preChar != None and iFirstLabelPos == None:
                iFirstLabelPos = i - 2
        else:
            if label != '':
                label += item
        preChar = item

    if len(label) > 1:
        Labels.append(label)
        result = True
    if iFirstLabelPos != None:
        return szContent[:iFirstLabelPos]
    else:
        return szContent
FilterLabel("5月6日 |《刷新》 #CEO #同理心 #成长型思维 #微软 #纳德拉")