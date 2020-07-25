# konachan_image_downloader
Download all high quality images from the given keyword in konachan.

Support transferring with interruption resuming capability.

Require python 2.7.

### Usage

Edit the *url* variable in konachan_url_version.py and run it using python 2.7. E.g:

```python
url = 'http://konachan.com/post?tags=eden'
python2 konachan_url_versison.py 
```

It will download all images (png prefered) and save them into a folder named eden in the same location.

Set *recaplink* to false to resume an interrputed downloading.

