Logic explanation

 

Pre requisite :  to participate in integration - 'Is Active Tortal LMS User'?

Case A

1.User is system user

2.Under user doctype check 'Is Active Tortal LMS User'? Yes

3.No need to check company.

Default company/group comes from Tortal LMS System Settings-->Group Name (i.e. Empowery)

4.User gets "non admin" access for parent company/Group Empowery.

Login with user - michael@parsimony.com

 

 

Case A.1

User mentioned in 'Tortal LMS System Settings'-->Group Admin Identifier gets Admin access to Empowery

Note: Please ensure that such user's flag is 'Is Active Tortal LMS User'? Yes

Login with user - melissa@empowery.com

 

 

Case B

1.User is website user

2.Under user doctype check 'Is Active Tortal LMS User'?

3.Get company detail ('Customer'-->'Type' either 'Individual' or 'Company') .

If company name not present do nothing (even if Is Active Tortal LMS User? flag is enabled )

4.Company detail present and is not primary contact of that company.

Give him "non-admin" access for just that company and Empowery

Login with user - michael@gobestrong.com (Customer--> Type= Individual i.e   Michael_Pinkowski)

 

 

Case B.1

5.Company detail present and is primary contact of that company.

Give him "admin" access for just that company and non-admin access to Empowery

Login with user - dennis@hcgamerlife.com (Customer--> Type=Company i.e  Denada_LLC)

Login with user - steve.simonson@gmail.com (Customer--> Type=Company i.e  HomeAdor.com)