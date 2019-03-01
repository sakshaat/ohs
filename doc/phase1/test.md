# Test

Our team is determined to follow a proper TDD approach to this project. By doing so, we are guaranteed to:
- Properly consider what is expected from our code
- Identify any errors/problems early on
- Allow the design to evolve and adapt to our changing understanding of the problem
- Have a cleaner interface

All our tests are written in pytest along with the pytest-cov plugin to produce detailed coverage reports, the tests can easily be run by simpy typing "make tests". All members are expected to run the tests before pushing any file to the repository, this ensures that all committed code is working and does not break any other part of the application. 

While unit testing is important, so is API testing. We have also built a wide array of API tests  on top of a solid foundation of unit tests to test application logic at a level that unit tests cannot. API tests can be split up into specific categories, for example:
- Contract Tests: to validate that the contract is written correctly and can be consumed by a client;
- Component Tests: take the individual methods available in the API and test each one of them in isolation;
- Scenario Tests: to understand if defects might be introduced by combining different data points together.

This allows to build a solid framework for identifying defects at multiple layers of your application.
 
And finally, one of our members is interested in gaining experience in automated testing frameworks and plans on setting it up with our repository to ensure a smoother testing.