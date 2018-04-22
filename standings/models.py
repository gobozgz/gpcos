from django.db import models
from django.db.models import Count
from django_countries.fields import CountryField
from django.contrib import messages
from datetime import date
from lxml import etree
import os
import standings.utils


class PointSystem(models.Model):
    name = models.CharField(max_length=25)
    race_points = models.CharField(max_length=100)
    qualifying_points = models.CharField(max_length=100, blank=True)
    pole_position = models.FloatField(default=0)
    lead_lap = models.FloatField(default=0)
    fastest_lap = models.FloatField(default=0)
    most_laps_lead = models.FloatField(default=0)

    def __str__(self):
        return "{} ({})".format(self.name, self.race_points)

    def to_dict(self, race=True):
        try:
            if race:
                return {int(k) + 1: int(v) for k, v in enumerate(self.race_points.split(','))}
            else:
                return {int(k) + 1: int(v) for k, v in enumerate(self.qualifying_points.split(','))}
        except ValueError:
            return {0: 0}


class League(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def breadcrumbs(self):
        return [
            {"url": "league", "object": self},
        ]


class Division(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, blank=True)
    url = models.CharField(max_length=100, blank=True)
    order = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return "{} ({})".format(self.name, self.league.name)

    def breadcrumbs(self):
        return [
            {"url": "league", "object": self.league},
            {"url": "division", "object": self},
        ]


class Track(models.Model):
    name = models.CharField(max_length=100)
    length = models.FloatField(default=0)
    version = models.CharField(max_length=25)
    country = CountryField(blank=True)

    def __str__(self):
        return '{} ({}, {})'.format(self.name, self.country, self.version)


class Season(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, blank=True)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
    finalized = models.BooleanField(default=False)
    point_system = models.ForeignKey(PointSystem, on_delete=models.SET_NULL, null=True, blank=True)
    classification_type = models.CharField(max_length=10, blank=True)
    percent_classified = models.IntegerField(default=0)
    laps_classified = models.IntegerField(default=0)
    teams_disabled = models.BooleanField(default=False)

    def __str__(self):
        return "{} ({})".format(self.name, self.division.name)

    def breadcrumbs(self):
        return [
            {"url": "league", "object": self.division.league},
            {"url": "division", "object": self.division},
            {"url": "season", "object": self}
        ]

    def race_count(self):
        return {
            "incomplete": self.race_set.annotate(Count('result')).filter(result__isnull=True).count(),
            "total": self.race_set.annotate(Count('result')).count()
        }

    def allocate_points(self, total_lap_count, driver_lap_count):
        if self.classification_type.lower() == 'percent':
            if driver_lap_count < (total_lap_count * (self.percent_classified / 100)):
                return False
        elif self.classification_type.lower() == 'laps':
            if driver_lap_count < total_lap_count - self.laps_classified:
                return False

        return True

    def get_standings(self):
        season_penalty = self.seasonpenalty_set

        drivers = {}
        teams = {}

        results = Result.objects.filter(race__season=self).prefetch_related('race').prefetch_related(
            'driver').prefetch_related('team').prefetch_related('race__track')

        for result in results:
            if result.driver_id not in drivers:
                try:
                    best_finish = self.sortcriteria_set.get(driver=result.driver).best_finish
                except SortCriteria.DoesNotExist:
                    best_finish = 0

                try:
                    sp = season_penalty.get(driver=result.driver)
                    result.points -= sp.points
                except SeasonPenalty.DoesNotExist:
                    sp = None

                drivers[result.driver_id] = {
                    'driver': result.driver,
                    'points': result.points,
                    'results': [result],
                    'position': 0,
                    'best_finish': best_finish,
                    'season_penalty': sp
                }
            else:
                drivers[result.driver_id]['results'].append(result)
                drivers[result.driver_id]['points'] += result.points

            if not self.teams_disabled:
                if result.team.id not in teams:
                    try:
                        sp = season_penalty.get(team=result.team)
                        result.points -= sp.points
                    except SeasonPenalty.DoesNotExist:
                        sp = None

                    teams[result.team.id] = {
                        'team': result.team,
                        'points': result.points,
                        'results': [result],
                        'drivers': {result.driver},
                        'season_penalty': sp
                    }
                else:
                    teams[result.team_id]['results'].append(result)
                    teams[result.team_id]['points'] += result.points
                    teams[result.team_id]['drivers'].add(result.driver)

                teams[result.team.id]['driver_count'] = len(teams[result.team.id]['drivers'])

        sorted_drivers = []
        driver_sort = sorted(drivers, key=lambda item: drivers[item]['best_finish'])
        driver_sort = sorted(driver_sort, key=lambda item: drivers[item]['points'], reverse=True)
        for pos, driver in enumerate(driver_sort):
            drivers[driver]["position"] = pos + 1
            sorted_drivers.append(drivers[driver])

        sorted_teams = []
        team_sort = sorted(teams, key=lambda item: teams[item]['season_penalty'] is None, reverse=True)
        team_sort = sorted(team_sort, key=lambda item: teams[item]['points'], reverse=True)
        for pos, team in enumerate(team_sort):
            teams[team]["position"] = pos + 1
            sorted_teams.append(teams[team])

        return sorted_drivers, sorted_teams



class Race(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    point_system = models.ForeignKey(PointSystem, on_delete=models.SET_NULL, null=True, blank=True)
    round_number = models.IntegerField(default=1)
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=3, null=True)
    start_time = models.DateTimeField()
    track = models.ForeignKey(Track, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['round_number']

    def __str__(self):
        return "{} ({}, {})".format(self.name, self.season.name, self.season.division.name)

    @property
    def qualifying_order(self):
        return self.result_set.order_by('qualifying')

    @property
    def race_order(self):
        return self.result_set.order_by('position')

    def breadcrumbs(self):
        return [
            {"url": "league", "object": self.season.division.league},
            {"url": "division", "object": self.season.division},
            {"url": "season", "object": self.season},
            {"url": "race", "object": self}
        ]

    def fill_attributes(self):
        total_race_time = 0
        total_lap_count = 0

        ps = self.point_system if self.point_system else self.season.point_system
        ll = self.laps_lead()
        ml = ll.first()
        season_penalty = SeasonPenalty.objects.filter(season=self.season)

        for result in self.result_set.all():
            if result.position == 1:
                result.gap = '-'
                total_lap_count = result.race_laps
                total_race_time = result.race_time

            if result.race_laps < total_lap_count:
                result.gap = '{} laps down'.format(total_lap_count - result.race_laps)
            else:
                result.gap = standings.utils.format_time(result.race_time - total_race_time)

            # check classification rules
            if self.season.allocate_points(total_lap_count, result.race_laps):
                result.points = ps.to_dict().get(result.position, 0)
                if result.fastest_lap:
                    result.points += ps.fastest_lap
            else:
                result.points = 0

            # pole position
            if result.qualifying == 1:
                result.points += ps.pole_position

            # most laps lead
            if ml['driver_id'] == result.driver_id:
                result.points += ps.most_laps_lead

            # points per lap lead
            for driver in ll:
                if driver['driver_id'] == result.driver_id:
                    result.points += (ps.lead_lap * driver['first_place'])

            # multiplier
            result.points *= result.points_multiplier

            try:
                sp = season_penalty.get(driver=result.driver)
            except SeasonPenalty.DoesNotExist:
                sp = None

            if sp and sp.disqualified:
                result.points = 0

            result.save()

            (sort_criteria, _) = SortCriteria.objects.get_or_create(season=self.season, driver=result.driver)
            if result.position < sort_criteria.best_finish or sort_criteria.best_finish == 0:
                sort_criteria.best_finish = result.position
            if sp and sp.disqualified:
                sort_criteria.best_finish = 99

            sort_criteria.save()

    def tooltip(self):
        tooltip = "{name}<br/>{time}".format(
            time=self.start_time.strftime('%B %d %Y @ %H:%M'),
            name=self.name,
        )
        return tooltip

    def laps_lead(self):
        return Result.objects.values('driver_id').filter(race=self, lap__position=1).annotate(
            first_place=Count('lap__position')).order_by('-first_place')


class Driver(models.Model):
    name = models.CharField(max_length=50)
    country = CountryField(blank=True)
    shortname = models.CharField(max_length=25, blank=True)
    birthday = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=50, blank=True)
    helmet = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.country)

    def collect_results(self):
        for driver in Driver.objects.filter(name=self.name):
            if driver is not self:
                driver.result_set.update(driver=self)


class Team(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=100, blank=True)
    country = CountryField(blank=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.id)


class SortCriteria(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    best_finish = models.IntegerField(default=0)


class Result(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, null=True, on_delete=models.SET_NULL)
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)
    qualifying = models.IntegerField('Position', default=0)
    position = models.IntegerField(default=0)
    fastest_lap = models.BooleanField('Fastest lap in race', default=False)
    note = models.CharField(max_length=100, blank=True)
    subbed_by = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.SET_NULL, related_name='substitute')
    allocate_points = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL,
                                        related_name='points_allocation')
    race_laps = models.IntegerField('Lap count', default=0)
    race_time = models.FloatField('Total time', default=0)
    qualifying_laps = models.IntegerField('Lap count', default=0)
    qualifying_time = models.FloatField('Total time', default=0)
    finalized = models.BooleanField(default=False)
    car = models.CharField(max_length=25, blank=True)
    car_class = models.CharField(max_length=25, blank=True)
    points_multiplier = models.FloatField('Points Multiplier', default=1)
    points_multiplier_description = models.CharField('Multiplier Description', max_length=250, blank=True)
    race_penalty_time = models.IntegerField('Time', default=0)
    race_penalty_positions = models.IntegerField('Positions', default=0)
    race_penalty_description = models.CharField('Description', max_length=100, blank=True)
    qualifying_penalty_grid = models.IntegerField('Grid Positions', default=0)
    qualifying_penalty_bog = models.BooleanField('Back of grid', default=False)
    qualifying_penalty_sfp = models.BooleanField('Start from pits', default=False)
    qualifying_penalty_description = models.CharField('Description', max_length=100, blank=True)
    dnf_reason = models.CharField('DNF Reason', max_length=50, blank=True, default='')
    points = models.FloatField(default=0)
    gap = models.CharField(default='-', max_length=25)
    race_fastest_lap = models.FloatField('Fastest lap (R)', default=0)
    qualifying_fastest_lap = models.FloatField('Fastest lap (Q)', default=0)
    penalty_points = models.IntegerField(default=0)
    race_penalty_dsq = models.BooleanField(default=False)
    qualifying_penalty_dsq = models.BooleanField(default=False)

    class Meta:
        ordering = ['position']

    def has_notes(self):
        return (self.note != '' and self.note is not None) \
               or self.subbed_by is not None \
               or self.allocate_points is not None \
               or (self.race_penalty_description != '' and self.race_penalty_description is not None) \
               or (self.qualifying_penalty_description != '' and self.qualifying_penalty_description is not None)

    def __str__(self):
        return "{race} ({driver}, {position})".format(
            race=self.race.name,
            driver=self.driver.name,
            position=self.position
        )


class Lap(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    session = models.CharField(max_length=10)
    lap_number = models.IntegerField(default=1)
    position = models.IntegerField(default=1)
    pitstop = models.BooleanField(default=False)
    sector_1 = models.FloatField(default=0)
    sector_2 = models.FloatField(default=0)
    sector_3 = models.FloatField(default=0)
    lap_time = models.FloatField(default=0)
    race_time = models.FloatField(default=0)


class LogFile(models.Model):
    file = models.FileField(upload_to='log_files/%Y/%m/%d')
    race = models.ForeignKey(Race, on_delete=models.CASCADE)

    @staticmethod
    def get_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def __str__(self):
        return '{} ({})'.format(os.path.basename(self.file.path), self.race)

    def process(self, request):
        with open(self.file.name) as infile:
            tree = etree.XML(infile.read().encode('utf-8'))

        qualify = len(tree.xpath('//Qualify'))
        if qualify > 0:
            session = 'qualify'
        else:
            session = 'race'

        duplicates = []
        drivers = tree.xpath('//Driver')
        for driver in drivers:
            driver_name = driver.xpath('./Name')[0].text.strip()
            try:
                driver_obj = Driver.objects.get(name__unaccent=driver_name)
            except Driver.DoesNotExist:
                driver_obj = Driver.objects.create(name=driver_name)
            except Driver.MultipleObjectsReturned:
                driver_obj = Driver.objects.filter(name__unaccent=driver_name).annotate(
                    result_count=Count('result')).order_by('-result_count').first()
                if driver_name not in duplicates:
                    duplicates.append(driver_name)

            team_name = driver.xpath('./CarType')[0].text
            (team_obj, created) = Team.objects.get_or_create(name=team_name)

            (result, created) = Result.objects.get_or_create(
                race=self.race, driver=driver_obj, team=team_obj
            )

            result.fastest_lap = driver.xpath('./LapRankIncludingDiscos')[0].text == '1'
            result.car_class = driver.xpath('./CarClass')[0].text
            result.car = driver.xpath('./VehFile')[0].text
            if session == 'race':
                result.qualifying = driver.xpath('./GridPos')[0].text
                result.position = driver.xpath('./Position')[0].text
                result.race_laps = driver.xpath('./Laps')[0].text
            else:
                result.qualifying_laps = driver.xpath('./Laps')[0].text
                result.qualifying = driver.xpath('./Position')[0].text

            if driver.xpath('./FinishStatus')[0].text == 'Finished Normally':
                try:
                    result.race_time = driver.xpath('./FinishTime')[0].text
                except IndexError:
                    result.race_time = 0
            else:
                result.race_time = 0
                try:
                    result.dnf_reason = driver.xpath('./DNFReason')[0].text
                except IndexError:
                    result.dnf_reason = ''

            result.save()

            race_time = 0
            fastest_lap = 0

            laps = driver.xpath('.//Lap')
            for lap in laps:
                lap_number = int(lap.get('num'))
                (lap_obj, created) = Lap.objects.get_or_create(result=result, lap_number=lap_number, session=session)

                lap_obj.position = int(lap.get('p'))
                lap_obj.sector_1 = self.get_float(lap.get('s1'))
                lap_obj.sector_2 = self.get_float(lap.get('s2'))
                lap_obj.sector_3 = self.get_float(lap.get('s3'))
                lap_obj.pitstop = lap.get('pit') == '1'
                lap_obj.lap_time = self.get_float(lap.text)

                lap_obj.save()

                race_time += lap_obj.lap_time
                if lap_obj.lap_time > 0 and (lap_obj.lap_time < fastest_lap or fastest_lap == 0):
                    fastest_lap = lap_obj.lap_time

            if session == 'race':
                result.race_fastest_lap = fastest_lap
                if result.race_time == 0:
                    result.race_time = race_time
            else:
                result.qualifying_fastest_lap = fastest_lap
                if result.qualifying_time == 0:
                    result.qualifying_time = race_time

            result.save()

        if duplicates:
            msg = 'The following drivers have duplicate records, results ' \
                  'have been applied to the one with the most results - {}'.format(', '.join(duplicates))

            messages.add_message(request, messages.WARNING, msg)

        self.race.fill_attributes()


class SeasonPenalty(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.SET_NULL)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL)
    points = models.IntegerField(default=0)
    disqualified = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Season Penalties'

    def process(self):
        qs = None
        if self.disqualified:
            if self.driver:
                qs = Result.objects.filter(driver=self.driver)
            elif self.team:
                qs = Result.objects.filter(team=self.team)

            if qs:
                qs.update(points=0)


    def __str__(self):
        string = '{}'.format(self.season)
        if self.driver:
            string = '{}, {}'.format(string, self.driver)
        if self.team:
            string = '{}, {}'.format(string, self.team)
        if self.points > 0:
            string = '{}, docked {} points'.format(string, self.points)
        if self.disqualified:
            string = '{}, disqualified'.format(string)

        return string
