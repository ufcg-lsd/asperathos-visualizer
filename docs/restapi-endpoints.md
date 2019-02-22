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