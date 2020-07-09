from _main_.utils.massenergize_errors import NotAuthorizedError, MassEnergizeAPIError
from _main_.utils.massenergize_response import MassenergizeResponse
from _main_.utils.context import Context
from database.models import UserProfile, CommunityMember, Action, Team, UserActionRel, Testimonial, TeamMember, Community
from django.db.models import Q
from sentry_sdk import capture_message

class DownloadStore:

  def __init__(self):
    self.name = "Download Store/DB"


  def _get_user_actions_cells(self, user, actions):
    cells = []
    # create collections with constant-time lookup. VERY much worth the up-front compute.
    user_testimonial_action_ids = set([testimonial.action.id if testimonial.action else None
                                for testimonial in Testimonial.objects.filter(user=user)])
    action_id_to_action_rel = {user_action_rel.action.id: user_action_rel
                                for user_action_rel in UserActionRel.objects.filter(user=user)}

    for action in actions:
      user_action_status = ''
      if action.id in user_testimonial_action_ids:
        user_action_status = 'testimonial'
      else:
        user_action_rel = action_id_to_action_rel.get(action.id, None)
        if user_action_rel:
          user_action_status = user_action_rel.status
      cells.append(user_action_status)
    return cells


  def _get_user_teams_cells(self, user, teams):
    cells = []
    user_team_members = TeamMember.objects.filter(user=user).select_related('team')

    for team in teams:
      user_team_status = ''
      team_member = user_team_members.filter(team=team).first()
      if team_member:
        if team_member.is_admin:
          user_team_status = 'admin'
        else:
          user_team_status = 'member'
      cells.append(user_team_status)
    return cells


  def _all_users_download(self):
    users = UserProfile.objects.filter(is_deleted=False)
    actions = Action.objects.filter(is_deleted=False)
    teams = Team.objects.filter(is_deleted=False)

    columns = ['primary community',
                'secondary community',
                'full_name',
                'preferred_name',
                'email',
                'role'] \
                + [action.title for action in actions] \
                + [team.name for team in teams]

    data = []

    for user in users:

      user_communities = user.communities.all()

      if len(user_communities) > 1:
        primary_community, secondary_community = user_communities[0].name, user_communities[1].name
      elif len(user_communities) == 1:
        primary_community, secondary_community = user_communities[0].name, ''
      else:
        primary_community, secondary_community = '', ''

      row = [primary_community,
            secondary_community,
            user.full_name,
            user.preferred_name if user.preferred_name else '',
            user.email,
            'super admin' if user.is_super_admin else
                'community admin' if user.is_community_admin else
                'vendor' if user.is_vendor else
                'community member']

      row += self._get_user_actions_cells(user, actions)
      row += self._get_user_teams_cells(user, teams)

      data.append(row)

    data = sorted(data, key=lambda row : row[0]) # sort by community
    data.insert(0, columns) # insert the column names

    return data


  def _community_users_download(self, community_id):
    users = [cm.user for cm in CommunityMember.objects.filter(community__id=community_id, \
            is_deleted=False, user__is_deleted=False).select_related('user')]
    actions = Action.objects.filter(Q(community__id=community_id) | Q(is_global=True)) \
                                                      .filter(is_deleted=False)
    teams = Team.objects.filter(community__id=community_id, is_deleted=False)

    columns = ['full_name',
                'preferred_name',
                'email',
                'role'] \
                + [action.title for action in actions] \
                + [team.name for team in teams]

    data = [columns]

    for user in users:

      row = [user.full_name,
            user.preferred_name if user.preferred_name else '',
            user.email,
            'super admin' if user.is_super_admin else
                'community admin' if user.is_community_admin else
                'vendor' if user.is_vendor else
                'community member']

      row += self._get_user_actions_cells(user, actions)
      row += self._get_user_teams_cells(user, teams)

      data.append(row)

    return data


  def _all_actions_download(self):
    actions = Action.objects.select_related('calculator_action', 'community') \
            .prefetch_related('tags').filter(is_deleted=False)

    columns = ['community',
              'title',
              'average_carbon_points',
              'category',
              'cost',
              'impact']

    data = []

    for action in actions:

      if action.is_global:
        community = 'global'
      elif action.community:
        community = action.community.name
      average_carbon_points = action.calculator_action.average_points \
                          if action.calculator_action else action.average_carbon_score
      category = action.tags.filter(tag_collection__name='Category').first()
      cost = action.tags.filter(tag_collection__name='Cost').first()
      impact = action.tags.filter(tag_collection__name='Impact').first()

      data.append([community if community else '',
                  action.title,
                  average_carbon_points,
                  category.name if category else '',
                  cost.name if cost else '',
                  impact.name if impact else ''])

    data = sorted(data, key=lambda row : row[0]) # sort by community
    data.insert(0, columns) # insert the column names

    return data


  def _community_actions_download(self, community_id):
    actions = Action.objects.filter(Q(community__id=community_id) | Q(is_global=True)) \
      .select_related('calculator_action').prefetch_related('tags').filter(is_deleted=False)

    columns = ['title',
              'is_global',
              'average_carbon_points',
              'category',
              'cost',
              'impact']
    
    data = [columns]

    for action in actions:

      average_carbon_points = action.calculator_action.average_points \
                          if action.calculator_action else action.average_carbon_score
      category = action.tags.filter(tag_collection__name='Category').first()
      cost = action.tags.filter(tag_collection__name='Cost').first()
      impact = action.tags.filter(tag_collection__name='Impact').first()

      data.append([action.title,
                  str(action.is_global),
                  average_carbon_points,
                  category.name if category else '',
                  cost.name if cost else '',
                  impact.name if impact else ''])

    return data


  def users_download(self, context: Context, community_id) -> (list, MassEnergizeAPIError):
    try:
      if community_id:
        community_name = Community.objects.get(id=community_id).name
      if context.user_is_super_admin:
        if community_id:
          return (self._community_users_download(community_id), community_name), None
        else:
          return (self._all_users_download(), None), None
      elif context.user_is_community_admin and community_id:
        return (self._community_users_download(community_id), community_name), None
      else:
        return None, NotAuthorizedError()
    except Exception as e:
      capture_message(str(e), level="error")
      return None, CustomMassenergizeError(e)


  def actions_download(self, context: Context, community_id) -> (list, MassEnergizeAPIError):
    try:
      if community_id:
        community_name = Community.objects.get(id=community_id).name
      if context.user_is_super_admin:
          if community_id:
            return (self._community_actions_download(community_id), community_name), None
          else:
            return (self._all_actions_download(), None), None
      elif context.user_is_community_admin and community_id:
          return (self._community_actions_download(community_id), community_name), None
      else:
          return None, NotAuthorizedError()
    except Exception as e:
      capture_message(str(e), level="error")
      return None, CustomMassenergizeError(e)
