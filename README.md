# line-expense-tracker
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)  
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)  
Warmup for hackathon

## usage
`/add <debtor> <lender> <money>` - Add one record.
`/remove <record_id>` - Remove specified record.
`/done <record_id>` - Done specified record. The record will not be shown in summary when it is marked `done`.
`/summary <username>` - Show specified user's summary.
`/list` - Show all records.