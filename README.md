Logger library that helps applications log messages.
● Client/application make use of logger library to log messages to a sink
  ● Message
    ○ has content which is of type string
    ○ has a level associated with it
    ○ is directed to a destination (sink)
    ○ has namespace associated with it to identify the part of application that sent the message
  ● Sink
    ○ This is the destination for a message (eg text file, database, console, etc)
    ○ Sink is tied to one or more message level
    ○ one or more message level can have the same sink
● Logger library
  ○ Accepts messages from client(s)
  ○ Routes messages to appropriate sink
  ○ Supports following message level: DEBUG, INFO, WARN, ERROR, FATAL
  ○ enriches message with current timestamp while directing message to a sink
  ○ requires configuration during setup
● Sending messages
  ○ Sink need not be mentioned while sending a message to the logger library.
  ○ A message level is tied to a sink.
  ○ You specify message content, level and namespace while sending a message
  ○ logger library to allow users to provide their own implementation of sink
  ○ Implementation of the text file sink and console sink.
  ○ Auto-rotate for log files based on file size. Compress previous log files.

