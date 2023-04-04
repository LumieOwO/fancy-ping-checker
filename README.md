# fancy-ping-checker
This is a module for stress testing a website by sending multiple HTTP GET requests to the specified URL using multiple threads or processes. The default maximum number of threads is set to 500, but you can modify this by changing the MAX_THREADS variable.

To use this module, import it into your Python script and create an instance of the StressTester class with the URL of the website you want to stress test. Then, call the start method of the StressTester instance to start the stress test.

The StressTester class will send HTTP GET requests to the specified URL using multiple threads or processes, depending on your system's capabilities. Each thread or process will send requests continuously until the stress test is stopped by pressing Ctrl+C.

If the specified URL uses the HTTP protocol, the default port is 80. If the URL uses the HTTPS protocol, the default port is 443. You can modify the URL or protocol by changing the URL variable.

Example usage:

```python
from main import StressTester

if __name__ == "__main__":
    url = "https://www.example.com"
    stress_tester = StressTester(url)
    stress_tester.start()
```
