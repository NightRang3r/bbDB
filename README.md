# bbDB
Simple Python Script to manage bugbounty programs and subdomains


```
usage: bbDB.py [-h] [-sp] [-st] [-ss] [-sq SELECTQUERY] [-si] [-cp] [-ct CREATETLD] [-cs CREATESUBDOMAIN] [-ci CREATEIPADDRESS] [-pi] [-pp] [-pt] [-ps] [-c] [-p ORGANIZATIONNAME] [-t SEARCHTERM] [-tl TLDOMAIN] [-f] [-o CSVOUTPUT]
               [-r REMOVERECORD] [-q] [-nc] [-tg] [-d DATABASE]

Manage BugBounty DB

options:
  -h, --help            show this help message and exit
  -sp, --select-Organization
                        List all Organizations in the Organization table
  -st, --select-tld     List TLD Domains in the TLD_Domains table, Use -p to specify Organization name or without -p to return all
  -ss, --select-subdomain
                        List Subomains from the Subdomains table, Use -p to specify Organization name or without -p to return all
  -sq SELECTQUERY, --select-query SELECTQUERY
                        Excute a custom SQL query
  -si, --select-ipaddress
                        List IP Addresses from the ip address table, Use -p to specify Organization name or without -p to return all
  -cp, --create-organization
                        Insert a new record(s) to the Organizations table
  -ct CREATETLD, --create-tld CREATETLD
                        Insert a new record(s) to the TLD_Domains table
  -cs CREATESUBDOMAIN, --create-subdomain CREATESUBDOMAIN
                        Insert a new record(s) to the Subdomains table
  -ci CREATEIPADDRESS, --create-ipaddress CREATEIPADDRESS
                        Insert a new record(s) to the ip address table
  -pi, --pipe-ipaddress
                        Insert a ip to the ip address table from stdin
  -pp, --pipe-organization
                        Insert a new record(s) to the organization table from stdin
  -pt, --pipe-tld       Insert a new record(s) to the TLD_Domains table from stdin
  -ps, --pipe-subdomain
                        Insert a new record(s) to the Subdomains table from stdin
  -c, --count           Display records count
  -p ORGANIZATIONNAME, --organization-name ORGANIZATIONNAME
                        Set Organization Names, or all
  -t SEARCHTERM, --search-term SEARCHTERM
                        Search table
  -tl TLDOMAIN, --tld-domain TLDOMAIN
                        Filter by TLD domain
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


## Usage Examples

### Select from database:

Show Organization: ```bbDB.py -sp```

Show All TLD Domains: ```bbDB.py -st```

Show TLD Domains by Organization: ```bbDB.py -st -p paypal```

Show All Subdomains: ```bbDB.py -ss```

Show Subdomains by TLD domain: ```bbDB.py -tl paypal.com```

Show Subdomains by Organization: ```bbDB.py -ss -p paypal```

Show All IP Addresses: ```bbDB.py -si -p```

Show IP Addresses by Organization: ```bbDB.py -si -p paypal```

Run Dynamic select query: ```bbDB.py -sq 'select * from Organization'```

### CSV Export

Save Organization: ```bbDB.py -sp -o results.csv```

Save All TLD Domains: ```bbDB.py -st -o results.csv```

Save TLD Domains by Organization: ```bbDB.py -st -p paypal -o results.csv```

Save All IP Addresses: ```bbDB.py -si -o results.csv```

Save IP Addresses by Organization: ```bbDB.py -si -p paypal -o results.csv```

Save All Subdomains: ```bbDB.py -ss -o results.csv```

Save Subdomains by Organization: ```bbDB.py -ss -p paypal -o results.csv```

Show Subdomains by TLD domain: ```bbDB.py -tl paypal.com -o results.csv```

Save Dynamic select query results: ```bbDB.py -sq 'select * from Organization' -o results.csv```

### Insert into database

Create Organization: ```bbDB.py -cp -p paypal```

Create Organization from file: ```bbDB.py -cp -p Organization.txt -f```

Create Organization from STDIN: ```cat organization-list.txt | bbDB.py -pp or echo PayPal | bbDB.py -pp```

Create TLD Domain: ```bbDB.py -ct paypal.com -p paypal```

Create TLD Domain from file: ```bbDB.py -ct tld.txt -p paypal -f```

Create TLD Domain from STDIN: ```cat tld-list.txt | bbDB.py -pt -p paypal or echo paypal.com | bbDB.py -pt -p paypal```

Create Subdomain: ```bbDB.py -cs admin.paypal.com -p paypal```

Create Subdomain from file: ```bbDB.py -cs subdomains.txt -p paypal -f```

Create Subdomain from STDIN: ```cat subdomain-list.txt | bbDB.py -ps -p paypal or echo paypal.com | bbDB.py -ps -p paypal```

Insert IP Address: bbDB.py -ci 8.8.8.8 -p paypal
Insert IP Address from file: bbDB.py -ci ips.txt -p paypal -f
Insert IP Address from STDIN: cat ip-list.txt | bbDB.py -pi -p paypal or echo 8.8.8.8 | bbDB.py -pi -p paypal

### Search Database:

Search Organization: ```bbDB.py -sp -t paypal```

Search TLD Domains: ```bbDB.py -st -t paypal```

Search Subdomains: ```bbDB.py -ss -t paypal```

Search IP Addresses: ```bbDB.py -si -t 8.8.8.8```

### Remove from database:


Remove Organization from DB: ```bbDB.py -sp -r paypal```

Remove TLD domain from DB: ```bbDB.py -st -r paypal.com```

Remove Subdomain from DB: ```bbDB.py -ss -r admin.paypal.com```

Remove IP Address from DB: ```bbDB.py -si -r 8.8.8.8```