# bbDB
Simple Python Script to manage bugbounty programs and subdomains


```
usage: bbDB.py [-h] [-sp] [-st] [-ss] [-sr] [-sq SELECTQUERY] [-cp] [-ct CREATETLD] [-cs CREATESUBDOMAIN] [-cr ADDRESOLVED] [-pt] [-ps] [-pr] [-c] [-p PROGRAMNAME] [-t SEARCHTERM] [-f] [-o CSVOUTPUT] [-r REMOVERECORD] [-q] [-nc] [-tg]
               [-d DATABASE]

Manage BugBounty DB

options:
  -h, --help            show this help message and exit
  -sp, --select-program
                        List all Programs in the Programs table
  -st, --select-tld     List TLD Domains in the TLD_Domains table, Use -p to specify program name or without -p to return all
  -ss, --select-subdomain
                        List Subomains from the Subdomains table, Use -p to specify program name or without -p to return all
  -sr, --select-resolved
                        List only resolved subdomains from the Subdomains table, Use -p to specify program name or without -p to return all
  -sq SELECTQUERY, --select-query SELECTQUERY
                        Excute a custom SQL query
  -cp, --create-program
                        Insert a new record(s) to the Programs table
  -ct CREATETLD, --create-tld CREATETLD
                        Insert a new record(s) to the TLD_Domains table
  -cs CREATESUBDOMAIN, --create-subdomain CREATESUBDOMAIN
                        Insert a new record(s) to the Subdomains table
  -cr ADDRESOLVED, --add-resolved ADDRESOLVED
                        Update existing subdomain(s) with an IP address
  -pt, --pipe-tld       Insert a new record(s) to the TLD_Domains table from stdin
  -ps, --pipe-subdomain
                        Insert a new record(s) to the Subdomains table from stdin
  -pr, --pipe-resolved  Update existing subdomain(s) with an IP address from stdin
  -c, --count           Display records count
  -p PROGRAMNAME, --program-name PROGRAMNAME
                        Set Program Names, or all
  -t SEARCHTERM, --search-term SEARCHTERM
                        Search table
  -f, --file            Input file
  -o CSVOUTPUT, --output-csv CSVOUTPUT
                        Save results to CSV file
  -r REMOVERECORD, --remove REMOVERECORD
                        Delete a record from database
  -q, --quite           Suppress logo
  -nc, --no-color       Disable color output
  -tg, --telegram       Send telegram message
  -d DATABASE, --db DATABASE
                        Set Database file name


```


## Usage Examples:

### Select from database:

Show Programs: ```bbDB.py -sp```

Show All TLD Domains: ```bbDB.py -st```

Show TLD Domains by program: ```bbDB.py -st -p paypal```

Show All Subdomains: ```bbDB.py -ss```

Show Subdomains by program: ```bbDB.py -ss -p paypal```

Show All Resolved Subdomains: ```bbDB.py -sr```

Show Resolved Subdomains by program: ```bbDB.py -sr -p paypal```

Run Dynamic select query: ```bbDB.py -sq 'select * from programs'```

### CSV Export

Save Programs: ```bbDB.py -sp -o results.csv```

Save All TLD Domains: ```bbDB.py -st -o results.csv```

Save TLD Domains by program: ```bbDB.py -st -p paypal -o results.csv```

Save All Subdomains: ```bbDB.py -ss -o results.csv```

Save Subdomains by program: ```bbDB.py -ss -p paypal -o results.csv```

Save All Resolved Subdomains: ```bbDB.py -sr -o results.csv```

Save Resolved Subdomains by program: ```bbDB.py -sr -p paypal -o results.csv```

Save Dynamic select query results: ```bbDB.py -sq 'select * from programs' -o results.csv```


### Insert into database

Create Program: ```bbDB.py -cp -p paypal```

Create Program from file: ```bbDB.py -cp -p programs.txt -f```

Create TLD Domain: ```bbDB.py -ct paypal.com -p paypal```

Create TLD Domain from file: ```bbDB.py -ct tld.txt -p paypal -f```

Create TLD Domain from STDIN: ```cat tld-list.txt | bbDB.py -pt -p paypal or echo paypal.com | bbDB.py -pt -p paypal```

Create Subdomain: ```bbDB.py -cs admin.paypal.com -p paypal```

Create Subdomain from file: ```bbDB.py -cs subdomains.txt -p paypal -f```

Create Subdomain from STDIN: ```cat subdomain-list.txt | bbDB.py -ps -p paypal or echo paypal.com | bbDB.py -ps -p paypal```

Update subdomain IP Address from resolved list: ```bbDB.py -cr paypal_resolved.txt -f```

Update subdomain IP Address from STDIN: ```cat resolved.csv | bbDB.py -pr or echo admin.paypal.com,172.16.1.1 | bbDB.py -pr```


### Search Database:

Search Programs: ```bbDB.py -sp -t paypal```

Search TLD Domains: ```bbDB.py -st -t paypal```

Search Subdomains: ```bbDB.py -ss -t paypal```

Search Resolved Subdomains: ```bbDB.py -sr -t paypal```


### Remove from database:

Remove Program from DB: ```bbDB.py -sp -r paypal```

Remove TLD domain from DB: ```bbDB.py -st -r paypal.com```

Remove Subdomain from DB: ```bbDB.py -ss -r admin.paypal.com```
