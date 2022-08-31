# Google Drive

## Introduction
Google drive is a **file storage** and **synchronization** service that help you store various files in the cloud. Its most important features are:
* upload files
* download files
* file sync across multiple devices
* See revisions, i.e. the history of modification
* Share files with others
* send a notification when a file is edited, deleted or shared with you

It should support multi-device, multi-platform. It should support all file types. And the files should be encrypted. Besides, the system should also satisfying these non-functional requirements:
* Reliability: data loss is unacceptable
* Fast sync speed; reduce unnecessary network bandwidth(e.g. p2p download software)
* Low bandwidth usage
* Scalability
* High availability: ability to provide service even some servers are offline, slow down.

## APIs

### Upload a file
* Simple upload, when file size is small 5MB or less
* Resumable upload, when files size is large, there is high chance of network interruption.
```
PUT /files
uploadType=<simple|resumable>
request body: data
```

Resumable upload consists 3 high-level steps:
1. Send the initial request and retrieve retrieve the resumable session URI
2. Upload the data and monitor upload state
3. resume the upload if disturbed(send a PUT request to the resumable URI session again, and get the offset from the server to resume)

### Download a file
```
GET /files/download
path=<path to the file>
```

### Get file revisions
API to retrieve the revision history of a file
```
GET /files/list_revisions
limit=<maximum number of revisions to return>
path=<path to the file>
```

## Architecture

First, to suffice the essential goal, we need
* A web server processing request such as upload, download
* A database persisting the metadata such as user data, file info, device info and so on.
* A storage system storying the files. We can store the files in S3. S3 supports smae-region and cross-region replication, and redundant files are stored in multiple regions to guard against data loss and ensure availability.

Except that, we also need following componets:
* Block servers: the client upload file to block server and it split the file into several blocks, each with a unique hash value, stored in metadata database. Each block is treated as an independent object and stored in S3. When download, the block server joined blocks to reconstruct a file. Dropbox set the max size of block to 4MB.
* notification service: notifies relevant clients some event happends and triggers action at client side
* offline backup queue: store the event when client is offline.

To add scalebility, we can also add 
* load balancer for the web server
* cache for metadata cache
* cold storage for inactive data.

### Block server

To optimize the amount of network traffic being transmitted, we can:
* Delta Sync: when modifying a file, only modified blocks are synced
* Compression. Compress blocks can significant reduce the data size.

Also, split the files into block enable the paralell processing. Given a file, we can split it into independent blocks and let it go through the pipeline(compress, encrypt, and store to cloud storage). 

### Notification service

To maintain file consistency, any mutation of a file performed locally needs to be informed to other clients to reduce conflicts. We will adopt **Long polling**(adopted by Dropbox) instead of WS for two reasons:
* Communication for notification service is not bi-directional
* WebSocket is suited for real-time bi-directional communication. But the notifications are sent infrequently with no burst of data.

## Workflow

### Upload
This two request are sent in parallel
* add the metadata
  1. client 1 sends request to add the metadata of the new file
  2. store the new file metadata in metadata DB and change the file upload status to "pending"
  3. notify the notification service that a new file is **being added**
  4. Notification service notifies relevant client a files is being uploaded
* upload the file to cloud
  1. client upload the content to block servers
  2. block server chunk the files into blocks, compress, encrypt the blocks and upload to cloud
  3. Once uploaded, cloud storage triggers upload completion callback
  4. update the metadata DB set status to "uploaded"
  5. notify the notification service that a new file is **uploaded**
  6. Notification service notifies relevant client a files is uploaded

### Download
Download is triggered when a file is added or edited elsewhere. The client can be aware of the change in two ways:
* If it is online, the notification service will notify it
* If it is offline, the event is stored in the backup queue, and when the client go online, it pulls the events and sync the data.

The workflow is:
1. The client is aware of the change, and send a fetch request to the API server to fetch metadata of the change(like the latest file version)
2. Once receive the metadata, it sends requests to block servers to download blocks
3. Block servers download the blocks from the cloud and reconstuct the file.
4. clients download the file

## Other Optimization

### Save storage space

### Failure handling
