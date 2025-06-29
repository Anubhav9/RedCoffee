## Change Log for RedCoffee

### Version 2.16 ( Released on June 29,2025):
* Inclusion of a new command : `redcoffee diagnose` - This does a sanity check whether the required infra/parameters needed by RedCoffee is up and running or not. This checks for SonarQube Connectivity and validity / authenticity of the provided SonarQube Token (which ideally should be the SonarQube user token). The user can get a hint of what is wrong with RedCoffee post running this command.
* Inclusion of a new command : `redcoffee support`- This encourages the end user to create a Github Issue in case they feel something is wrong with RedCoffee and needs an urgent attention. Alternatively, the maintener's email has been given as well , incase , someone wants to reach out directly.
* Addition of a new ASCII Banner. Users will be greeted with this ASCII art when they run any commands of RedCoffee.
* Bug Fix - Saw errors on Sentry regarding Invalid Path Supplied. This was happening because when no path was supplied, RedCoffee was trying to create reports in Downloads Directory. However, we were not checking if Downloads directory exists or not. Added the code to create a new directory called `redcoffee-reports` where RedCoffee reports will be stored in case user does not supply the required path.
* Minor Bug Fix - An if condition in the code was incorrect. This was however not creating any issues. But fixed it just in case.


### Version 2.15 ( Released on May 25,2025 )
* No Changes from a Customer POV. The Code / Repository structure has been modified to segregate components and follow the Single Responsibility Principle.
* Better adherence to PEP8 structure.
* Github Actions file added to auto-publish the changes to Pypi and Trigger test run on every commit.
* Will observe Sentry for potential errors post the code changes


### Version 2.9 (Released on April 26,2025)
* The flags getting used in Click Commands that power the CLI has now been parameterised with field `required` (possible values - True or False) . If the mandatory flags are not passed, CLI execution will throw error then and there itself.
* Bug Resolution - Observed errors coming due to JSON not being unpackaged correctly and duplication API returning no object inside the key `measures`. Handled both these components safely so that execution does not stop midway.
* Unit Test Cases Fixed to match the new function style.

### Version 2.8 (Released on April 5,2025)
* Saw a lot of errors in Sentry as users were passing the path flag incorrectly. Made code changes to handle the same and also added a fallback mechanism which shall prevent any more failures from happening.
* Few errors were reported because the API response did not contain the key `line`. The failure is now being handled properly from this version.
### Version 2.5 (Released on March 8,2025)
* After addition of Sentry logs, I got notified that most of the failures are coming because of Protocol Handling mismatch. I was previously enforcing protocol on my side, now the control has been given to the user. There is an additional fallback option though if the user forgets to add the protocol or makes a mistake.


### Version 2.2 (Released on March 2,2025)
* Addition of Sentry SDK to the codebase. Since RedCoffee is a tool completely running on the client side, I had no way to monitor the logs and fix failures, if any. Addition of Sentry SDK will help me track and fix failures better. Please note that no personal information / token etc is being stored at Sentry side. It just logs failures.
* General Bug Fixes

### Version 1.8 (Released on Feb 16,2025)
* Bug Fix - Code Duplication % was hardcoded to 0. This led to this metric never appearing on the report itself. The bug is fixed in this release. New Table / Section has been added for Code Duplication metrics.

### Version 1.1 (Released on Feb 8,2025)
* Major Version Upgrade - There has been changes in SonarQube API Structure and regarding utilisation of User Tokens. Changes have been made to handle the code changes from SonarQube end.

### Version 0.2 (Released on June 1,2024)
* Initial release for RedCoffee



PS: Please do not ask me why the version numbers are not contigious.
