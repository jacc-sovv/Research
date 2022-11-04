import csv
from packaging import version as vs
S7_1500_VERSION = "2.9.4"

versions_dict = {"SIMATIC S7-1500 CPU" : "2.9.4", "SIMATIC S7-1500 Software Controller" : "21.9.4", "SIMATIC WinCC OA" : "3.18",
"Windows Server 2012" : "1000", "Microsoft SQL" : "1000", "SIMATIC WinCC" : "7.5", "SIMATIC WinCC Runtime Advanced" : "17",
"SIMATIC WinCC Runtime Professional" : "16"}


def checkVersion(product, product_version):
    version = description.find(product)
    version = description[version:]
    versionIndex = version.find("V")
    commaIndex = version.find(",")
    if (commaIndex < versionIndex):
        #There was no version given, so let's skip it for now
        #TO DO : COME BACK TO THIS
        #print(f"adding {cve} since there was no found version")
        cvss = row[3]
        vuln_type = row[5]
        if cve not in written_vulns:
            writer.writerow(['', '', cve, cvss, description, vuln_type])
            written_vulns.append(cve)
            return
        
    if(version == -1):
        print("Skip")
        writer.writerow(['', '', cve, cvss, description, vuln_type])
        written_vulns.append(cve)
        return
    version = version[versionIndex+1:]
    paramIndex = version.find(")")

    version = version[:paramIndex]
    #print(f"{versionIndex} to {paramIndex}")


    if(version.find('V') != -1):
        version = version[version.find('V')+1:]
    #print(version)
    if vs.parse(version) >= vs.parse(product_version):
        print(f"vulnerability {cve} found, {version} is vulnerable compared to {product_version}")
        
        cvss = row[3]
        vuln_type = row[5]
        if cve not in written_vulns:
            writer.writerow(['', '', cve, cvss, description, vuln_type])
            written_vulns.append(cve)
    return


#'main' is here
with open("./9-26-output.csv", 'r') as inp, open('./9-26-output_clean.csv', 'w') as out:
    written_vulns = []
    vendor = ''
    product = ''
    writer = csv.writer(out, lineterminator='\n')
    firstcount = True
    for row in csv.reader(inp):
        if not firstcount:
            if row[1]:  #If this is a vendor / product line
                vendor = row[0]
                product = row[1]
                writer.writerow([vendor, product])
            else:   #If this is a CVE line
                cve = row[2]
                year = int(cve[4:8])
                description = row[4]
                if year < 2019:
                    continue
                for exact_product in versions_dict:
                    product_version = versions_dict[exact_product]
                    if exact_product in description:
                        checkVersion(exact_product, product_version)

        else:
            writer.writerow(['vendor', 'product', 'cve', 'cvss', 'cve description', 'vulnerability type'])
            firstcount = False;




#Next Steps:
# Need to double check all vulnearbilities manually (shouldn't be too bad)
# Need to maybe add some more criteria to look for (like with wincc)
# Add another row saying which specific products are vulnerable