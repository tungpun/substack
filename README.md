# Substack

substack is an open source penetration testing tool that can discover sub-domains from a specific domain. This tool is based on the idea of listing search engine results. [Sublist3r](https://github.com/aboul3la/Sublist3r) also implemented this idea, but it was really hard to develop more features, so we decided to write a tool for ourselves.

Features
----
- Discover sub-domains
- Discover openned ports

Installation 
----
```
pip -r requirements.txt
```

Usage
----

```
substack -d google.com
```

Use with Slack

* Create a SLACKBOT, set name as `substack`
* Then run the command:

```
export SLACK_BOT_TOKEN=<your_slack_bot_token>
python slackbot.py
```

Credits
----
- [Sublist3r](https://github.com/aboul3la/Sublist3r) - An anwesome tool, it inspires us to build substack

