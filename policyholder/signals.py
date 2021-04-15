from django.db.models import Q
from payment.apps import PaymentConfig
from payment.models import Payment
from .apps import PolicyholderConfig
from .models import PolicyHolderUser


def append_policy_holder_filter(sender, **kwargs):
    # OFS-257: Create dynamic filters for the payment mutation
    user = kwargs.get("user", None)
    additional_filter = kwargs.get('additional_filter', None)
    if "policyHolder" in additional_filter:
        # then check perms
        print("before checking payment perms")
        if user.has_perms(PaymentConfig.gql_query_payments_perms) or user.has_perms(PolicyholderConfig.gql_query_payment_portal_perms):
            print("perms ok")
            ph_id = additional_filter["policyHolder"]
            # check if user is linked to ph in policy holder user table
            type_user = f"{user}"
            # related to user object output (i) or (t)
            # check if we have interactive user from current context
            print(type_user)
            print("check type user")
            if '(i)' in type_user:
                print("yes, interactive user")
                print(user.i_user.id)
                print(user.i_user)
                print(user.uuid)
                ph_user = PolicyHolderUser.objects.filter(Q(policy_holder__id=ph_id, user__id=user.i_user.id)).first()
                print("check ph user exist")
                print(ph_user)
                if ph_user:
                    return Q(
                        payment_details__premium__contract_contribution_plan_details__contract_details__contract__policy_holder__id=ph_id
                    )