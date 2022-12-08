# SOLUTION

This is the proposed solution for the Backend Engineering Challenge.
The solution in based over the management of the input stream using ijson. Every json object gets extracted and then mapped to a Pydantic dataclass to enable field validation over types.
A list of Event objects is then passed to the main business logic of the application that will calculate the moving average via the args that are passed by the user.

To initialize the application, first intall all the packages needed to run. Project has been developed using python 3.8.3

```
	pip install requirements.txt
```

To launch the application, open a new terminal and use the following command

```
	python3 main.py --input_file NAME_FILE --window-size WINDOW_SIZE

```

Where NAME_FILE is a string representing the input file to use. For experimental reasons, a file named "input.json" is provided to use with the app inside "example_files" folder.

# EVENTUAL IMPROVEMENTS

In the current state, the application is not really suited for managing large JSON input files. A possibile solution to this could be to use libraries such as pandas to manage data in a different way, but the optimal solution should be to associate an Elasticsearch instance to the application, in which the input entries should be stored and then queried to retrieve the moving average

# Backend Engineering Challenge

Welcome to our Engineering Challenge repository 🖖

If you found this repository it probably means that you are participating in our recruitment process. Thank you for your time and energy. If that's not the case please take a look at our [openings](https://unbabel.com/careers/) and apply!

Please fork this repo before you start working on the challenge, read it careful and take your time and think about the solution. Also, please fork this repository because we will evaluate the code on the fork.

This is an opportunity for us both to work together and get to know each other in a more technical way. If have some doubt please open and issue and we'll reach out to help.

Good luck!

## Challenge Scenario

At Unbabel we deal we a lot of translation data. One of the metrics we use for our clients' SLAs is the delivery time of a translation.

In the context of this problem, and to keep things simple, our translation flow is going to be modeled as only one event.

### _translation_delivered_

Example:

```json
{
    "timestamp": "2018-12-26 18:12:19.903159",
    "translation_id": "5aa5b2f39f7254a75aa4",
    "source_language": "en",
    "target_language": "fr",
    "client_name": "easyjet",
    "event_name": "translation_delivered",
    "duration": 20,
    "nr_words": 100
}
```

## Challenge Objective

Your mission is to build a simple command line application that parses a stream of events and produces an aggregated output. In this case, we're instered in calculating, for every minute, a moving average of the translation delivery time for the last X minutes.

If we want to count, for each minute, the moving average delivery time of all translations for the past 10 minutes we would call your application like (feel free to name it anything you like!).

    unbabel_cli --input_file events.json --window_size 10

The input file format would be something like:

    {"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 20}
    {"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 31}
    {"timestamp": "2018-12-26 18:23:19.903159","translation_id": "5aa5b2f39f7254a75bb33","source_language": "en","target_language": "fr","client_name": "booking","event_name": "translation_delivered","nr_words": 100, "duration": 54}

The output file would be something in the following format.

```
{"date": "2018-12-26 18:11:00", "average_delivery_time": 0}
{"date": "2018-12-26 18:12:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:13:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:14:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:15:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:16:00", "average_delivery_time": 35,5}
{"date": "2018-12-26 18:17:00", "average_delivery_time": 35,5}
{"date": "2018-12-26 18:18:00", "average_delivery_time": 35,5}
{"date": "2018-12-26 18:19:00", "average_delivery_time": 35,5}
{"date": "2018-12-26 18:20:00", "average_delivery_time": 35,5}
{"date": "2018-12-26 18:21:00", "average_delivery_time": 35,5}
{"date": "2018-12-26 18:22:00", "average_delivery_time": 31}
{"date": "2018-12-26 18:23:00", "average_delivery_time": 31}
{"date": "2018-12-26 18:24:00", "average_delivery_time": 58}
```

#### Notes

Before jumping right into implementation we advise you to think about the solution first. We will evaluate, not only if your solution works but also the following aspects:

-   Simple and easy to read code. Remember that [simple is not easy](https://www.infoq.com/presentations/Simple-Made-Easy)
-   Include a README.md that briefly describes how to build and run your code, as well as how to test it
-   Be consistent in your code.

Feel free to, in your solution, include some your considerations while doing this challenge. We want you to solve this challenge in the language you feel most confortable with. Our machines run Python (3.7.x or higher) or Go (1.16.x or higher). If you are thinking of using any other programming language please reach out to us first 🙏.

Also if you have any problem please **open an issue**.

Good luck and may the force be with you
