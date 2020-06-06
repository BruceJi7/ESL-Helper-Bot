import requests, bs4



def formatDictcomResponse(meanings_dict):

    keys = [key for key in meanings_dict.keys()]
    values = [value for value in meanings_dict.values()]

    formatted_list = []
    for i in range(len(keys)-1):
        part_of_speech = keys[i]
        meanings = values[i]

        meaning_string = '\n- '.join(meanings)

        formatted_list.append(f'{str(i+1)}: {part_of_speech} --------------\n- {meaning_string}')

    return '\n'.join(formatted_list)

def getDictLink(word):
    dictcom_url = r'https://www.dictionary.com/browse/'

    if ' ' in word:
        word = '--'.join(word.split(' '))

    return dictcom_url + word


def getDefinitionFromDictSite(word):
    '''
    Given a single word, searches for definition on web and returns most uses for that word.  Returns a dict.

    Parameters:
    word: Single word as string.

    '''

    
    dictionary_url = 'https://www.dictionary.com/browse/'

    headers = {'User-Agent' : 'Chrome/70.0.3538.77'}

    res = requests.get(f'{dictionary_url}{word}', headers=headers)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, features='html.parser')

    # word_heading_section = soup.select("#top-definitions-section")
    heading = soup.select('.css-1jzk4d9')

    top_definitions_section = soup.select('.css-1urpfgu.e16867sm0')[0] # Dict site uses this class to contain definitions chunk. We just want the top.
    
    # Get IPA for the word
    IPA_pron = top_definitions_section.select('.pron-ipa-content.css-z3mf2.evh0tcl2')[0].text

    definitions = top_definitions_section.select('.css-pnw38j.e1hk9ate0') #This contains each definition. Iterate over this

    found_definitions_dict = {}
    for c in definitions:
        part_of_speech = c.select('.luna-pos')[0].text.capitalize() #Noun, Verb, etc
        all_defs = c.select('.e1hk9ate4')

        definition_text = [] # List of all text-only definitions

        for definition_paragraph in all_defs: #For each chunk of definitions given for the part of speech...

            default_content = definition_paragraph.select('.default-content') #Check if there is the expandable cell
            if default_content:

                for definition_text_span in default_content: #For each actual entry inside this
                    for content in definition_text_span.select('.e1q3nk1v3'): #Get the text content from it.

                        definition_text_span = content.text

                        for luna_example in content.select('.luna-example'): # Find the example sentences
                            example_sentence = luna_example.text
                            
                            definition_text_span = definition_text_span.replace(example_sentence, '')

                        
                        
                        if definition_text_span.endswith(': '):
                            definition_text_span = definition_text_span[:-2]
                        definition_text.append(definition_text_span)

            else: #No expandable content in cell

                for content in definition_paragraph.select('.e1q3nk1v3'): #Grab all content.

                    definition_text_span = content.text

                    for luna_example in content.select('.luna-example'): # Find the example sentences
                        example_sentence = luna_example.text
                        
                        definition_text_span = definition_text_span.replace(example_sentence, '')

                    
                    
                    if definition_text_span.endswith(': '):
                        definition_text_span = definition_text_span[:-2]

                    definition_text.append(definition_text_span)
                    
                    # definition_text.append(content.text)

        found_definitions_dict[part_of_speech] = definition_text

            



    return found_definitions_dict  
if __name__ == "__main__":

    print(getDefinitionFromDictSite('teleport'))