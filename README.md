# line-expense-tracker
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)  
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)  

## usage
`/add <debtor> <lender> <money>` - Add one record.  
`/remove <record_id>` - Remove specified record.  
`/remove_all [filter]` - Remove all records.  
`/done <record_id>` - Done specified record. The record will not be shown in summary when it is marked `done`.  
`/done_all [filter]` - Done all records.  
`/summary <username>` - Show specified user's summary.  
`/list [filter]` - Show all records.  
`/list_done [filter]` - Show all done records.  
`/list_undone [filter]` - Show all undone records.
