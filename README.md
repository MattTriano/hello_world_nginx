# nginx Hello World sandbox

I want to securely serve things to the public internet. `nginx` is a very commonly used tool for this, but I don't have much experience using `nginx`, so I want to learn how to use `nginx` to do regular `nginx`y things. In this repo, I'm going to start with hello world and incrementally build on that, adding the code needed to answer one "How do I do x" question per branch.

## "How do I do X" roadmap
1. How do I serve a static "hello world"?
2. How do I serve a site that takes input and returns an output based on the input?
3. How do I serve https responses instead of http?
4. How do I configure the server to only respond to specific IP addresses?
5. ... more to be added

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

