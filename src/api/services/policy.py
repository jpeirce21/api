from _main_.utils.massenergize_errors import MassEnergizeAPIError
from _main_.utils.massenergize_response import MassenergizeResponse
from _main_.utils.common import serialize, serialize_all
from api.store.policy import PolicyStore
from _main_.utils.context import Context

class PolicyService:
  """
  Service Layer for all the policies
  """

  def __init__(self):
    self.store =  PolicyStore()

  def get_policy_info(self, policy_id) -> (dict, MassEnergizeAPIError):
    policy, err = self.store.get_policy_info(policy_id)
    if err:
      return None, err
    return serialize(policy, full=True), None

  def list_policies(self, policy_id) -> (list, MassEnergizeAPIError):
    policy, err = self.store.list_policies(policy_id)
    if err:
      return None, err
    return serialize(policy), None


  def create_policy(self, community_id, args) -> (dict, MassEnergizeAPIError):
    policy, err = self.store.create_policy(community_id, args)
    if err:
      return None, err
    return serialize(policy), None


  def update_policy(self, policy_id, args) -> (dict, MassEnergizeAPIError):
    policy, err = self.store.update_policy(policy_id, args)
    if err:
      return None, err
    return serialize(policy), None

  def delete_policy(self, policy_id) -> (dict, MassEnergizeAPIError):
    policy, err = self.store.delete_policy(policy_id)
    if err:
      return None, err
    return serialize(policy), None

  def copy_policy(self, policy_id) -> (dict, MassEnergizeAPIError):
    policy, err = self.store.copy_policy(policy_id)
    if err:
      return None, err
    return serialize(policy), None

  def list_policies_for_community_admin(self, context, community_id) -> (list, MassEnergizeAPIError):
    policies, err = self.store.list_policies_for_community_admin(context, community_id)
    if err:
      return None, err
    return serialize_all(policies, full=True), None


  def list_policies_for_super_admin(self, context) -> (list, MassEnergizeAPIError):
    policies, err = self.store.list_policies_for_super_admin(context)
    if err:
      return None, err
    return serialize_all(policies, full=True), None
