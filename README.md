# nginx Hello World sandbox

I want to securely serve things to the public internet. `nginx` is a very commonly used tool for this, but I don't have much experience using `nginx`, so I want to learn how to use `nginx` to do regular `nginx`y things. In this repo, I'm going to start with hello world and incrementally build on that, adding the code needed to answer one "How do I do x" question per branch.

## "How do I do X" roadmap
1. How do I serve a static "hello world"?
2. How do I log requests received as well as info about the requester?
3. How do I serve a site that takes input and returns an output based on the input?
4. How do I serve https responses instead of http?
5. How do I configure the server to only respond to specific IP addresses?
6. ... more to be added

# Things learned

## **nginx.conf**: the config file
 The way nginx and its modules work is determined in the configuration file. By default, the configuration file is named nginx.conf and placed in the directory /usr/local/nginx/conf, /etc/nginx, or /usr/local/etc/nginx. In a `nginx.conf` file, users define **directives** (simple or block).
* Simple directives consist of a name and parameters separated by spaces and terminated with a semicolon.
* Block directives start with a name and then curly braces create a context for other directives (of either kind).

The main context will typically include (at least?) block directives named `events` and `http`.
* The `events` directive will often just have empty brackets for simple applications.
* The `http` directive will typically include a `server` block directive that can define things like:
    * Which port(s) should the server `listen` to?
        * Example for the http port: `listen 80` (IP4) or `listen [::]80` (IP6)
    * What response should be served at the base URL?
	* Example: `index /path/to/index.html``
    * What response should be served at URLs for files?
        * Example for `/`: `location / { try_files $uri $uri/ =404; }`
        * This tells nginx to serve a file if one exists at the given `uri`, otherwise return 404.

# "How do I do X" running notes

## How do I serve a static "hello world" site?

(First, roll back to the merge commit for the first merged PR)

1) Start up the system via `docker compose up`.
2) Go to [http://127.0.0.1](http://127.0.0.1) (or http://whatever-your-host-ip-is, if you aren't running it on your local machine)./

You'll see the static html page from `/server/index.html`.

## How do I log incoming requests and requestor metadata?

By default, nginx will output information to the console about requests as those requests come in. These are presented in nginx's default `log_format`, which is named `combined`. You can define other formats with other variables listed [here](https://nginx.org/en/docs/http/ngx_http_log_module.html#log_format).

You can direct these logs to file by using the `access_log` directive. Using this logging scheme, you'll have to modify the docker-compose.yml file to define a volumn (mount point) for the nginx service. This could get cumbersome if files become large, and it does involve tying the system to a specific location in a file system, so it may be desirable to output to console (where it will be captured by docker's logs) and configure log retention specs in the docker-compose.yml file.

### Using docker to handle nginx logs

You might want to define a `log_format` that outputs logs to a json compatible format (as shown in the second PR's `/server/nginx.conf` file's `http` directive block), and add `access_log` and `error_log` directives passing stdout (`/dev/stdout`) and strerr (`/dev/stderr`) to that `json` format. It's not strictly necessary to output logs in a json format, but it will make it a lot easier to extract json records later.

This is enough to get nginx logs captured by Docker's logging system, but you should add a `logging` section to your service that defines the max size for a log file (e.g., `max-size: "10m"`) and the max number of log files for that service (e.g., `max-file: "5"`).

Here is the command to view logs for the `docker-compose.yml` service named "server".

```bash
docker compose logs server
```

## How do I serve a site that accepts inputs and responds

There are many tools for building a web application. Python's Flask is one of the easiest, and this addition implements an app that accepts a json input then returns that input in a json formatted output.

```bash
curl -X POST http://127.0.0.1/process -H "Content-Type: application/json" -d '{"input":"Hello, World!"}'
{"response":"Processed input: Hello, World!"}
```

On the nginx side, we'll use directives from the [proxy module](http://nginx.org/en/docs/http/ngx_http_proxy_module.html), specifically `proxy_pass` and `proxy_set_header` to configure the server to act as a reverse proxy.
* `proxy_pass` lets you set the protocol (eg http, https, ftp, etc) and address of the proxied server.
* `proxy_set_header` lets you define the information included in the request header. You can specify the host, the client IP address, SSL cert, host to forward to, etc. The information provided should be limited to just what the application needs.
