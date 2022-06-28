# Backend Engineering Challenge:
Hey Team! My idea for the solution was to build a Batch Process with Spring because from my experience this type of problems we solved via Jobs.
## Run the Application [Apache CLI or Spring Batch]

Apache CLI Documentation:
https://commons.apache.org/proper/commons-cli/usage.html
Spring Batch Documentation
https://spring.io/projects/spring-batch

In order to run the application via Spring Batch you will need to add the input file under resources and add the argument of the window size


## Sequence of Execution

![alt text](images/diagramOfProcess.png)


Use Case:
* If the Object is not like **this** it would be added to a bad record list and for future _reporting_ or _control_
```
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

## Reading Json File:
In order to read the JSON file and sanitize the objects I have to work with Generics and with the Class **JsonEventItemReader**
```
    @Bean
    public JsonItemReader<Set<EventRecordVo>> eventTranslationDeliveredReader() {
    FastJsonItemRead<Set<EventRecordVo>> jsonReader = new FastJsonItemRead<>(new TypeReference<Object[]>() {}.getType());
        ClassPathResource resource = new ClassPathResource("event.json");
        return new JsonItemReaderBuilder<Set<EventRecordVo>>()
                .resource(resource)
                .jsonObjectReader(jsonReader)
                .name("EventTranslationDelivered")   
                .build();
    }
``` 
## Processing step 
 Every successful record will get to the Processor, and it will calculate the Average Delivery Time
```








```
## Writer step                                                                                         
 It would be the responsible to write the output of the successful records and generate a file for future analyze of the Bad Records
```                                                                                                        
                                                                                                           
                                                                                                           
                                                                                                           
                                                                                                           
                                                                                                           
                                                                                                           
                                                                                                           
                                                                                                           
```                                                                                                        
