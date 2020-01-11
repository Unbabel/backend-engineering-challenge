# Backend Engineering Challenge - Solution by Daniel Da Silva

I opted to make a solution in Java using Spring boot as a CLI app.
This solutions was think of to make it clean and easy to reuse, for example:
- in a case that unbabel wants to read or write into a kafka topic, it would be pretty easy just to extends the proper
classes and write down the new logic without affecting the current structure.

## Build and run

To build and run the CLI app, you should run this command:
    
    ./gradlew bootRun --args="--window_size=10 --input_file=events.json"
	
To build and run the unit tests you should use this command:

	./gradlew test

#### Notes

- While running the app it should never throws an exception, instead it's logged.
- You can check the output in the root of the project as a file "output.json"
- If you want, you could set the level of logs wanted while running the app in the application.properties files under src/main/resources

These are the validations that I implemented:

- Window size must always be a positive int
- Input file must always be an existing and readable file
- If a line of the input has a bad syntax, the event would be ignored and proceed with the next one.