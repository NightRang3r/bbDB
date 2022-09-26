#!/usr/bin/env python3

import os
import sys
import shutil
import sqlite3
from sqlite3 import Error
import argparse
import csv
import requests
import validators
import tldextract
from colorama import Fore, Style
from colorama import init

RED_COLOR  = Style.BRIGHT + Fore.RED
GREEN_COLOR = Style.BRIGHT + Fore.GREEN
YELLOW_COLOR = Style.BRIGHT + Fore.YELLOW

def message():
    print(Style.BRIGHT + Fore.GREEN + '''
▀█████████▄  ▀█████████▄  ████████▄  ▀█████████▄  
  ███    ███   ███    ███ ███   ▀███   ███    ███ 
  ███    ███   ███    ███ ███    ███   ███    ███ 
 ▄███▄▄▄██▀   ▄███▄▄▄██▀  ███    ███  ▄███▄▄▄██▀  
▀▀███▀▀▀██▄  ▀▀███▀▀▀██▄  ███    ███ ▀▀███▀▀▀██▄  
  ███    ██▄   ███    ██▄ ███    ███   ███    ██▄ 
  ███    ███   ███    ███ ███   ▄███   ███    ███ 
▄█████████▀  ▄█████████▀  ████████▀  ▄█████████▀  
                                                                                                           
    ''')

    print(Style.BRIGHT + Fore.RED + '''                       /CODED BY : NightRang3r/          
''')                                              

init(autoreset=True)


def examples():
    print("Usage Examples:\n")
    print("Select from database:")
    print("=====================\n")
    print("Show Organization: " + YELLOW_COLOR + sys.argv[0] + " -sp")
    print("Show All TLD Domains: " + YELLOW_COLOR + sys.argv[0] + " -st")
    print("Show TLD Domains by Organization: " + YELLOW_COLOR  + sys.argv[0] + " -st -p paypal")
    print("Show All Subdomains: " + YELLOW_COLOR + sys.argv[0] + " -ss")
    print("Show Subdomains by TLD domain: " + YELLOW_COLOR + sys.argv[0] + " -tl paypal.com")
    print("Show Subdomains by Organization: " + YELLOW_COLOR  + sys.argv[0] + " -ss -p paypal")
    print("Run Dynamic select query: " + YELLOW_COLOR + sys.argv[0] + " -sq 'select * from Organization'\n")
    print("CSV Export")
    print("==========\n")
    print("Save Organization: " + YELLOW_COLOR + sys.argv[0] + " -sp -o results.csv")
    print("Save All TLD Domains: " + YELLOW_COLOR + sys.argv[0] + " -st -o results.csv")
    print("Save TLD Domains by Organization: " + YELLOW_COLOR + sys.argv[0] + " -st -p paypal -o results.csv")
    print("Save All Subdomains: " + YELLOW_COLOR + sys.argv[0] + " -ss -o results.csv")
    print("Save Subdomains by Organization: " + YELLOW_COLOR + sys.argv[0] + " -ss -p paypal -o results.csv")
    print("Show Subdomains by TLD domain: " + YELLOW_COLOR + sys.argv[0] + " -tl paypal.com -o results.csv")
    print("Save Dynamic select query results: " + YELLOW_COLOR + sys.argv[0] + " -sq 'select * from Organization' -o results.csv" + "\n")
    print("Insert into database")
    print("====================\n")
    print("Create Organization: " + YELLOW_COLOR + sys.argv[0] + " -cp -p paypal")
    print("Create Organization from file: " + YELLOW_COLOR + sys.argv[0] + " -cp -p Organization.txt -f")
    print("Create Organization from STDIN: " + "cat organization-list.txt | " + YELLOW_COLOR + sys.argv[0] + " -pp " + "or" + " echo PayPal | " + sys.argv[0] + " -pp")
    print("Create TLD Domain: " + YELLOW_COLOR + sys.argv[0] + " -ct paypal.com -p paypal")
    print("Create TLD Domain from file: " + YELLOW_COLOR + sys.argv[0] + " -ct tld.txt -p paypal -f")
    print("Create TLD Domain from STDIN: " + "cat tld-list.txt | " + YELLOW_COLOR + sys.argv[0] + " -pt -p paypal " + "or" + " echo paypal.com | " + sys.argv[0] + " -pt -p paypal")
    print("Create Subdomain: " + YELLOW_COLOR + sys.argv[0] + " -cs admin.paypal.com -p paypal")
    print("Create Subdomain from file: " + YELLOW_COLOR + sys.argv[0] + " -cs subdomains.txt -p paypal -f")
    print("Create Subdomain from STDIN: " + "cat subdomain-list.txt | " + YELLOW_COLOR + sys.argv[0] + " -ps -p paypal " + "or" + " echo paypal.com | " + sys.argv[0] + " -ps -p paypal\n")
    print("Search Database:")
    print("================\n")
    print("Search Organization: " + YELLOW_COLOR + sys.argv[0] + " -sp -t paypal")
    print("Search TLD Domains: " + YELLOW_COLOR + sys.argv[0] + " -st -t paypal")
    print("Search Subdomains: " + YELLOW_COLOR + sys.argv[0] + " -ss -t paypal\n")
    print("Remove from database:")
    print("=====================\n")
    print("Remove Organization from DB: " + YELLOW_COLOR +  sys.argv[0] + " -sp -r paypal")
    print("Remove TLD domain from DB: " + YELLOW_COLOR + sys.argv[0] + " -st -r paypal.com")
    print("Remove Subdomain from DB: " + YELLOW_COLOR + sys.argv[0] + " -ss -r admin.paypal.com\n")

parser = argparse.ArgumentParser(description='Manage BugBounty DB')
parser.add_argument('-sp', '--select-Organization', required=False, dest='SelectOrganization', help='List all Organizations in the Organization table', action='store_true')
parser.add_argument('-st', '--select-tld', dest='SelectTLD', help='List TLD Domains in the TLD_Domains table, Use -p to specify Organization name or without -p to return all', action='store_true')
parser.add_argument('-ss', '--select-subdomain', dest='SelectSubdomain', help='List Subomains from the Subdomains table, Use -p to specify Organization name or without -p to return all', action='store_true')
parser.add_argument('-sq', '--select-query', dest='SelectQuery', help='Excute a custom SQL query')
parser.add_argument('-cp', '--create-organization', required=False, dest='CreateOrganization', help='Insert a new record(s) to the Organizations table', action='store_true')
parser.add_argument('-ct', '--create-tld', required=False, dest='CreateTLD', help='Insert a new record(s) to the TLD_Domains table')
parser.add_argument('-cs', '--create-subdomain', required=False, dest='CreateSubdomain', help='Insert a new record(s) to the Subdomains table')
parser.add_argument('-pp', '--pipe-organization', dest='pipeOrg', help='Insert a new record(s) to the organization table from stdin', required=False, action='store_true')
parser.add_argument('-pt', '--pipe-tld', dest='pipeTLD', help='Insert a new record(s) to the TLD_Domains table from stdin', required=False, action='store_true')
parser.add_argument('-ps', '--pipe-subdomain', dest='pipeSubdomains', help='Insert a new record(s) to the Subdomains table from stdin', required=False, action='store_true')
parser.add_argument('-c', '--count', dest='countResults', help='Display records count', required=False, action='store_true')
parser.add_argument('-p', '--organization-name', dest='OrganizationName', help='Set Organization Names, or all', required=False)
parser.add_argument('-t', '--search-term', dest='SearchTerm', help='Search table', required=False)
parser.add_argument('-tl', '--tld-domain', dest='TLDomain', help='Filter by TLD domain', required=False)
parser.add_argument('-f', '--file', dest='FileName', help='Input file', required=False, action='store_true')
parser.add_argument('-o', '--output-csv', dest='CSVoutput', help='Save results to CSV file', required=False)
parser.add_argument('-r', '--remove', dest='removeRecord', help='Delete a record from database', required=False)
parser.add_argument('-q', '--quite', dest='QuiteMode', help='Suppress logo', required=False, action='store_true')
parser.add_argument('-nc', '--no-color', dest='NoColor', help='Disable color output', required=False, action='store_true')
parser.add_argument('-tg', '--telegram', dest='Telegram', help='Send telegram message', required=False, action='store_true')
parser.add_argument('-d', '--db', dest='DATABASE', help='Set Database file name', required=False)


args = parser.parse_args()

if len(sys.argv) < 2:
    message()
    examples()
    sys.exit(1)


def ValidateSubdomain(domain):
    domain = validators.domain(domain)
    return domain

def telegram_bot_sendtext(bot_message):
    bot_token = '0000000000:00000000000000000000000000000000000'
    bot_chatID = '000000000'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    try:
        response = requests.get(send_text)
        return response.json()
    except:
        pass

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def query(conn, query):
        if args.CSVoutput:
            try:
                cur = conn.cursor()
                cur.execute(query)
            except Error as e:
                print("[!] " , e)
            try:
                with open(args.CSVoutput, "w") as csv_file:
                    csv_writer = csv.writer(csv_file, delimiter=",")
                    csv_writer.writerow([i[0] for i in cur.description])
                    csv_writer.writerows(cur)
                print(GREEN_COLOR + "Results saved to: " + args.CSVoutput)
            except:
                 print(RED_COLOR + "[!] Error saving file!")
        else:
            try:
                cur = conn.cursor()
                cur.execute(query)
                rows = cur.fetchall() 
                if rows:
                    for row in rows:
                        print(row)
                    if (args.countResults):
                        print("\n" + GREEN_COLOR + "[+] " + str(len(rows)) + " record(s) found")
                else:
                    print(RED_COLOR + "[!] No results!")
            except Error as e:
                print("[!] " , e)

def select_all_organizations(conn):
    if args.CSVoutput:
        cur = conn.cursor()
        cur.execute("SELECT organization_name FROM organization ORDER BY organization_name ASC")
        try:
            with open(args.CSVoutput, "w") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=",")
                csv_writer.writerow([i[0] for i in cur.description])
                csv_writer.writerows(cur)
            print(GREEN_COLOR + "Results saved to: " + args.CSVoutput)
        except:
             print(RED_COLOR + "[!] Error saving file!")
    if args.SearchTerm: 
        cur = conn.cursor()
        search_term =('%' + args.SearchTerm + '%',)
        cur.execute("SELECT organization_name FROM organization WHERE organization_name LIKE ? COLLATE NOCASE", (search_term))
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(GREEN_COLOR + row[0])
            if (args.countResults):
                        print("\n" + GREEN_COLOR + "[+] " + str(len(rows)) + " record(s) found")
        else:
            print(RED_COLOR + "[!] No results!")
    else:
        cur = conn.cursor()
        cur.execute("SELECT organization_name FROM organization ORDER BY organization_name ASC")
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(GREEN_COLOR + row[0])
            if (args.countResults):
                        print("\n" + GREEN_COLOR + "[+] " + str(len(rows)) + " record(s) found")
        else:
            print(RED_COLOR + "[!] No results!")
    
def select_all_tld(conn):
    if args.CSVoutput:
        cur = conn.cursor()
        cur.execute("SELECT domain, organization_name FROM domains join organization USING (organization_id) ORDER BY organization_id ASC")
        try:
            with open(args.CSVoutput, "w") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=",")
                csv_writer.writerow([i[0] for i in cur.description])
                csv_writer.writerows(cur)
            print(GREEN_COLOR + "Results saved to: " + args.CSVoutput)
        except:
             print(RED_COLOR + "[!] Error saving file!")
    if args.SearchTerm:
        search_term =('%' + args.SearchTerm + '%',)
        cur = conn.cursor()
        cur.execute("SELECT domain, organization_name FROM domains join organization USING (organization_id) WHERE domain LIKE ? COLLATE NOCASE", (search_term))
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(GREEN_COLOR + row[0] + ', ' + row[1])
            if (args.countResults):
                        print("\n" + GREEN_COLOR + "[+] " + str(len(rows)) + " record(s) found")
        else:
            print(RED_COLOR + "[!] No results!")
    else:
        cur = conn.cursor()
        cur.execute("SELECT domain, organization_name FROM domains join organization USING (organization_id) ORDER BY organization_id ASC")
        rows = cur.fetchall()
        
        if rows:
            for row in rows:
                print(GREEN_COLOR + row[0] + ', ' + row[1])
            if (args.countResults):
                        print("\n" + GREEN_COLOR + "[+] " + str(len(rows)) + " record(s) found")
        else:
            print(RED_COLOR + "[!] No results!")

def select_all_subdomains(conn):
    if args.CSVoutput:
        cur = conn.cursor()
        cur.execute("SELECT subdomain, organization_name FROM Subdomains join organization USING (organization_id) ORDER BY organization_id ASC")
        try:
            with open(args.CSVoutput, "w") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=",")
                csv_writer.writerow([i[0] for i in cur.description])
                csv_writer.writerows(cur)
            print(GREEN_COLOR + "Results saved to: " + args.CSVoutput)
        except:
             print(RED_COLOR + "[!] Error opening file!")
    if args.SearchTerm:
        search_term =('%' + args.SearchTerm + '%',)
        cur = conn.cursor()
        cur.execute("SELECT subdomain, organization_name FROM Subdomains join organization USING (organization_id) WHERE subdomain LIKE ? COLLATE NOCASE", (search_term))
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(GREEN_COLOR + row[0] + ', ' + row[1])
            if (args.countResults):
                        print("\n" + GREEN_COLOR + "[+] " + str(len(rows)) + " record(s) found")
        else:
            print(RED_COLOR + "[!] No results!")
    else:
        cur = conn.cursor()
        cur.execute("SELECT subdomain, organization_name FROM Subdomains join organization USING (organization_id) ORDER BY organization_id ASC")
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(GREEN_COLOR + row[0] + ', ' + row[1])
            if (args.countResults):
                        print("\n" + GREEN_COLOR + "[+] " + str(len(rows)) + " record(s) found")
        else:
            print(RED_COLOR + "[!] No results!")

def select_all_tld_by_organization(conn, organization_name):
    if args.CSVoutput:
        cur = conn.cursor()
        cur.execute("SELECT domain from domains join organization USING (organization_id) where organization.organization_name =? COLLATE NOCASE", ([organization_name]))
        try:
            with open(args.CSVoutput, "w") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=",")
                csv_writer.writerow([i[0] for i in cur.description])
                csv_writer.writerows(cur)
            print(GREEN_COLOR + "Results saved to: " + args.CSVoutput)
        except:
             print(RED_COLOR + "[!] Error opening file!")
    else:
        cur = conn.cursor()
        cur.execute("SELECT domain from domains join organization USING (organization_id) where organization.organization_name =? COLLATE NOCASE", ([organization_name]))
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(GREEN_COLOR + row[0])
            if (args.countResults):
                        print("\n" + GREEN_COLOR + "[+] " + str(len(rows)) + " record(s) found")
        else:
            print(RED_COLOR + "[!] No results!")

def select_all_subdomains_by_organization(conn, organization_name):
    if args.CSVoutput:
        cur = conn.cursor()
        cur.execute("SELECT subdomain from Subdomains join organization USING (organization_id) where organization.organization_name =? COLLATE NOCASE", ([organization_name]))
        try:
            with open(args.CSVoutput, "w") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=",")
                csv_writer.writerow([i[0] for i in cur.description])
                csv_writer.writerows(cur)
            print(GREEN_COLOR + "Results saved to: " + args.CSVoutput)
        except:
             print(RED_COLOR + "[!] Error opening file!")
             
    else:
        cur = conn.cursor()
        cur.execute("SELECT subdomain from Subdomains join organization USING (organization_id) where organization.organization_name =? COLLATE NOCASE", ([organization_name]))
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(GREEN_COLOR + row[0])
            if (args.countResults):
                        print("\n" + GREEN_COLOR + "[+] " + str(len(rows)) + " record(s) found")
        else:
            print(RED_COLOR + "[!] No results!")
            
def select_all_subdomains_by_tld(conn, domain):
    if args.CSVoutput:
        cur = conn.cursor()
        cur.execute("SELECT subdomain from subdomains where domain_id=(select domain_id from domains where domain =" + "'" + domain + "')")
        try:
            with open(args.CSVoutput, "w") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=",")
                csv_writer.writerow([i[0] for i in cur.description])
                csv_writer.writerows(cur)
            print(GREEN_COLOR + "Results saved to: " + args.CSVoutput)
        except:
             print(RED_COLOR + "[!] Error opening file!")
             
             
    else:
        cur = conn.cursor()
        cur.execute("SELECT subdomain from subdomains where domain_id=(select domain_id from domains where domain =" + "'" + domain + "')")
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(GREEN_COLOR + row[0])
            if (args.countResults):
                        print("\n" + GREEN_COLOR + "[+] " + str(len(rows)) + " record(s) found")
        else:
            print(RED_COLOR + "[!] No results!")

def create_organization(conn, organization_name):
    cur = conn.cursor()
    cur.execute("SELECT organization_name FROM organization WHERE organization_name=? COLLATE NOCASE", ([organization_name]))
    result = cur.fetchone()
    if result:
        print(RED_COLOR + "[!] " +  organization_name + " Organization already exist")
    else:
        sql = '''INSERT INTO organization(organization_name) VALUES(?)'''
        cur = conn.cursor()
        cur.execute(sql, [organization_name])
        conn.commit()
        print(GREEN_COLOR + "[+] " + organization_name + " organization added to database.")
        return cur.lastrowid

def create_tld(conn, domain, organization_name):
    cur = conn.cursor()
    cur.execute("SELECT organization_name FROM organization WHERE organization_name=? COLLATE NOCASE", ([organization_name]))
    result = cur.fetchone()
    if not result:
        print(RED_COLOR + "[!] Organization not valid!")
    else:
        cur = conn.cursor()
        cur.execute("SELECT domain FROM domains WHERE domain=? COLLATE NOCASE", ([domain.replace('*.','')]))
        result = cur.fetchone()
        if result:
            print(RED_COLOR + "[!] " + domain + " TLD Domain already exist")
        else:
            if domain.startswith("*."):
                domain =  domain.replace('*.','')
                sql = """INSERT INTO domains(domain, organization_id, is_wildcard) VALUES(""" + "'" + domain.lower() + "'" + """, (SELECT organization_id FROM organization WHERE organization_name=""" + "'" + organization_name + "' COLLATE NOCASE""),1"")"""
            else:
                sql = """INSERT INTO domains(domain, organization_id, is_wildcard) VALUES(""" + "'" + domain.lower() + "'" + """, (SELECT organization_id FROM organization WHERE organization_name=""" + "'" + organization_name + "' COLLATE NOCASE""),0"")"""
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            print(GREEN_COLOR + "[+] TLD Domain '" + domain.lower() + "' added to the " + organization_name + " organization")
            return cur.lastrowid

def create_subdomain(conn, subdomain, organization_name):
    cur = conn.cursor()
    cur.execute("SELECT organization_name FROM organization WHERE organization_name=? COLLATE NOCASE", ([organization_name]))
    result = cur.fetchone()
    if not result:
        print(RED_COLOR + "[!] Organization not valid!")
    
    else:
        cur = conn.cursor()
        cur.execute("SELECT subdomain FROM Subdomains WHERE subdomain=? COLLATE NOCASE", ([subdomain]))
        result = cur.fetchone()
        if result:
            print(RED_COLOR + "[!] " + subdomain + " Subdomain already exist")
        
        else:
            cur = conn.cursor()
            cur.execute("SELECT domain FROM domains WHERE domain=? COLLATE NOCASE", ([tldextract.extract(subdomain).registered_domain]))
            result = cur.fetchone()
            if not result:
                print(RED_COLOR + "[!] TLD doamin not in DB, not adding subdomain!")
            else:
                sql = """INSERT INTO subdomains(subdomain, organization_id, domain_id) VALUES(""" + "'" + subdomain.lower() + "'" + """, (SELECT organization_id FROM organization WHERE organization_name=""" + "'" + organization_name + "'" + " COLLATE NOCASE), (SELECT domain_id FROM domains WHERE domain=""" + "'" +  tldextract.extract(subdomain).registered_domain + "'" + "))"""

                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                print(GREEN_COLOR + "[+] '" + subdomain.lower() + "' added to the " + organization_name + " organization subdomain list.")
                if args.Telegram:
                    telegram_bot_sendtext(subdomain.lower() + " added to the " + organization_name + " organization subdomain list.")
                return cur.lastrowid

def deleteRecord(conn, table, column, data):
    cur = conn.cursor()
    cur.execute("SELECT " + column + " FROM " + table + " WHERE " + column + "=" + "'" + data + "' COLLATE NOCASE")
    result = cur.fetchone()
    if not result:
        print(RED_COLOR + "[!] No results")
    else:
        sql = 'DELETE FROM ' + table + ' WHERE ' + column + '=' + "'" + data + "' COLLATE NOCASE"
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print(GREEN_COLOR + "[+] " + data + ' was deleted from ' + table)


def main():

    HOME_DIR = os.path.join(os.getcwd(), '')
    DB_NAME = 'Subdomains.db'
    DB_PATH = HOME_DIR + DB_NAME
    
    if not (args.QuiteMode):
        message()
    
    if (args.DATABASE):
        DB_PATH = args.DATABASE
    
    if not (os.path.exists(DB_PATH)):
        print(RED_COLOR + "[!] DB File Missing!")
        print(GREEN_COLOR + "[*] Restoring new DB file!")
        try:
            shutil.copy2(HOME_DIR + '.clean_db', DB_PATH)
        except Exception as e:
            print(e)
        
    conn = create_connection(DB_PATH)
    with conn:
        if (args.SelectOrganization):
            if args.removeRecord:
                deleteRecord(conn, "organization", "organization_name", args.removeRecord)
            else:
                select_all_organizations(conn)
        if (args.SelectTLD):
            if args.removeRecord:
                deleteRecord(conn, "domains", "domain", args.removeRecord)
            elif (args.OrganizationName is None or args.OrganizationName=='all'):
               select_all_tld(conn)
            else:
                select_all_tld_by_organization(conn, args.OrganizationName)
        if (args.SelectSubdomain):
            if args.removeRecord:
                deleteRecord(conn, "Subdomains", "subdomain", args.removeRecord)
            elif (args.OrganizationName is None or args.OrganizationName=='all'):
                select_all_subdomains(conn)
            else:
                select_all_subdomains_by_organization(conn,  args.OrganizationName)
        if(args.TLDomain):
            select_all_subdomains_by_tld(conn, args.TLDomain)

        if (args.SelectQuery):
             query(conn, args.SelectQuery)
        if (args.CreateOrganization):
            if (args.OrganizationName is None):
                print(RED_COLOR + '[!] Please use -p to specify organization name')
            else:
                if args.FileName:
                    try:
                        f = open(args.OrganizationName, 'rt')
                        l = f.readline()
                        while (l):
                            create_organization(conn, l.strip())
                            l = f.readline()
                        f.close()
                    except:
                        print(RED_COLOR + "[!] Error opening file!")
                else:
                   create_organization(conn, args.OrganizationName)
        if (args.CreateTLD):
            if (args.OrganizationName is None):
                print(RED_COLOR + '[!] Please use -p to specify organization name')
            else:
                if args.FileName:
                    try:
                        f = open(args.CreateTLD, 'rt')
                        l = f.readline()
                        while (l):
                            if not ValidateSubdomain(l.strip()):
                                print(RED_COLOR + "[!] Invalid domain name " + "'" + l.strip() + "'")
                            else:
                                create_tld(conn, l.strip(), args.OrganizationName)
                            l = f.readline()
                        f.close()
                    except:
                        print(RED_COLOR +"[!] Error opening file!")
                else:
                    if not ValidateSubdomain(args.CreateTLD):
                        print(RED_COLOR + "[!] Invalid domain name " + "'" + args.CreateTLD + "'")
                    else:
                        create_tld(conn, args.CreateTLD, args.OrganizationName)
        if (args.CreateSubdomain):
            if (args.OrganizationName is None):
                print(RED_COLOR +'[!] Please use -p to specify organization name')
            else:
                if args.FileName:
                    try:
                        f = open(args.CreateSubdomain, 'rt')
                        l = f.readline()
                        while (l):
                            if not ValidateSubdomain(l.strip()):
                                print(RED_COLOR + "[!] Invalid domain name " + "'" + l.strip() + "'")
                            else:
                                create_subdomain(conn,  l.strip(), args.OrganizationName)
                            l = f.readline()
                        f.close()
                    except:
                        print(RED_COLOR + "[!] Error opening file!")
                else:
                    if not ValidateSubdomain(args.CreateSubdomain):
                        print(RED_COLOR + "[!] Invalid domain name " + "'" + args.CreateSubdomain + "'")
                    else:
                        create_subdomain(conn, args.CreateSubdomain, args.OrganizationName)
        if (args.pipeSubdomains):
            if (args.OrganizationName is None):
                print(RED_COLOR + '[!] Please use -p to specify organization name')
            else:
                for line in sys.stdin:
                    if not ValidateSubdomain(line.strip()):
                        print(RED_COLOR + "[!] Invalid domain name " + "'" + line.strip() + "'")
                    else:
                        create_subdomain(conn, line.strip(), args.OrganizationName)
        if (args.pipeOrg):
            if (args.pipeOrg is None):
                print(RED_COLOR + '[!] Please specify organization name')
            else:
                for line in sys.stdin:
                    create_organization(conn, line.strip())
                        
        if (args.pipeTLD):
            if (args.OrganizationName is None):
                print(RED_COLOR + '[!] Please use -p to specify organization name')
            else:
                for line in sys.stdin:
                    if not ValidateSubdomain(line.strip()):
                        print(RED_COLOR + "[!] Invalid domain name " + "'" + line.strip() + "'")
                    else:
                        create_tld(conn, line.strip(), args.OrganizationName)
                        

if __name__ == '__main__':

    if (args.NoColor):
        GREEN_COLOR = ''
        RED_COLOR = ''
        YELLOW_COLOR = ''
    main()
    init(autoreset=True)

