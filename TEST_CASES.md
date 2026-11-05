RPMS – Test Cases

1. Candidate Management

Test ID| Test Scenario| Expected Result| Actual Result| Status
TC01| Add a new candidate| Candidate should be added successfully| Candidate added successfully| PASS
TC02| View all candidates| Candidate list should be displayed| Candidate list displayed| PASS
TC03| Update candidate details| Candidate details should be updated| Candidate updated successfully| PASS
TC04| Delete a candidate| Candidate should be deleted| Candidate deleted successfully| PASS
TC05| Test invalid candidate ID handling| Candidate not found message should appear| CandidateNotFoundError tested| PASS
TC37| Candidate DAO Add after refactoring| Candidate should be inserted successfully| Temporary candidate created with ID 24| PASS
TC38| Candidate DAO Update after refactoring| Candidate details should be updated| Mobile number updated and original value restored| PASS
TC39| Candidate DAO Delete after refactoring| Candidate should be deleted| Temporary candidate ID 24 deleted successfully| PASS

2. Company Management

Test ID| Test Scenario| Expected Result| Actual Result| Status
TC06| Add a new company| Company should be added| Company added successfully| PASS
TC07| View all companies| Company list should appear| Company list displayed| PASS
TC08| Update company details| Company details should be updated| Company updated successfully| PASS

3. Job Management

Test ID| Test Scenario| Expected Result| Actual Result| Status
TC09| Add a new job| Job should be created| Job created successfully| PASS
TC10| View all jobs| Job list should appear| Job list displayed| PASS
TC11| Update job details| Job details should be updated| Job updated successfully| PASS
TC12| Test invalid job ID handling| Job not found message should appear| JobNotFoundError tested| PASS

4. Application Management

Test ID| Test Scenario| Expected Result| Actual Result| Status
TC13| Apply for an eligible job| Application should be created| Application created successfully| PASS
TC14| Apply for an ineligible job| Application should be blocked| Eligibility check blocked application| PASS
TC15| Apply for the same job twice| Duplicate application should be blocked| DuplicateApplicationError tested| PASS
TC16| Update application status| Application status should be updated| Status updated successfully| PASS
TC40| Eligibility check after refactoring| Eligible candidate should pass eligibility check| All eligibility criteria satisfied for Candidate ID 1 and Job ID 13| PASS
TC41| Duplicate application check after refactoring| Duplicate application should be blocked| Duplicate application detected for Candidate ID 1 and Job ID 13| PASS

5. Interview Management

Test ID| Test Scenario| Expected Result| Actual Result| Status
TC17| Schedule an interview| Interview should be scheduled| Interview scheduled successfully| PASS
TC18| Update interview status| Interview status should be updated| Interview updated successfully| PASS
TC19| View interviews| Interview list should appear| Interview list displayed| PASS

6. Offer Management

Test ID| Test Scenario| Expected Result| Actual Result| Status
TC20| Create an offer| Offer should be created| Offer created successfully| PASS
TC21| Update offer status| Offer status should be updated| Offer status updated successfully| PASS
TC22| View offers| Offer list should appear| Offer list displayed| PASS

7. Placement Management

Test ID| Test Scenario| Expected Result| Actual Result| Status
TC23| Create placement using an accepted offer| Placement should be created| Placement created successfully| PASS
TC24| Update placement status| Placement status should be updated| Placement updated successfully| PASS
TC25| View all placements| Placement list should appear| Placement list displayed| PASS

8. Reports Management

Test ID| Test Scenario| Expected Result| Actual Result| Status
TC26| Generate summary report| Summary should be displayed| Summary report generated| PASS
TC27| Generate candidates by technology report| Technology-wise candidates should appear| Report generated| PASS
TC28| Generate open jobs report| Open jobs should appear| Report generated| PASS
TC29| Generate applications by status report| Status-wise application counts should appear| Report generated| PASS
TC30| Generate company-wise placement report| Company-wise placements should appear| Report generated| PASS
TC31| Generate placed candidates report| Placed candidates should appear| Report generated| PASS
TC32| Generate unplaced candidates report| Unplaced candidates should appear| Report generated| PASS
TC42| Generate all reports after refactoring| All eight reports should work| All eight reports opened and verified| PASS

9. Database and Application Testing

Test ID| Test Scenario| Expected Result| Actual Result| Status
TC33| Connect to MySQL database| Database connection should succeed| Database connected successfully| PASS
TC34| Run main application| Main menu should appear| Main menu displayed| PASS
TC35| Import custom exceptions| All custom exceptions should import| All exceptions imported successfully| PASS
TC36| Write activity log| Activity should be recorded in file| Activity log entries recorded| PASS
TC43| Compile Python files| Python files should compile without syntax errors| 25 Python files compiled successfully| PASS
TC44| Import Model and DAO modules| All modules should import successfully| All Model and DAO imports passed| PASS
TC45| Import Service modules| All service modules should import successfully| All Service imports passed| PASS
TC46| Retrieve candidate records through DAO| Candidate records should be retrieved| 20 records retrieved| PASS
TC47| Retrieve company records through DAO| Company records should be retrieved| 10 records retrieved| PASS
TC48| Retrieve job records through DAO| Job records should be retrieved| 14 records retrieved| PASS
TC49| Retrieve application records through DAO| Application records should be retrieved| 42 records retrieved| PASS
TC50| Retrieve interview records through DAO| Interview records should be retrieved| 22 records retrieved| PASS
TC51| Retrieve offer records through DAO| Offer records should be retrieved| 8 records retrieved| PASS
TC52| Retrieve placement records through DAO| Placement records should be retrieved| 6 records retrieved| PASS
TC53| Test Main Menu and submenus| All management submenus should open| Main Menu and all Nine submenus verified| PASS
TC54| Retrieve summary report through Report DAO| Summary data should be retrieved| Summary report data retrieved successfully| PASS

9. Skills Management

Test ID | Test Scenario | Expected Result | Actual Result | Status
TC55 | Add a new skill | Skill should be added successfully | Skill added successfully | PASS
TC56 | View all skills | Skill list should be displayed | Skill list displayed successfully | PASS
TC57 | Test duplicate skill validation | Duplicate skill should be blocked | Duplicate skill detected successfully | PASS
TC58 | View candidate skills | Candidate skill details should appear | Candidate skills displayed successfully | PASS
TC59 | View job skills | Job skill details should appear | Job skills displayed successfully | PASS
TC60 | Verify skill ID ordering | Skills should be displayed in ID order | Skills displayed in ascending Skill ID order | PASS

---

Note: These test cases document the operations and checks performed during project development and refactoring. Tests that have not been performed are not marked as passed. Previously performed functional tests are recorded separately from post-refactoring verification.