# NZTA-GraphRAG
Graph Retrieval Augmemed generative chatbot prototype built for NZTA as use case. 


# How to set up chrome driver for selenium crawler
## Download chrome 

https://support.google.com/chrome/answer/95346?hl=en&co=GENIE.Platform%3DDesktop

## Download Chrome Driver (Same version as Chrome you downloaded)

1. Download the driver from the link bellow
You will most likely be using one of this versions of chrome

https://googlechromelabs.github.io/chrome-for-testing/

2. Copy the executable  (Windows: chromedriver.exe, Mac: chromedriver) to the directory  'driver' in the repository.

3. If on a mac the following needs to be set into the path for the driver to work

```{bash}
sudo xattr -d com.apple.quarantine "/path/to/driver/executable/chromedriver"
```
