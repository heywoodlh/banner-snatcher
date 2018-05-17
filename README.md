## banner-snatcher

```
❯ ./banner-snatcher.py --help
usage: banner-snatcher.py [-h] {scan} ...

Python program that snatches banners of accessible ports

positional arguments:
  {scan}      sub-command help
    scan      scan host

optional arguments:
  -h, --help  show this help message and exit
```

```
❯ ./banner-snatcher.py scan --help
usage: banner-snatcher.py scan [-h] --host HOST [HOST ...] -p PORT [PORT ...]
                               [-o FILE] [-q]

optional arguments:
  -h, --help            show this help message and exit
  --host HOST [HOST ...]
                        host(s) to scan
  -p PORT [PORT ...], --port PORT [PORT ...]
                        port(s) to scan
  -o FILE, --outfile FILE
                        output to file
  -q, --quiet           suppress output
```
