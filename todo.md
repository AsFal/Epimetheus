-[ ] Complete the CategoryTree object (Section tree)
-[ ] Find a way to connect this to google Calendar
-[ ] Cleanup code and module things
-[ ] Make a json format for the logs (Could also just implement Tree->JSON)

-[ ] Start exploring the beautiful world of nlp

-[ ] Organize this for real

Log: Date - TimeStart -> TimeEnd # A level zero entry is the log header
    Category: Name -> At level two, the tile is a category and the content is the category name
        Title: Content # Each entry is composed of the title and the content
        Mhmmm: Some text # All further levels down do not have specific nomenclature
            Regardless: Of how deep you go

August 19th todo list
Make LogList DataStructure
-> Make methods to get stuff by date
-> Get report method

Implement the conversion from TextLog to TreeLog

Connect things to the interface

Make Design extensible to accomodate editing other data structures
e.g. the a report edit that also adds to the log
-> Editing always accessses the log of the day, for now only support append to the category
-> Becomes somewhat easy to add that after the fact