# Test suite

Test suite for MyDollarBot. For phase 1 of Project 2, we are focusing on getting any/all tests created.
The repo given had 1 test case and 0% test coverage. This README explores what methods we can test
and how they integrate with other methods.

## Methods
Defining what tests to make for first iter.
Mainly unit tests and does not include methods that use a bot. 

Once tests are completed, this README will include links per each category/test.

## Testable functions - Unit Tests
For each function, what method(s) use it, to better understand the scope. 
In the future, these should be kept in mind when creating integration tests.

1. [validate_entered_amount](unit/test_validate_entered_amount.py)
   1. post_amount_input
   2. edit_cost
2. [write_json](unit/test_write_json.py)
   1. edit_cost
   2. command_delete
   3. post_amount_input
   4. edit_date
   5. edit_cat
3. [add_user_record](unit/test_add_user_record.py)
   1. post_amount_input
4. [read_json](unit/test_read_json.py)
   1. command_add
   2. command_delete
   3. command_display
   4. edit1
   5. show_history
   6. start_and_menu_command
5. [calculate_spendings](unit/test_calculate_spendings.py)
   1. display_total
6. [get_user_history](unit/test_get_user_history.py)
   1. command_display
   2. display_total
   3. edit2
   4. edit3
   5. edit_cat
   6. edit_cost
   7. edit_date
   8. show_history
7. [deleteHistory](test/unit/test_delete_history.py)
   1. command_delete
8. addUserHistory
   1. **no usages found**


## Testable functions - bot test


1. [start_and_menu_command](test/bot/test_start_and_menu.py)
   1. bot, as of now basic test to just see if message handlers are created
2. [show_history](test/bot/test_history.py) 
   2. bot, as of now basic test to just see if message handlers are created
      1. test with history, message handler is created
      2. test without history, no message handler created
3. [add](test/bot/test_add.py)
4. [display](test/bot/test_display.py)
5. [edit](test/bot/test_edit.py)
6. [delete](test/bot/test_delete.py)