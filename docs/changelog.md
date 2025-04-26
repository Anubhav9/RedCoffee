## Change Log for RedCoffee

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
