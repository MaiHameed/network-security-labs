Restrictions:
- Images are confined to exactly 100x100px to reduce image download time
- Images to send the end user are stored in the respective [client|server]ImageRepo
- If a user receives a message, it is stored in their image repo under the name `downloaded.jpg`. Each subsequently downloaded image will overwrite the file
- App cannot handle an invalid input for image sending, errors are not dealt with. Fix if I have time
