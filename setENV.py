import os
this_dir = os.path.dirname(os.path.abspath(__file__)) # The folder where 'setENV' is kept.

#Check if the config file exists
config_file = os.path.join(this_dir, 'CONFIG.txt')
if os.path.exists(config_file):
    print('Loading configurations...')
    with open(config_file, 'r') as f:
        configs = f.readlines()
    
    #Attempt to load the key
    try:
        loaded_key = configs[0][8:]
    except:
        raise Exception('CONFIG.txt file appears to be blank.')
        
    #Attempt to set the 
    if loaded_key:
        print('Setting ENVIRON variables...')
        os.environ['BOT_KEY'] = loaded_key

        print('Done')
    else:
        raise Exception("Discord Bot Key setting 'BOT_KEY' appears to be blank. ")
    
        


else:
    print('CONFIG.txt file is missing or obstructed: New one will be made.')
    print('Please copy your discord bot key into the new CONFIG.txt file.')

    with open(config_file, 'w') as f:
        f.write('BOT_KEY=')
    
