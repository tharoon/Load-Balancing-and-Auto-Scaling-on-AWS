# Load-Balancing-and-Auto-Scaling-on-AWS

## The goal of this project was to have a practical knowledge on how load balancing and auto scaling of EC2 instances.

I developed a web aplication which involves querying earthquake details that occurs across the United States with simple UI using HTML5 and developed backend using the Python Framework. The backend for this application involoves processing of raw data fetched from the database. 
The database has the raw data of earthquakes that occured across the United States on a daily basis which has data from small magnitude earthquake to larger magnitude earthquakes.

I used SQL server for my database. I established a connection between my database that has been hosted on my AWS account to the local database in my machine. So I can query my database within my local machine. The backend of the application is built using python flask, 
which accepts request from the frontend and based on the endpoint, its corresponding function is triggered for processing the request and sends back the response to the frontend.

I configured my SQL Server database on my AWS account using the RDS.

I used the eb-cli to push my python application into the cloud.

I had to simulate real time requests to my EC2 instance where my python application was deployed, so I used Jmeter to spike requests to my application. 
Based on the requests I configured my application to scale up and down based on the request hit. I set my scaling limit to a fixed request and once if the threshold is over the limit the application scales automatically and load balances the requests.
