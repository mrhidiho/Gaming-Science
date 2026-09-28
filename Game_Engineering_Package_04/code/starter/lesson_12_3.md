# Student contract 12.3: Interfaces, composition and polymorphism

Create interchangeable console and recording renderers behind one small interface. Pass: both satisfy the same contract, tests run without display output, and ownership/destructor behavior is explicit.

1. Write a one-page renderer contract before either implementation.
2. Implement console and recording backends with the same unit ordering and synchronous-borrow policy.
3. Test both through the interface with empty and multiple-unit inputs.
4. Write an architecture decision comparing runtime polymorphism with composition and a static alternative.

## Cases

1. empty input emits no commands
2. two units preserve input order
3. recorded commands own copied data
4. derived cleanup observed through base ownership
5. simulation does not mutate renderer ownership

## Evidence

Interface contract, two backend implementations, shared contract tests and design decision record.

## Transfer

A backend queues rendering asynchronously. Amend the contract to transfer owned command data or guarantee a valid lifetime until completion.
