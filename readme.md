--

       _                           _               
      (_)  ___    ___    ___    __| |   ___   _ __ 
      | | / __|  / _ \  / _ \  / _` |  / _ \ | '__|
      | | \__ \ |  __/ |  __/ | (_| | |  __/ | |   
     _/ | |___/  \___|  \___|  \__,_|  \___| |_|   
    |__/                                           

--

##Using

Run `python src/run.py -h`


##Change logs:

###v0.0.0 [WIP](https://github.com/jitendra-1217/jseeder/issues?q=is%3Aopen+is%3Aissue+milestone%3Av0.0.0)


- Minimal working seeder for mysql
 - Takes input a config file (.yaml) which specifies things eg. - Tables to include. Per table configs - seed size. Column specific configs - which particular seeder to use etc...
 - Works per database: Resolves foreign key relationships across tables automatically
- Code structure abstracted for it to be extended:
 - for other engines eg. mongodb, postgres etc.
 - for adding custom seeders and use in config file
