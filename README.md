# Hotel-Booking-Analysis

Group#13

This program has 4 different major parts. You need to enter the corresponding folder and then run the code inside.

- k-anonymity
- Data analysis based on k-anonymity
- User Identity Check MD5 for User Password Hashing
- Two Trusted Data Centers Share Data Using RSA for Email Encryption and Decryption

You could see the details in our report.

## Dataset

The file: "data/hotel_booking.csv"

## How to run this program?

#### k-anonymity

Enter to "anonymity" folder.

```
cd anonymity
```

Run the code:

```
python ./anonymit.py
```

This will generate 2 files under the "result":

- input.csv
- output.csv

They are the files match the concept of k-anonymity.

#### Data analysis based on k-anonymity

Enter "analysis" folder:

```
cd analysis
```

Run the ".ipynb" file. You may need [Jupyter](https://jupyter.org/) environment.

After running this, you will see a bunch of charts generated.

#### User Identity Check MD5 for User Password Hashing

1. Enter "identify_token" folder:

```
cd identify_token
```

2. Run the ".ipynb" file. You may need [Jupyter](https://jupyter.org/) environment.

After running this:

- file "identify_token/random_passwords.txt" will be generated.
- file "modified_data/hotel_booking_token.csv" will be generated with the column "token" added.


3. Start the server:

```
python server.py
```

4. Test the user identity(Just an example, you may need to change the password to correct one to get a success check):

```
curl --location 'http://127.0.0.1:5000/login' \
--header 'Content-Type: application/json' \
--data '{
   "username": "669-792-1661",
   "password": "3c5678493dd6298f1ffc178bed9905ae" 
}'
```


#### Two Trusted Data Centers Share Data Using RSA for Email Encryption and Decryption

1. Enter the "identify_rsa_email" folder.

```
cd identify_rsa_email
```

2. Run the "identify_rsa_email_generate.ipynb" file. You may need [Jupyter](https://jupyter.org/) 

After running this:
- "identify_rsa_email/private_key.pem" will be generated.
- "identify_rsa_email/public_key.pem" will be generated.
- The file "modified_data/hotel_booking_token_rsaemail.csv" will be generated and the column "email" will be changed to encrypt the e-mail.

3. Run the "datacenter2.ipynb" file. You may need [Jupyter](https://jupyter.org/) 

After running this, it will fetch the encrypted data and decrypt it and show in the logs.

