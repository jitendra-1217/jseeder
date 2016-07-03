--

       _                           _               
      (_)  ___    ___    ___    __| |   ___   _ __ 
      | | / __|  / _ \  / _ \  / _` |  / _ \ | '__|
      | | \__ \ |  __/ |  __/ | (_| | |  __/ | |   
     _/ | |___/  \___|  \___|  \__,_|  \___| |_|   
    |__/                                           

--


##Change logs:

###v0.0.0

- Minimal working seeder for mysql
 - Takes input a config file (.yaml) which specifies things eg. - Tables to include. Per table configs - seed size. Column specific configs - which particular seeder to use etc...
 - Works per database: Resolves foreign key relationships across tables automatically
- Code structure abstracted for it to be extended:
 - for other engines eg. mongodb, postgres etc.
 - for adding custom seeders and use in config file
