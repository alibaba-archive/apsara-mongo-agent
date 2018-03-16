import unittest
from mongo_testcases.test_entry_point import TestEntryPoint


if __name__ == "__main__":
    suite = unittest.TestSuite()

    tests = [TestEntryPoint("test_super_account_create"), TestEntryPoint("test_system_account_create"),
             TestEntryPoint("test_lockins_diskfull"), TestEntryPoint("test_unlockins_diskfull"),
             TestEntryPoint("test_health_check"), TestEntryPoint("test_flush_params")]
    suite.addTests(tests)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
