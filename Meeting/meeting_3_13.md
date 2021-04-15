# DataGovernance Sync Up Meeting 

`2020 Mar 13`

## 1 Current State

* Implemented upsert to replace 

* Tested with low volume data flow from FocalPoint
  * Successfully receive data from other microservice
  * Wrtie given governance payload without conflict

* Working on test backfill

## 2 Issues

* Lost Update
  ![Payload From GateWay](./gateway.jpg)
  Timestamp: 23.524-23.588
  ![Payload From Ingestion](./ingestion.jpg)
  Timestamp: 23.474-23.520
  ![Payload From Processing](./processing.jpg)
  Timestamp: 23.531-23/588