#  REST API Endpoints
This section provides a detailed list of avaliable endpoints in Visualizer REST API.

## Start visualization
  Start the visualization of a running application.

* **URL**: `/visualizing`
* **Method:** `POST`

* **JSON Request:**
	* ```javascript
	  {
	     username : [string],
	     password : [string],
	     plugin: [string],
	     plugin_info : {
	         ...
	     }
	  }
	  ```
* **Success Response:**
  * **Code:** `202` <br /> **Content:** 
	  * ```javascript
	    {
	       job_id : [string]
	    }
		```
		
* **Error Response:**
  * **Code:** `400 BAD REQUEST` and `401 UNAUTHORIZED`<br />


## Stop visualization
  Stop the visualization of a running application.

* **URL**: `/visualizing/:id/stop`
* **Method:** `PUT`

* **JSON Request:**
	* ```javascript
	  {
	     username : [string],
	     password : [string]
	  }
	  ```
* **Success Response:**
  * **Code:** `204` <br />
		
* **Error Response:**
  * **Code:** `400 BAD REQUEST` and `401 UNAUTHORIZED`<br />

## Get visualization URL
  Returns the url of the visualizer of the job.

* **URL**: `/visualizing/:id`
* **Method:** `GET`
* **Success Response:**
  * **Code:** `200` <br /> **Content:** 
	  * ```javascript
	    {
	       url : [string]		 
	    }
		```

## Add cluster
  Add a new cluster reference into the Asperathos Visualizer section

* **URL**: `/visualizing/cluster`
* **Method:** `POST`
* **JSON Request:**
	* ```javascript
		{
			"user" : [string],
			"password" : [string],
			"cluster_name" : [string],
			"cluster_config" : [string]
		}
* **Success Response:**
  * **Code:** `220` <br /> **Content:** 
	  * ```javascript
	    {
			"cluster_name" : [string],
			"status": [string],
			"reason": [string]
	    }
		```

## Add certificate
  Add a certificate in the a cluster reference into the Asperathos Visualizer section

* **URL**: `/visualizing/cluster/:cluster_name`
* **Method:** `POST`
* **JSON Request:**
	* ```javascript
		{
			"user" : [string],
			"password" : [string],
			"certificate_name" : [string],
			"certificate_content" : [string]
		}
* **Success Response:**
  * **Code:** `220` <br /> **Content:** 
	  * ```javascript
	    {
			"cluster_name" : [string],
			"certificate_name" : [string],
			"status": [string],
			"reason": [string]
	    }
		```

## Delete cluster
  Delete a cluster reference of the Asperathos Visualizer section

* **URL**: `/visualizing/cluster/:app_id/delete`
* **Method:** `POST`
* **JSON Request:**
	* ```javascript
		{
			"user" : [string],
			"password" : [string]
		}
* **Success Response:**
  * **Code:** `220` <br /> **Content:** 
	  * ```javascript
	    {
			"cluster_name" : [string],
			"status": [string],
			"reason": [string]
	    }
		```

## Delete certificate
  Delete a certificate of a cluster reference in the Asperathos Visualizer section

* **URL**: `/visualizing/cluster/:cluster_name/certificate/:certificate_name/delete`
* **Method:** `POST`
* **JSON Request:**
	* ```javascript
		{
			"user" : [string],
			"password" : [string]
		}
* **Success Response:**
  * **Code:** `220` <br /> **Content:** 
	  * ```javascript
	    {
			"cluster_name" : [string],
			"certificate_name" : [string],
			"status": [string],
			"reason": [string]
	    }
		```

## Active cluster
  Start to use the informed cluster as active cluster in the Asperathos Visualizer section.

* **URL**: `/visualizing/cluster/:app_id`
* **Method:** `POST`
* **JSON Request:**
	* ```javascript
		{
			"user" : [string],
			"password" : [string]
		}
* **Success Response:**
  * **Code:** `220` <br /> **Content:** 
	  * ```javascript
	    {
			"cluster_name" : [string],
			"status": [string],
			"reason": [string]
	    }
		```
