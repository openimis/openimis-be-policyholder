from functools import lru_cache
from unittest import TestCase

from policyholder.models import PolicyHolder, PolicyHolderInsuree, PolicyHolderUser
from policyholder.tests import create_test_policy_holder, create_test_policy_holder_insuree, \
    create_test_policy_holder_user


class HelpersTest(TestCase):
    """
    Class to check whether the helper methods responsible for creating test data work correctly.
    """

    def test_create_policy_holder(self):
        policy_holder = self.__create_test_policy_holder()
        db_policy_holder = PolicyHolder.objects.filter(id=policy_holder.id).first()
        self.assertEqual(db_policy_holder, policy_holder, "Failed to create policy holder in helper")

    def test_create_policy_holder_insuree(self):
        policy_holder_insuree = self.__create_test_policy_holder_insuree()
        db_policy_holder_insuree = PolicyHolderInsuree.objects.filter(id=policy_holder_insuree.id).first()

        self.assertEqual(db_policy_holder_insuree, policy_holder_insuree,
                         "Failed to create policy holder insuree in helper")

    def test_create_policy_holder_user(self):
        policy_holder_user = self.__create_test_policy_holder_user()
        db_policy_holder_user = PolicyHolderUser.objects.filter(id=policy_holder_user.id).first()

        self.assertEqual(db_policy_holder_user, policy_holder_user,
                         "Failed to create policy holder insuree in helper")

    def test_create_policy_holder_custom_params(self):
        policy_holder = self.__create_test_policy_holder(custom=True)
        db_policy_holder = PolicyHolder.objects.filter(id=policy_holder.id).first()

        self.assertEqual(db_policy_holder.code, self.__custom_policy_holder_params['code'])
        self.assertEqual(db_policy_holder.trade_name, self.__custom_policy_holder_params['trade_name'])
        self.assertEqual(db_policy_holder.activity_code, self.__custom_policy_holder_params['activity_code'])

    def test_create_policy_holder_insuree_custom_params(self):
        policy_holder_insuree = self.__create_test_policy_holder_insuree(custom=True)
        db_policy_holder_insuree = PolicyHolderInsuree.objects.filter(id=policy_holder_insuree.id).first()
        params = self.__custom_policy_holder_insuree_params
        self.assertEqual(db_policy_holder_insuree.policy_holder, params['policy_holder'])
        self.assertEqual(db_policy_holder_insuree.version, 1)

    def test_create_policy_holder_user_custom_params(self):
        policy_holder_user = self.__create_test_policy_holder_user(custom=True)
        db_policy_holder_user = PolicyHolderUser.objects.filter(id=policy_holder_user.id).first()
        params = self.__custom_policy_holder_user_params
        self.assertEqual(db_policy_holder_user.policy_holder, params['policy_holder'])
        self.assertEqual(db_policy_holder_user.is_deleted, True)

    @property
    @lru_cache(maxsize=2)
    def __custom_policy_holder_params(self):
        return {
            'code': 'CustomCode',
            'trade_name': 'CustomTradeName',
            'activity_code': -1,
            }

    @property
    @lru_cache(maxsize=2)
    def __custom_policy_holder_insuree_params(self):
        return {
            'policy_holder': self.__create_test_policy_holder(custom=True),
        }

    @property
    @lru_cache(maxsize=2)
    def __custom_policy_holder_user_params(self):
        return {
            'policy_holder': self.__create_test_policy_holder(custom=True),
            'is_deleted': True
        }

    def __create_test_instance(self, function, **kwargs):
        if kwargs:
            return function(**kwargs)
        else:
            return function()

    def __create_test_policy_holder(self, custom=False):
        custom_params = self.__custom_policy_holder_params if custom else {}
        return self.__create_test_instance(create_test_policy_holder, custom_props=custom_params)

    def __create_test_policy_holder_insuree(self, custom=False):
        custom_params = self.__custom_policy_holder_insuree_params if custom else {}
        return self.__create_test_instance(create_test_policy_holder_insuree, custom_props=custom_params)

    def __create_test_policy_holder_user(self, custom=False):
        custom_params = self.__custom_policy_holder_user_params if custom else {}
        return self.__create_test_instance(create_test_policy_holder_user, custom_props=custom_params)



