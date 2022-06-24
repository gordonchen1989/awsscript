import boto3
import csv

client = boto3.client('acm')

response = client.list_certificates()

csl = response["CertificateSummaryList"]

certlist = []

for cert in csl:
    arn = cert["CertificateArn"]
    cert_response = client.describe_certificate(CertificateArn = arn)
    cert['InUseBy'] = cert_response['Certificate']['InUseBy']
    certlist.append(cert)

csvFile = open("acm_result.csv", "w", newline='')
writer = csv.writer(csvFile)
for cert in certlist:
    temp = []
    for key in cert:
        temp.append(cert[key])
    
    writer.writerow(temp)

csvFile.close()
