## Objective:
Showcase of solutions using open data for Salone

## Concept:
Enable the citizens of Sierra Leone to easily and conveniently access details on health facilities close to them.

## Data Source:
http://www.slbr.sl/api/v1/slbiz/health.json
### Data break-down:
* 10 unique cities
* 251 unique street addresses
* 11 unique districts


## Technical Project Description:
### Customer Journey
* User sends SMS with their street address to a pre-defined phone number.
* System finds all health facilities matching the user’s address (from data source API)
* System ranks the top 2 or 3 results and sends the facilities’ details to the user via SMS

### Components:
* SMS listener web service
  * Receives user message from Twilio
  * Queues request to RabbitMQ
* RabbitMQ consumer
  * Consumes user request from queue
  * Process request
  * Send SMS response
  * Persist request details
