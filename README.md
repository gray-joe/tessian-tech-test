# tessian-tech-test

* Part 1: https://github.com/gray-joe/tessian-tech-test/pull/1

* Part 2: The failure in the test is because both the user & chatbot messages are being saved to the history twice. To fix, the yield call in `conversationPersistence` needs to occur after `inmemory_storage` has been updated.

* Part 3: https://github.com/gray-joe/tessian-tech-test/pull/2
