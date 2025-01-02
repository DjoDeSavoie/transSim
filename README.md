**transSim**
Card transaction simulator project developed in Python

**Introduction**
This transaction management system processes financial transactions between issuer and acquirer accounts. It includes several interconnected components that handle various stages of a transaction, including balance verification, authorization generation, and interbank routing.

**Configuration**
Ensure your environment is set up with Python 3.x and that you have installed the required dependencies such as pymysql and colorama using pip:

pip3 install pymysql
pip install getpass4
pip install termcolor
pip install ntplib

**Components**

_Server Acquisition_ : This component runs a loop that continuously monitors log files in the logs/logsTPE/ directory. It looks for transactions marked as unprocessed (“isTraite”: false). When an unprocessed transaction is detected, the Server Acquisition calls the Server Authorization to begin the verification and authorization process.

_Server Authorization_ : This component is responsible for checking the available funds in the issuer account. It confirms that the balance is sufficient to cover the requested transaction. If the funds are adequate, the server authorizes the transaction and records the details in the autorisationtransaction table in the database.

_Interbank Routing_ : When a transaction involves two different banks, the system activates an interbank routing process. This service ensures that transactions are correctly routed between issuing and acquiring banks, adhering to interbank protocols and data exchange formats.

_Electronic Payment Terminal (TPE)_ : This virtual terminal initiates transactions. It simulates the interaction of a physical terminal by sending transaction requests to the Server Acquisition and receiving authorizations from the Server Authorization.

_NTP Server (Network Time Protocol)_ : This server is used to obtain precise and synchronized timestamps for each transaction. Timestamps are essential for traceability and auditing.

_Utilz_ : This component is a set of tools or utility libraries used across the system for common tasks such as date manipulation, log generation, etc.

_creationBanque_ : This script or function is responsible for adding new banks to the database. It adds records to the banque table with the necessary information for each newly created bank.

_creationCarte_ : This component manages the creation of new bank cards. It generates card numbers, PINs, and expiration dates, then saves them to the database.

_creationCompteAcquereur_ : This script creates new acquirer accounts used to receive funds during transactions. These accounts are added to the comptebancaireacquereur table with the appropriate details.

_creationCompteEmetteur_ : Similarly, this script creates new issuer accounts used to send money in transactions. The information for these accounts is stored in the comptebancaireemetteur table.

**Features**
_Transaction Processing_ : Transactions are read from a JSON log file. Each transaction contains information such as issuer and acquirer account numbers, the amount, and the transaction date.

_Balance Verification_ : Before proceeding with a transaction, the system checks that the issuer account has sufficient funds.

_Authorization Generation_ : For each successful transaction, an authorization is generated and stored in the autorisationtransaction table in the database.

_Transaction Routing_ : Transactions between different banks are managed by the interbank routing system.

_Receipt Display_ : After each transaction, a receipt is generated showing the authorization details.

**Usage**
To start the system, execute the main.py file, which will launch the main menu and allow users to select different actions such as checking balances, performing transactions, or stopping the program.

python main.py

The system automatically handles transactions in the background via a multithreaded process that monitors the JSON log files.

**Database Structure**
The database contains several tables to store information related to transactions, issuer and acquirer accounts, and transaction authorizations. Here is an overview of the main table structure:

_comptebancaireemetteur_ : Stores details of issuer accounts.
_comptebancaireacquereur_ : Stores details of acquirer accounts.
_autorisationtransaction_ : Logs authorizations for successful transactions.
_banque_ : Lists all banks.
_tpe_ : Lists all electronic payment terminals.
_carte bancaire_ : Lists all bank cards.

**Logs**
Log files are stored in the logs/logsTPE/ folder in JSON format. They contain transaction details to be processed and are continuously monitored by the system for processing.

**Security**
SHA256 hashing has been implemented to ensure optimal security throughout the transaction process.
