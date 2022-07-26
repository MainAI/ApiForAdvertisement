# ApiForAdvertisement

* Start Database:  
```docker-compose up db```  
  
  
* Install dependencies:    
```pip install requirements.txt```
  

* Run script ```app.py```
  

* Requests example ```clients.py```
  

Option use pgadmin:   
 ```docker-conpose up dbadmin```
 
 Alembic for migration
    
 Description requests method:    
 1. GET all advertisement:    
 *http://localhost:5000/advertisement/*
 1. POST advertisement:     
 *http://localhost:5000/advertisement/* +    
 *json {"title","description","owner"}* information
 1. GET, PATCH, DELETE one advertisement, use id_adv:     
 *http://localhost:5000/advertisement/<id_adv>*

