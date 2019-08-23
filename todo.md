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


August 20th, TODO list for future
-> Modify SectionTree to accomodate get all titles/conten by section
-> Use that modification to create the TreeLogSection data structure
-> Implement the subSection method in the LogSection data structure
-> Propogate the modifications to the cli
-> Add a report option for the cli
-> Publish v0 once everything seems tested, plan for next step


FEATURES
-> The interface should have a tab complete feature
-> No log should be added to logs.txt if the log only contains a root
-> fish out all of the todos from the code
-> A button to see more suggestions, or a shortcut
