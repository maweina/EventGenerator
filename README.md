# EventGenerator
The Event Generator is a utility which allows user to easily produce events with user behavior patterns embedded. 
The user can easily design and generate events through configuration without having to write any code.

## Input
* attribute_distribution.json defines attribute distributions to control generated events.
* patterns.json defines user behavior patterns to be inserted into events.
* ${attribute}.csv maps real attribute value to encoded representation.
* num_events_per_day indicates the number of events per user per day on average.
* num_days_per_user indicaetes the number of dates on average that the user has access event.

## Output
* events.txt are generated events based on attribute definition and with behavior pattern inserted randomly.
* ${attribute}.pdf are attribute distribution extracted from generated events.
* pattern.txt records where the pattern are inserted. It is used for evaluation.
