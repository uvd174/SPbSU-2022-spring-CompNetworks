# Setup Guide
## System requirements
* Python 3 (3.9.7 will definitely work).

## Run the app
`python simple_mail_sender.py <destination_address> <format> <content_file>`

The message in the specified `format` with the content from the `content_file` 
will be sent at the `destination_address`. `format` is either `txt` or `html`.

`python hand-made_mail_sender.py <destination_address> <content_file>`

The message with the content from the `content_file` will be sent at the `destination_address`.
If the file is in the .jpg format, an image will be sent.

## Proof of work

![proof image](it_works.png)