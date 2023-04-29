import time
from azure.identity import DefaultAzureCredential

## Import control plane sdk

from azure.mgmt.confidentialledger import ConfidentialLedger as ConfidentialLedgerAPI
from azure.mgmt.confidentialledger.models import ConfidentialLedger

# import data plane sdk

from azure.confidentialledger import ConfidentialLedgerClient
from azure.confidentialledger.certificate import ConfidentialLedgerCertificateClient

# Set variables

resource_group = "myResourceGroup"
ledger_name = "myLedgers"
subscription_id = "576f43f0-8947-474f-b221-4fb3c11c3488"

identity_url = "https://identity.confidential-ledger.core.azure.com"
ledger_url = "https://" + ledger_name + ".confidential-ledger.azure.com"

# Authentication

# Need to do az login to get default credential to work

credential = DefaultAzureCredential()

# Control plane (azure.mgmt.confidentialledger)
# 
# initialize endpoint with credential and subscription

confidential_ledger_mgmt = ConfidentialLedgerAPI(
    credential, "576f43f0-8947-474f-b221-4fb3c11c3488"
)

# Create properties dictionary for begin_create call 

properties = {
    "location": "eastus",
    "tags": {},
    "properties": {
        "ledgerType": "Public",
        "aadBasedSecurityPrincipals": [],
    },
}

ledger_properties = ConfidentialLedger(**properties)

# Create a ledger

confidential_ledger_mgmt.ledger.begin_create(resource_group, ledger_name, ledger_properties)

# Get the details of the ledger you just created

print(f"{resource_group} / {ledger_name}")
 
print("Here are the details of your newly created ledger:")
myledger = confidential_ledger_mgmt.ledger.get(resource_group, ledger_name)

print (f"- Name: {myledger.name}")
print (f"- Location: {myledger.location}")
print (f"- ID: {myledger.id}")

# Data plane (azure.confidentialledger)
#
# Create a CL client

identity_client = ConfidentialLedgerCertificateClient(identity_url)
network_identity = identity_client.get_ledger_identity(
     ledger_id=ledger_name
)

ledger_tls_cert_file_name = "networkcert.pem"
with open(ledger_tls_cert_file_name, "w") as cert_file:
    cert_file.write(network_identity['ledgerTlsCertificate'])


ledger_client = ConfidentialLedgerClient(
     endpoint=ledger_url, 
     credential=credential,
     ledger_certificate_path=ledger_tls_cert_file_name
)

# Write to the ledger
sample_entry = {"contents": "Hello world!"}
ledger_client.create_ledger_entry(entry=sample_entry)
  
# Read from the ledger
latest_entry = ledger_client.get_current_ledger_entry()
print(f"Current entry (transaction id = {latest_entry['transactionId']}) in collection {latest_entry['collectionId']}: {latest_entry['contents']}")