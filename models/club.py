from copy import deepcopy

from sqlalchemy import Column, Integer, Sequence, ForeignKey, Unicode
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr, declarative_base

from models.common import BaseSchema
import models.common.overview as mco
import models.common.personnel as mcp
import models.common.match as mcm
import models.common.events as mce


ClubSchema = declarative_base(name="Clubs", metadata=BaseSchema.metadata,
                              class_registry=deepcopy(BaseSchema._decl_class_registry))


class Clubs(ClubSchema):
    __tablename__ = 'clubs'

    id = Column(Integer, Sequence('club_id_seq', start=10000), primary_key=True)

    name = Column(Unicode(60))

    country_id = Column(Integer, ForeignKey('countries.id'))
    country = relationship('Countries', backref=backref('clubs'))

    def __repr__(self):
        return "<Club(name={0}, country={1})>".format(self.name, self.country.name)

    def __unicode__(self):
        return u"<Club(name={0}, country={1})>".format(self.name, self.country.name)


class ClubMixin(object):

    @declared_attr
    def team_id(cls):
        return Column(Integer, ForeignKey('clubs.id'))


class ClubMatchMixin(object):

    @declared_attr
    def home_team_id(cls):
        return Column(Integer, ForeignKey('clubs.id'))

    @declared_attr
    def away_team_id(cls):
        return Column(Integer, ForeignKey('clubs.id'))


class FriendlyMixin(object):

    @declared_attr
    def home_team(cls):
        return relationship('Clubs', foreign_keys="{}.home_team_id".format(cls.__name__),
                            backref=backref('home_friendly_matches'))

    @declared_attr
    def away_team(cls):
        return relationship('Clubs', foreign_keys="{}.away_team_id".format(cls.__name__),
                            backref=backref('away_friendly_matches'))


class LeagueMixin(object):

    @declared_attr
    def home_team(cls):
        return relationship('Clubs', foreign_keys="{}.home_team_id".format(cls.__name__),
                            backref=backref('home_league_matches'))

    @declared_attr
    def away_team(cls):
        return relationship('Clubs', foreign_keys="{}.away_team_id".format(cls.__name__),
                            backref=backref('away_league_matches'))


class GroupMixin(object):

    @declared_attr
    def home_team(cls):
        return relationship('Clubs', foreign_keys="{}.home_team_id".format(cls.__name__),
                            backref=backref('home_group_matches'))

    @declared_attr
    def away_team(cls):
        return relationship('Clubs', foreign_keys="{}.away_team_id".format(cls.__name__),
                            backref=backref('away_group_matches'))


class KnockoutMixin(object):

    @declared_attr
    def home_team(cls):
        return relationship('Clubs', foreign_keys="{}.home_team_id".format(cls.__name__),
                            backref=backref('home_knockout_matches'))

    @declared_attr
    def away_team(cls):
        return relationship('Clubs', foreign_keys="{}.away_team_id".format(cls.__name__),
                            backref=backref('away_knockout_matches'))


class ClubFriendlyMatches(FriendlyMixin, ClubMatchMixin, ClubSchema, mcm.Matches):
    __tablename__ = "club_friendly_matches"
    __mapper_args__ = {'polymorphic_identity': 'friendly'}

    id = Column(Integer, ForeignKey('matches.id'), primary_key=True)


class ClubLeagueMatches(LeagueMixin, ClubMatchMixin, ClubSchema, mcm.LeagueMatches, mcm.Matches):
    __tablename__ = "club_league_matches"
    __mapper_args__ = {'polymorphic_identity': 'league'}

    id = Column(Integer, ForeignKey('matches.id'), primary_key=True)


class ClubGroupMatches(GroupMixin, ClubMatchMixin, ClubSchema, mcm.GroupMatches):
    __tablename__ = "club_group_matches"
    __mapper_args__ = {'polymorphic_identity': 'group'}

    id = Column(Integer, ForeignKey('matches.id'), primary_key=True)


class ClubKnockoutMatches(KnockoutMixin, ClubMatchMixin, ClubSchema, mcm.KnockoutMatches):
    __tablename__ = "club_knockout_matches"
    __mapper_args__ = {'polymorphic_identity': 'knockout'}

    id = Column(Integer, ForeignKey('matches.id'), primary_key=True)


class ClubMatchLineups(ClubMixin, ClubSchema, mcm.MatchLineups):
    __tablename__ = "club_match_lineups"
    __mapper_args__ = {'polymorphic_identity': 'club'}

    id = Column(Integer, ForeignKey('lineups.id'), primary_key=True)

    team = relationship('Clubs', foreign_keys="ClubMatchLineups.team_id", backref=backref("lineups"))


class ClubGoals(ClubMixin, ClubSchema, mce.Goals):
    __mapper_args__ = {'polymorphic_identity': 'club'}

    team = relationship('Clubs', foreign_keys="ClubGoals.team_id", backref=backref("goals"))


class ClubPenaltyShootoutOpeners(ClubMixin, ClubSchema, mce.PenaltyShootoutOpeners):
    __mapper_args__ = {'polymorphic_identity': 'club'}

    team = relationship('Clubs', foreign_keys="ClubPenaltyShootoutOpeners.team_id",
                        backref=backref("shootout_openers"))
