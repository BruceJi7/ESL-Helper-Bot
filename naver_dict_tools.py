import bs4, requests

def handleSplitWord(word):

    return '%20'.join(word.split(' '))

def discardWhitespace(titleString):
    titleString = titleString.replace('\r', '')
    titleString = titleString.replace('\t', '')
    titleString = titleString.replace(' ', '')
    titleString = titleString.replace('\n', ' ')

    return titleString


def getNaverDictLink(word):
    naver_url = r'https://en.dict.naver.com/#/search?range=meaning&query='


    if ' ' in word:
        word = handleSplitWord(word)


    return naver_url + word

def formatNaverResponse(meanings_dict):

    keys = [key for key in meanings_dict.keys()]
    values = [value for value in meanings_dict.values()]

    formatted_list = [f'{str(i+1)}: {keys[i]} - {values[i]}' for i in range(len(keys)-1)]

    return '\n'.join(formatted_list)

def getNaverDef_KORintoENG(requested_word):
    headers = {'User-Agent' : 'Chrome/70.0.3538.77'}

    if ' ' in requested_word:
        requested_word = handleSplitWord(requested_word)

    naver_url = r'https://endic.naver.com/search.nhn?sLn=en&searchOption=meanings&query='

    searchURL = naver_url + requested_word

    
    res = requests.get(searchURL, headers=headers)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, features='lxml')

    try:
        
        word_idiom_box = soup.find_all("dl", class_='list_e2')[1]   
        meaning_titles = word_idiom_box.find_all('dt')
    except:
        return None

    word_id_results = {}
    for dt_title in meaning_titles:

        # Extract string of title only
        title_span = dt_title.find('span', class_="fnt_e30")
        title = title_span.get_text().strip()


        # Extract string of sib-sibling meaning thing
        title_dd_sibling = dt_title.next_sibling.next_sibling
        meaning_span = title_dd_sibling.find('span', class_="fnt_k05")

        if meaning_span: #Throw away weird non-korean entries
            meaning = meaning_span.get_text().strip()
            if meaning: # final chance to discard empty lines
                word_id_results[title] = meaning

    return word_id_results




def getNaverDef_ENGintoKOR(requested_word):

    headers = {'User-Agent' : 'Chrome/70.0.3538.77'}

    if ' ' in requested_word:
        requested_word = handleSplitWord(requested_word)

    naver_url = r'https://endic.naver.com/search.nhn?sLn=en&searchOption=meanings&query='

    searchURL = naver_url + requested_word

    
    res = requests.get(searchURL, headers=headers)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, features='lxml')
    try:
        meanings_box = soup.find_all("dl", class_='list_e2')[1]
    except:
        return None

    meanings_titles = meanings_box.find_all('dt')

    meanings_results = {}
    for dt_title in meanings_titles:
        # Extract string of title only
        title_span = dt_title.find('span', class_="fnt_e30")
        title = discardWhitespace(title_span.get_text().strip())

        # Extract string of sib-sibling meaning thing
        title_dd_sibling = dt_title.next_sibling.next_sibling
        meaning_spans = title_dd_sibling.find_all('span', class_="fnt_k05")



        if meaning_spans: #Throw away weird non-korean entries

            meaning = ' '.join([sp.get_text().strip() for sp in meaning_spans])
            if meaning: # final chance to discard empty lines
                meanings_results[title] = meaning

    return meanings_results










if __name__ == '__main__':

    # test = '표현'
    # engtest = 'rntp'

    # print(getNaverDef_ENGintoKOR('save'))
    # print('--------')
    # print(getNaverDef_KORintoENG('구세'))

    print(formatNicely(getNaverDef_ENGintoKOR('house')))
    print(formatNicely(getNaverDef_KORintoENG('수준')))
    

