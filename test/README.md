# Test suite

Test suite for MyDollarBot. For phase 1 of Project 2, we are focusing on getting any/all tests created.
The repo given had 1 test case and 0% test coverage. This README explores what methods we can test
and how they integrate with other methods.

## Methods
Defining what tests to make for first iter.
Mainly unit tests and does not include methods that use a bot. 

Once tests are completed, this README will include links per each category/test.

1. listener 
   1. debugger, no test 
2. start_and_menu_command 
   1. bot, no test 
3. command_add 
   1. bot, no test
4. post_category_selection 
   1. bot, no test 
5. post_amount_input 
   1. bot, no input 
6. validate_entered_amount 
   1. testable 
7. write_json 
   1. testable 
8. add_user_record 
   1. testable 
9. read_json 
   1. testable 
10. show_history 
    1. bot, no test 
11. edit1 
    1. bot, no test 
12. edit2 
    1. bot, no test 
13. edit3 
    1. bot, no test 
14. edit_date 
    1. bot, no test 
15. edit_cat 
    1. bot, no test 
16. edit_cost 
    1. bot, no test 
17. command_display 
    1. bot, no test
18. display_total 
    1. bot, no test 
19. calculate_spendings 
    1. testable 
20. getUserHistory 
    1. testable 
21. deleteHistory 
    1. testable 
22. command_delete 
    1. bot, no test 
23. addUserHistory 
    1. testable


## Testable functions
For each function, what method(s) use it, to better understand the scope. 
In the future, these should be kept in mind when creating integration tests.

1. [validate_entered_amount](test/unit/test_validate_entered_amount.py)
   1. post_amount_input
   2. edit_cost
2. write_json
   1. edit_cost
   2. command_delete
   3. post_amount_input
   4. edit_date
   5. edit_cat
3. [add_user_record](test/unit/test_add_user_record.py)
   1. post_amount_input
4. read_json
   1. command_add
   2. command_delete
   3. command_display
   4. edit1
   5. show_history
   6. start_and_menu_command
5. [calculate_spendings](test/unit/test_calculate_spendings.py)
   1. display_total
6. [get_user_history](test/unit/test_get_user_history.py)
   1. command_display
   2. display_total
   3. edit2
   4. edit3
   5. edit_cat
   6. edit_cost
   7. edit_date
   8. show_history
7. [deletHistory](test/unit/test_delete_history.py)
   1. command_delete
8. addUserHistory
   1. **no usages found**