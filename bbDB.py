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
    print("Show Programs: " + YELLOW_COLOR + sys.argv[0] + " -sp")
    print("Show All TLD Domains: " + YELLOW_COLOR + sys.argv[0] + " -st")
    print("Show TLD Domains by program: " + YELLOW_COLOR  + sys.argv[0] + " -st -p paypal")
    print("Show All Subdomains: " + YELLOW_COLOR + sys.argv[0] + " -ss")
    print("Show Subdomains by program: " + YELLOW_COLOR  + sys.argv[0] + " -ss -p paypal")
    print("Show All Resolved Subdomains: " + YELLOW_COLOR  + sys.argv[0] + " -sr")
    print("Show Resolved Subdomains by program: " + YELLOW_COLOR  + sys.argv[0] + " -sr -p paypal")
    print("Run Dynamic select query: " + YELLOW_COLOR + sys.argv[0] + " -sq 'select * from programs'\n")
    print("CSV Export")
    print("==========\n")
    print("Save Programs: " + YELLOW_COLOR + sys.argv[0] + " -sp -o results.csv")
    print("Save All TLD Domains: " + YELLOW_COLOR + sys.argv[0] + " -st -o results.csv")
    print("Save TLD Domains by program: " + YELLOW_COLOR + sys.argv[0] + " -st -p paypal -o results.csv")
    print("Save All Subdomains: " + YELLOW_COLOR + sys.argv[0] + " -ss -o results.csv")
    print("Save Subdomains by program: " + YELLOW_COLOR + sys.argv[0] + " -ss -p paypal -o results.csv")
    print("Save All Resolved Subdomains: " + YELLOW_COLOR + sys.argv[0] + " -sr -o results.csv")
    print("Save Resolved Subdomains by program: " + YELLOW_COLOR + sys.argv[0] + " -sr -p paypal -o results.csv")
    print("Save Dynamic select query results: " + YELLOW_COLOR + sys.argv[0] + " -sq 'select * from programs' -o results.csv" + "\n")
    print("Insert into database")
    print("====================\n")
    print("Create Program: " + YELLOW_COLOR + sys.argv[0] + " -cp -p paypal")
    print("Create Program from file: " + YELLOW_COLOR + sys.argv[0] + " -cp -p programs.txt -f")
    print("Create TLD Domain: " + YELLOW_COLOR + sys.argv[0] + " -ct paypal.com -p paypal")
    print("Create TLD Domain from file: " + YELLOW_COLOR + sys.argv[0] + " -ct tld.txt -p paypal -f")
    print("Create TLD Domain from STDIN: " + "cat tld-list.txt | " + YELLOW_COLOR + sys.argv[0] + " -pt -p paypal " + "or" + " echo paypal.com | " + sys.argv[0] + " -pt -p paypal")
    print("Create Subdomain: " + YELLOW_COLOR + sys.argv[0] + " -cs admin.paypal.com -p paypal")
    print("Create Subdomain from file: " + YELLOW_COLOR + sys.argv[0] + " -cs subdomains.txt -p paypal -f")
    print("Create Subdomain from STDIN: " + "cat subdomain-list.txt | " + YELLOW_COLOR + sys.argv[0] + " -ps -p paypal " + "or" + " echo paypal.com | " + sys.argv[0] + " -ps -p paypal")
    print("Update subdomain IP Address from resolved list: " + YELLOW_COLOR + sys.argv[0] + " -cr paypal_resolved.txt -f")
    print("Update subdomain IP Address from STDIN: " + "cat resolved.csv | " + YELLOW_COLOR + sys.argv[0] + " -pr " + "or" + " echo admin.paypal.com,172.16.1.1 | " + sys.argv[0] + " -pr")
    print("Search Database:")
    print("================\n")
    print("Search Programs: " + YELLOW_COLOR + sys.argv[0] + " -sp -t paypal")
    print("Search TLD Domains: " + YELLOW_COLOR + sys.argv[0] + " -st -t paypal")
    print("Search Subdomains: " + YELLOW_COLOR + sys.argv[0] + " -ss -t paypal")
    print("Search Resolved Subdomains: " + YELLOW_COLOR + sys.argv[0] + " -sr -t paypal" )
    print("Remove from database:")
    print("=====================\n")
    print("Remove Program from DB: " + YELLOW_COLOR +  sys.argv[0] + " -sp -r paypal")
    print("Remove TLD domain from DB: " + YELLOW_COLOR + sys.argv[0] + " -st -r paypal.com")
    print("Remove Subdomain from DB: " + YELLOW_COLOR + sys.argv[0] + " -ss -r admin.paypal.com")

parser = argparse.ArgumentParser(description='Manage BugBounty DB')
parser.add_argument('-sp', '--select-program', required=False, dest='SelectProgram', help='List all Programs in the Programs table', action='store_true')
parser.add_argument('-st', '--select-tld', dest='SelectTLD', help='List TLD Domains in the TLD_Domains table, Use -p to specify program name or without -p to return all', action='store_true')
parser.add_argument('-ss', '--select-subdomain', dest='SelectSubdomain', help='List Subomains from the Subdomains table, Use -p to specify program name or without -p to return all', action='store_true')
parser.add_argument('-sr', '--select-resolved', dest='SelectResolved', help='List only resolved subdomains from the Subdomains table, Use -p to specify program name or without -p to return all', action='store_true')
parser.add_argument('-sq', '--select-query', dest='SelectQuery', help='Excute a custom SQL query')
parser.add_argument('-cp', '--create-program', required=False, dest='CreateProgram', help='Insert a new record(s) to the Programs table', action='store_true')
parser.add_argument('-ct', '--create-tld', required=False, dest='CreateTLD', help='Insert a new record(s) to the TLD_Domains table')
parser.add_argument('-cs', '--create-subdomain', required=False, dest='CreateSubdomain', help='Insert a new record(s) to the Subdomains table')
parser.add_argument('-cr', '--add-resolved', required=False, dest='addResolved', help='Update existing subdomain(s) with an IP address')
parser.add_argument('-pt', '--pipe-tld', dest='pipeTLD', help='Insert a new record(s) to the TLD_Domains table from stdin', required=False, action='store_true')
parser.add_argument('-ps', '--pipe-subdomain', dest='pipeSubdomains', help='Insert a new record(s) to the Subdomains table from stdin', required=False, action='store_true')
parser.add_argument('-pr', '--pipe-resolved', dest='pipeResolved', help='Update existing subdomain(s) with an IP address from stdin', required=False, action='store_true')
parser.add_argument('-c', '--count', dest='countResults', help='Display records count', required=False, action='store_true')
parser.add_argument('-p', '--program-name', dest='ProgramName', help='Set Program Names, or all', required=False)
parser.add_argument('-t', '--search-term', dest='SearchTerm', help='Search table', required=False)
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

def select_all_programs(conn):
    if args.CSVoutput:
        cur = conn.cursor()
        cur.execute("SELECT program_name FROM Programs ORDER BY program_name ASC")
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
        cur.execute("SELECT program_name FROM Programs WHERE program_name LIKE ? COLLATE NOCASE", (search_term))
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
        cur.execute("SELECT program_name FROM Programs ORDER BY program_name ASC")
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
        cur.execute("SELECT tld_domain, program_name FROM TLD_Domains join Programs USING (program_id) ORDER BY program_id ASC")
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
        cur.execute("SELECT tld_domain, program_name FROM TLD_Domains join Programs USING (program_id) WHERE tld_domain LIKE ? COLLATE NOCASE", (search_term))
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
        cur.execute("SELECT tld_domain, program_name FROM TLD_Domains join Programs USING (program_id) ORDER BY program_id ASC")
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
        cur.execute("SELECT subdomain, program_name FROM Subdomains join Programs USING (program_id) ORDER BY program_id ASC")
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
        cur.execute("SELECT subdomain, program_name FROM Subdomains join Programs USING (program_id) WHERE subdomain LIKE ? COLLATE NOCASE", (search_term))
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
        cur.execute("SELECT subdomain, program_name FROM Subdomains join Programs USING (program_id) ORDER BY program_id ASC")
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(GREEN_COLOR + row[0] + ', ' + row[1])
            if (args.countResults):
                        print("\n" + GREEN_COLOR + "[+] " + str(len(rows)) + " record(s) found")
        else:
            print(RED_COLOR + "[!] No results!")

def select_all_resolved(conn):
    if args.CSVoutput:
            cur = conn.cursor()
            cur.execute("SELECT subdomain, ip_address, program_name FROM Subdomains join Programs USING (program_id) WHERE is_resolved=1 ORDER BY program_id ASC")
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
        cur.execute("SELECT subdomain, ip_address, program_name FROM Subdomains join Programs USING (program_id) WHERE subdomain LIKE ? COLLATE NOCASE AND is_resolved=1", (search_term))
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(GREEN_COLOR + row[0] + ', ' + row[1] + ', ' + row[2])
            if (args.countResults):
                        print("\n" + GREEN_COLOR + "[+] " + str(len(rows)) + " record(s) found")
        else:
            print(RED_COLOR + "[!] No results!")
    else:
        cur = conn.cursor()
        cur.execute("SELECT subdomain, ip_address, program_name FROM Subdomains join Programs USING (program_id) WHERE is_resolved=1 ORDER BY program_id ASC")
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(GREEN_COLOR + row[0] + ', ' + row[1])
            if (args.countResults):
                        print("\n" + GREEN_COLOR + "[+] " + str(len(rows)) + " record(s) found")
        else:
            print(RED_COLOR + "[!] No results!")


def select_all_tld_by_program(conn, program_name):
    if args.CSVoutput:
        cur = conn.cursor()
        cur.execute("SELECT tld_domain from TLD_Domains join Programs USING (program_id) where Programs.program_name =? COLLATE NOCASE", ([program_name]))
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
        cur.execute("SELECT tld_domain from TLD_Domains join Programs USING (program_id) where Programs.program_name =? COLLATE NOCASE", ([program_name]))
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(GREEN_COLOR + row[0])
            if (args.countResults):
                        print("\n" + GREEN_COLOR + "[+] " + str(len(rows)) + " record(s) found")
        else:
            print(RED_COLOR + "[!] No results!")

def select_all_subdomains_by_program(conn, program_name):
    if args.CSVoutput:
        cur = conn.cursor()
        cur.execute("SELECT subdomain from Subdomains join Programs USING (program_id) where Programs.program_name =? COLLATE NOCASE", ([program_name]))
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
        cur.execute("SELECT subdomain from Subdomains join Programs USING (program_id) where Programs.program_name =? COLLATE NOCASE", ([program_name]))
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(GREEN_COLOR + row[0])
            if (args.countResults):
                        print("\n" + GREEN_COLOR + "[+] " + str(len(rows)) + " record(s) found")
        else:
            print(RED_COLOR + "[!] No results!")

def select_all_resolved_by_program(conn, program_name):
    if args.CSVoutput:
        cur = conn.cursor()
        cur.execute("SELECT subdomain, ip_address from Subdomains JOIN Programs USING (program_id) WHERE Programs.program_name =? COLLATE NOCASE AND is_resolved=1", ([program_name]))
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
        cur.execute("SELECT subdomain, ip_address FROM Subdomains JOIN Programs USING (program_id) WHERE Programs.program_name =? COLLATE NOCASE AND is_resolved=1", ([program_name]))
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(GREEN_COLOR + row[0] + ',' + row[1])
            if (args.countResults):
                        print("\n" + GREEN_COLOR + "[+] " + str(len(rows)) + " record(s) found")
        else:
            print(RED_COLOR + "[!] No results!")

def create_program(conn, program_name):
    cur = conn.cursor()
    cur.execute("SELECT program_name FROM Programs WHERE program_name=? COLLATE NOCASE", ([program_name]))
    result = cur.fetchone()
    if result:
        print(RED_COLOR + "[!] " +  program_name + " Program already exist")
    else:
        sql = '''INSERT INTO Programs(program_name) VALUES(?)'''
        cur = conn.cursor()
        cur.execute(sql, [program_name])
        conn.commit()
        print(GREEN_COLOR + "[+] " + program_name + " program added to database.")
        return cur.lastrowid

def create_tld(conn, tld_domain, program_name):
    cur = conn.cursor()
    cur.execute("SELECT program_name FROM Programs WHERE program_name=? COLLATE NOCASE", ([program_name]))
    result = cur.fetchone()
    if not result:
        print(RED_COLOR + "[!] Program not valid!")
    else:
        cur = conn.cursor()
        cur.execute("SELECT tld_domain FROM TLD_Domains WHERE tld_domain=? COLLATE NOCASE", ([tld_domain.replace('*.','')]))
        result = cur.fetchone()
        if result:
            print(RED_COLOR + "[!] " + tld_domain + " TLD Domain already exist")
        else:
            if tld_domain.startswith("*."):
                tld_domain =  tld_domain.replace('*.','')
                sql = """INSERT INTO TLD_Domains(tld_domain, program_id, is_wildcard) VALUES(""" + "'" + tld_domain.lower() + "'" + """, (SELECT program_id FROM Programs WHERE program_name=""" + "'" + program_name + "' COLLATE NOCASE""),1"")"""
            else:
                sql = """INSERT INTO TLD_Domains(tld_domain, program_id, is_wildcard) VALUES(""" + "'" + tld_domain.lower() + "'" + """, (SELECT program_id FROM Programs WHERE program_name=""" + "'" + program_name + "' COLLATE NOCASE""),0"")"""
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            print(GREEN_COLOR + "[+] TLD Domain '" + tld_domain.lower() + "' added to the " + program_name + " program")
            return cur.lastrowid

def create_subdomain(conn, subdomain, program_name):
    cur = conn.cursor()
    cur.execute("SELECT program_name FROM Programs WHERE program_name=? COLLATE NOCASE", ([program_name]))
    result = cur.fetchone()
    if not result:
        print(RED_COLOR + "[!] Program not valid!")
    else:
        cur = conn.cursor()
        cur.execute("SELECT subdomain FROM Subdomains WHERE subdomain=? COLLATE NOCASE", ([subdomain]))
        result = cur.fetchone()
        if result:
            print(RED_COLOR + "[!] " + subdomain + " Subdomain already exist")
        else:
            sql = """INSERT INTO Subdomains(subdomain, program_id) VALUES(""" + "'" + subdomain.lower() + "'" + """, (SELECT program_id FROM Programs WHERE program_name=""" + "'" + program_name + "'" + " COLLATE NOCASE""))"""
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            print(GREEN_COLOR + "[+] '" + subdomain.lower() + "' added to the " + program_name + " program subdomain list.")
            if args.Telegram:
                telegram_bot_sendtext(subdomain.lower() + " added to the " + program_name + " program subdomain list.")
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
        if (args.SelectProgram):
            if args.removeRecord:
                deleteRecord(conn, "Programs", "program_name", args.removeRecord)
            else:
                select_all_programs(conn)
        if (args.SelectTLD):
            if args.removeRecord:
                deleteRecord(conn, "TLD_Domains", "tld_domain", args.removeRecord)
            elif (args.ProgramName is None or args.ProgramName=='all'):
               select_all_tld(conn)
            else:
                select_all_tld_by_program(conn, args.ProgramName)
        if (args.SelectSubdomain):
            if args.removeRecord:
                deleteRecord(conn, "Subdomains", "subdomain", args.removeRecord)
            elif (args.ProgramName is None or args.ProgramName=='all'):
                select_all_subdomains(conn)
            else:
                select_all_subdomains_by_program(conn,  args.ProgramName)

        if (args.SelectQuery):
             query(conn, args.SelectQuery)
        if (args.CreateProgram):
            if (args.ProgramName is None):
                print(RED_COLOR + '[!] Please use -p to specify program name')
            else:
                if args.FileName:
                    try:
                        f = open(args.ProgramName, 'rt')
                        l = f.readline()
                        while (l):
                            create_program(conn, l.strip())
                            l = f.readline()
                        f.close()
                    except:
                        print(RED_COLOR + "[!] Error opening file!")
                else:
                   create_program(conn, args.ProgramName)
        if (args.CreateTLD):
            if (args.ProgramName is None):
                print(RED_COLOR + '[!] Please use -p to specify program name')
            else:
                if args.FileName:
                    try:
                        f = open(args.CreateTLD, 'rt')
                        l = f.readline()
                        while (l):
                            if not ValidateSubdomain(l.strip()):
                                print(RED_COLOR + "[!] Invalid domain name " + "'" + l.strip() + "'")
                            else:
                                create_tld(conn, l.strip(), args.ProgramName)
                            l = f.readline()
                        f.close()
                    except:
                        print(RED_COLOR +"[!] Error opening file!")
                else:
                    if not ValidateSubdomain(args.CreateTLD):
                        print(RED_COLOR + "[!] Invalid domain name " + "'" + args.CreateTLD + "'")
                    else:
                        create_tld(conn, args.CreateTLD, args.ProgramName)
        if (args.CreateSubdomain):
            if (args.ProgramName is None):
                print(RED_COLOR +'[!] Please use -p to specify program name')
            else:
                if args.FileName:
                    try:
                        f = open(args.CreateSubdomain, 'rt')
                        l = f.readline()
                        while (l):
                            if not ValidateSubdomain(l.strip()):
                                print(RED_COLOR + "[!] Invalid domain name " + "'" + l.strip() + "'")
                            else:
                                create_subdomain(conn,  l.strip(), args.ProgramName)
                            l = f.readline()
                        f.close()
                    except:
                        print(RED_COLOR + "[!] Error opening file!")
                else:
                    if not ValidateSubdomain(args.CreateSubdomain):
                        print(RED_COLOR + "[!] Invalid domain name " + "'" + args.CreateSubdomain + "'")
                    else:
                        create_subdomain(conn, args.CreateSubdomain, args.ProgramName)
        if (args.pipeSubdomains):
            if (args.ProgramName is None):
                print(RED_COLOR + '[!] Please use -p to specify program name')
            else:
                for line in sys.stdin:
                    if not ValidateSubdomain(line.strip()):
                        print(RED_COLOR + "[!] Invalid domain name " + "'" + line.strip() + "'")
                    else:
                        create_subdomain(conn, line.strip(), args.ProgramName)
        if (args.pipeTLD):
            if (args.ProgramName is None):
                print(RED_COLOR + '[!] Please use -p to specify program name')
            else:
                for line in sys.stdin:
                    if not ValidateSubdomain(line.strip()):
                        print(RED_COLOR + "[!] Invalid domain name " + "'" + line.strip() + "'")
                    else:
                        create_tld(conn, line.strip(), args.ProgramName)
        if (args.addResolved):
            if args.FileName:
                try:
                    f = open(args.addResolved, 'rt')
                    l = f.readline()
                    while (l):
                        csv_line = l.strip()
                        csv_clean = csv_line.split(",")
                        csv_subdomain = csv_clean[0]
                        csv_ip =  csv_clean[1]
                        cur = conn.cursor()
                        cur.execute("SELECT subdomain_id, subdomain, ip_address, is_resolved FROM Subdomains WHERE subdomain=? COLLATE NOCASE", ([csv_subdomain]))
                        result = cur.fetchone()             
                        if result:
                            ip_address = result[2]
                            subdomain_id = result[0]
                            if not ip_address:
                                sql = ("UPDATE Subdomains SET ip_address=" + "'" + csv_ip + "'" + ", is_resolved=1 WHERE subdomain_id=" + str(subdomain_id))
                                if args.Telegram:
                                    telegram_bot_sendtext("IP Address " + csv_ip + " updated for " + csv_subdomain)
                                print(GREEN_COLOR + "[+] Updating IP Address " + csv_ip + " for " + csv_subdomain)
                                cur = conn.cursor()
                                cur.execute(sql)
                                conn.commit()
                            else:
                                print(RED_COLOR + "[!] No update for " + csv_subdomain)
                        l = f.readline()
                    f.close()
                    if result == None:
                        print(GREEN_COLOR + "[!] Nothing to update or subdomains are not in table")
                except Exception as e:
                    print(e)

        if (args.pipeResolved):
                    try:
                        for line in sys.stdin:
                            csv_line = line.strip()
                            csv_clean = csv_line.split(",")
                            csv_subdomain = csv_clean[0]
                            csv_ip =  csv_clean[1]
                            cur = conn.cursor()
                            cur.execute("SELECT subdomain_id, subdomain, ip_address, is_resolved FROM Subdomains WHERE subdomain=? COLLATE NOCASE", ([csv_subdomain]))
                            result = cur.fetchone()
                            if result:
                                ip_address = result[2]
                                subdomain_id = result[0]
                                if not ip_address:
                                    sql = ("UPDATE Subdomains SET ip_address=" + "'" + csv_ip + "'" + ", is_resolved=1 WHERE subdomain_id=" + str(subdomain_id))
                                    if args.Telegram:
                                        telegram_bot_sendtext("IP Address " + csv_ip + " updated for " + csv_subdomain)
                                    print(GREEN_COLOR + "[+] Updating IP Address " + csv_ip + " for " + csv_subdomain)
                                    cur = conn.cursor()
                                    cur.execute(sql)
                                    conn.commit()
                                else:
                                    print(RED_COLOR + "[!] No update for " + csv_subdomain)
                        if result == None:
                            print(RED_COLOR + "[!] Nothing to update or subdomains are not in table")        
                    except Exception as e:
                        print(e)
    
        if(args.SelectResolved):
            if (args.ProgramName is None or args.ProgramName=='all'):
                select_all_resolved(conn)
            else:
                select_all_resolved_by_program(conn, args.ProgramName)

if __name__ == '__main__':

    if (args.NoColor):
        GREEN_COLOR = ''
        RED_COLOR = ''
        YELLOW_COLOR = ''
    main()
    init(autoreset=True)

