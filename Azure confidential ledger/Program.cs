using System;
using System.Text.Json;
using Azure;
using Azure.Core;
using Azure.Identity;
using Azure.Security.ConfidentialLedger;
using Azure.Security.ConfidentialLedger.Certificate;
    
namespace acl_app
{
    class Program
    {
        static async Task Main(string[] args)
        {

            // Replace with the name of your confidential ledger

            const string ledgerName = "myLedgers";
            var ledgerUri = $"https://{ledgerName}.confidential-ledger.azure.com";

            // Create a confidential ledger client using the ledger URI and DefaultAzureCredential

            var ledgerClient = new ConfidentialLedgerClient(new Uri(ledgerUri), new DefaultAzureCredential());

            // Write to the ledger

            Operation postOperation = ledgerClient.PostLedgerEntry(
                waitUntil: WaitUntil.Completed,
                RequestContent.Create(
                    new { contents = "Hello world!" }));
            
            // Access the transaction ID of the ledger write

            string transactionId = postOperation.Id;
            Console.WriteLine($"Appended transaction with Id: {transactionId}");


            // Use the transaction ID to read from the ledger

            Response ledgerResponse = ledgerClient.GetLedgerEntry(transactionId);

            string entryContents = JsonDocument.Parse(ledgerResponse.Content)
                .RootElement
                .GetProperty("entry")
                .GetProperty("contents")
                .GetString();

            Console.WriteLine(entryContents);

        }
    }
}