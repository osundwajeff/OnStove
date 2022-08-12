"""This module contains the technology classes used in OnStove."""

import os
import numpy as np
import pandas as pd
from typing import Optional, Callable
from math import exp

from onstove.layer import VectorLayer, RasterLayer
import onstove.onstove


class Technology:
    """
    Standard technology class.
    """

    def __init__(self,
                 name=None,
                 carbon_intensity=None,
                 co2_intensity=0,
                 ch4_intensity=0,
                 n2o_intensity=0,
                 co_intensity=0,
                 bc_intensity=0,
                 oc_intensity=0,
                 energy_content=0,
                 tech_life=0,  # in years
                 inv_cost=0,  # in USD
                 fuel_cost=0,
                 time_of_cooking=0,
                 om_cost=0,  # percentage of investement cost
                 efficiency=0,  # ratio
                 pm25=0,
                 is_base=False,
                 transport_cost=0,
                 is_clean=False,
                 current_share_urban=0,
                 current_share_rural=0,
                 epsilon=0.71):  # 24-h PM2.5 concentration

        self.name = name
        self.carbon_intensity = carbon_intensity
        self.co2_intensity = co2_intensity
        self.ch4_intensity = ch4_intensity
        self.n2o_intensity = n2o_intensity
        self.co_intensity = co_intensity
        self.bc_intensity = bc_intensity
        self.oc_intensity = oc_intensity
        self.energy_content = energy_content
        self.tech_life = tech_life
        self.fuel_cost = fuel_cost
        self.inv_cost = inv_cost
        self.om_cost = om_cost
        self.time_of_cooking = time_of_cooking
        self.efficiency = efficiency
        self.pm25 = pm25
        self.time_of_collection = 0
        self.fuel_use = None
        self.is_base = is_base
        self.transport_cost = transport_cost
        self.carbon = None
        self.total_time_yr = None
        self.is_clean = is_clean
        self.current_share_urban = current_share_urban
        self.current_share_rural = current_share_rural
        self.energy = 0
        self.epsilon = epsilon
        for paf in ['paf_alri_', 'paf_copd_', 'paf_ihd_', 'paf_lc_', 'paf_stroke_']:
            for s in ['u', 'r']:
                self[paf + s] = 0
        self.discounted_fuel_cost = 0
        self.discounted_investments = 0

    def __setitem__(self, idx, value):
        if idx == 'name':
            self.name = value
        elif idx == 'energy_content':
            self.energy_content = value
        elif idx == 'carbon_intensity':
            self.carbon_intensity = value
        elif idx.lower() == 'co2_intensity':
            self.co2_intensity = value
        elif idx.lower() == 'ch4_intensity':
            self.ch4_intensity = value
        elif idx.lower() == 'n2o_intensity':
            self.n2o_intensity = value
        elif idx.lower() == 'co_intensity':
            self.co_intensity = value
        elif idx.lower() == 'bc_intensity':
            self.bc_intensity = value
        elif idx.lower() == 'oc_intensity':
            self.oc_intensity = value
        elif idx == 'fuel_cost':
            self.fuel_cost = value
        elif idx == 'tech_life':
            self.tech_life = value
        elif idx == 'inv_cost':
            self.inv_cost = value
        elif idx == 'om_cost':
            self.om_cost = value
        elif idx == 'time_of_cooking':
            self.time_of_cooking = value
        elif idx == 'efficiency':
            self.efficiency = value
        elif idx == 'pm25':
            self.pm25 = value
        elif idx == 'time_of_collection':
            self.time_of_collection = value
        elif idx == 'fuel_use':
            self.fuel_use = value
        elif idx == 'is_base':
            self.is_base = value
        elif idx == 'diesel_cost':
            self.diesel_cost = value
        elif idx == 'carbon':
            self.carbon = value
        elif idx == 'current_share_urban':
            self.current_share_urban = value
        elif idx == 'current_share_rural':
            self.current_share_rural = value
        elif idx == 'paf_alri_r':
            self.paf_alri_r = value
        elif idx == 'paf_copd_r':
            self.paf_copd_r = value
        elif idx == 'paf_ihd_r':
            self.paf_ihd_r = value
        elif idx == 'paf_lc_r':
            self.paf_lc_r = value
        elif idx == 'paf_stroke_r':
            self.paf_stroke_r = value
        elif idx == 'paf_alri_u':
            self.paf_alri_u = value
        elif idx == 'paf_copd_u':
            self.paf_copd_u = value
        elif idx == 'paf_ihd_u':
            self.paf_ihd_u = value
        elif idx == 'paf_lc_u':
            self.paf_lc_u = value
        elif idx == 'paf_stroke_u':
            self.paf_stroke_u = value
        elif idx == 'epsilon':
            self.epsilon = value
        else:
            raise KeyError(idx)

    def __getitem__(self, idx):
        if idx == 'name':
            return self.name
        elif idx == 'energy_content':
            return self.energy_content
        elif idx == 'carbon_intensity':
            return self.carbon_intensity
        elif idx.lower() == 'co2_intensity':
            return self.co2_intensity
        elif idx.lower() == 'ch4_intensity':
            return self.ch4_intensity
        elif idx.lower() == 'n2o_intensity':
            return self.n2o_intensity
        elif idx.lower() == 'co_intensity':
            return self.co_intensity
        elif idx.lower() == 'bc_intensity':
            return self.bc_intensity
        elif idx.lower() == 'oc_intensity':
            return self.oc_intensity
        elif idx == 'fuel_cost':
            return self.fuel_cost
        elif idx == 'tech_life':
            return self.tech_life
        elif idx == 'inv_cost':
            return self.inv_cost
        elif idx == 'om_cost':
            return self.om_cost
        elif idx == 'time_of_cooking':
            return self.time_of_cooking
        elif idx == 'efficiency':
            return self.efficiency
        elif idx == 'pm25':
            return self.pm25
        elif idx == 'time_of_collection':
            return self.time_of_collection
        elif idx == 'fuel_use':
            return self.fuel_use
        elif idx == 'is_base':
            return self.is_base
        elif idx == 'diesel_cost':
            return self.diesel_cost
        elif idx == 'carbon':
            return self.carbon
        elif idx == 'current_share_urban':
            return self.current_share_urban
        elif idx == 'current_share_rural':
            return self.current_share_rural
        elif idx == 'paf_alri_r':
            return self.paf_alri_r
        elif idx == 'paf_copd_r':
            return self.paf_copd_r
        elif idx == 'paf_ihd_r':
            return self.paf_ihd_r
        elif idx == 'paf_lc_r':
            return self.paf_lc_r
        elif idx == 'paf_stroke_r':
            return self.paf_stroke_r
        elif idx == 'paf_alri_u':
            return self.paf_alri_u
        elif idx == 'paf_copd_u':
            return self.paf_copd_u
        elif idx == 'paf_ihd_u':
            return self.paf_ihd_u
        elif idx == 'paf_lc_u':
            return self.paf_lc_u
        elif idx == 'paf_stroke_u':
            return self.paf_stroke_u
        elif idx == 'epsilon':
            return self.epsilon
        else:
            raise KeyError(idx)

    def adjusted_pm25(self):
        self.pm25 *= self.epsilon

    def relative_risk(self):
        if self.pm25 < 7.298:
            rr_alri = 1
        else:
            rr_alri = 1 + 2.383 * (1 - exp(-0.004 * (self.pm25 - 7.298) ** 1.193))

        if self.pm25 < 7.337:
            rr_copd = 1
        else:
            rr_copd = 1 + 22.485 * (1 - exp(-0.001 * (self.pm25 - 7.337) ** 0.694))

        if self.pm25 < 7.449:
            rr_ihd = 1
        else:
            rr_ihd = 1 + 1.647 * (1 - exp(-0.048 * (self.pm25 - 7.449) ** 0.467))

        if self.pm25 < 7.345:
            rr_lc = 1
        else:
            rr_lc = 1 + 152.496 * (1 - exp(-0.000167 * (self.pm25 - 7.345) ** 0.76))

        if self.pm25 < 7.358:
            rr_stroke = 1
        else:
            rr_stroke = 1 + 1.314 * (1 - exp(-0.012 * (self.pm25 - 7.358) ** 1.275))

        return rr_alri, rr_copd, rr_ihd, rr_lc, rr_stroke

    def paf(self, rr, sfu):
        paf = (sfu * (rr - 1)) / (sfu * (rr - 1) + 1)
        return paf

    @staticmethod
    def discount_factor(specs):
        """
        :param model: onstove instance containing the informtion of the model
        :return: discount factor to be used for all costs in the net benefit fucntion and the years of analysis
        """
        if specs["Start_year"] == specs["End_year"]:
            proj_life = 1
        else:
            proj_life = specs["End_year"] - specs["Start_year"]

        year = np.arange(proj_life) + 1

        discount_factor = (1 + specs["Discount_rate"]) ** year

        return discount_factor, proj_life

    def required_energy(self, model):
        # Annual energy needed for cooking, affected by stove efficiency (MJ/yr)
        self.energy = model.specs["Meals_per_day"] * 365 * model.energy_per_meal / self.efficiency

    def get_carbon_intensity(self, model):
        pollutants = ['co2', 'ch4', 'n2o', 'co', 'bc', 'oc']
        self.carbon_intensity = sum([self[f'{pollutant}_intensity'] * model.gwp[pollutant] for pollutant in pollutants])

    def carb(self, model):
        self.required_energy(model)
        if self.carbon_intensity is None:
            self.get_carbon_intensity(model)
        self.carbon = pd.Series([(self.energy * self.carbon_intensity) / 1000] * model.gdf.shape[0],
                                index=model.gdf.index)

    def carbon_emissions(self, model):
        self.carb(model)
        proj_life = model.specs['End_year'] - model.specs['Start_year']
        carbon = model.specs["Cost of carbon emissions"] * (model.base_fuel.carbon - self.carbon) / 1000 / (
                1 + model.specs["Discount_rate"]) ** (proj_life)

        self.decreased_carbon_emissions = model.base_fuel.carbon - self.carbon
        self.decreased_carbon_costs = carbon

    def health_parameters(self, model):
        rr_alri, rr_copd, rr_ihd, rr_lc, rr_stroke = self.relative_risk()
        self.paf_alri_r = self.paf(rr_alri, 1 - model.clean_cooking_access_r)
        self.paf_copd_r = self.paf(rr_copd, 1 - model.clean_cooking_access_r)
        self.paf_ihd_r = self.paf(rr_ihd, 1 - model.clean_cooking_access_r)
        self.paf_lc_r = self.paf(rr_lc, 1 - model.clean_cooking_access_r)
        self.paf_stroke_r = self.paf(rr_stroke, 1 - model.clean_cooking_access_r)

        self.paf_alri_u = self.paf(rr_alri, 1 - model.clean_cooking_access_u)
        self.paf_copd_u = self.paf(rr_copd, 1 - model.clean_cooking_access_u)
        self.paf_ihd_u = self.paf(rr_ihd, 1 - model.clean_cooking_access_u)
        self.paf_lc_u = self.paf(rr_lc, 1 - model.clean_cooking_access_u)
        self.paf_stroke_u = self.paf(rr_stroke, 1 - model.clean_cooking_access_u)

    def mort_morb(self, model, parameter='Mort', dr='Discount_rate'):
        """
        Calculates mortality or morbidity rate per fuel

        Returns
        ----------
        Monetary mortality for each stove in urban and rural settings
        """
        self.health_parameters(model)

        mor_u = {}
        mor_r = {}
        diseases = ['ALRI', 'COPD', 'IHD', 'LC', 'STROKE']
        is_urban = model.gdf["IsUrban"] > 20
        is_rural = model.gdf["IsUrban"] < 20
        for disease in diseases:
            rate = model.specs[f'{parameter}_{disease}']

            paf = f'paf_{disease.lower()}_u'
            mor_u[disease] = model.gdf.loc[is_urban, "Calibrated_pop"].sum() * (model.base_fuel[paf] - self[paf]) * (
                    rate / 100000)

            paf = f'paf_{disease.lower()}_r'
            mor_r[disease] = model.gdf.loc[is_rural, "Calibrated_pop"].sum() * (model.base_fuel[paf] - self[paf]) * (
                    rate / 100000)

        cl_diseases = {'ALRI': {1: 0.7, 2: 0.1, 3: 0.07, 4: 0.07, 5: 0.06},
                       'COPD': {1: 0.3, 2: 0.2, 3: 0.17, 4: 0.17, 5: 0.16},
                       'LC': {1: 0.2, 2: 0.1, 3: 0.24, 4: 0.23, 5: 0.23},
                       'IHD': {1: 0.2, 2: 0.1, 3: 0.24, 4: 0.23, 5: 0.23},
                       'STROKE': {1: 0.2, 2: 0.1, 3: 0.24, 4: 0.23, 5: 0.23}}

        i = 1
        total_mor_u = 0
        total_mor_r = 0
        while i < 6:
            for disease in diseases:
                if parameter == 'Morb':
                    cost = model.specs[f'COI_{disease}']
                elif parameter == 'Mort':
                    cost = model.specs['VSL']
                total_mor_u += cl_diseases[disease][i] * cost * mor_u[disease] / (1 + model.specs[dr]) ** (i - 1)
                total_mor_r += cl_diseases[disease][i] * cost * mor_r[disease] / (1 + model.specs[dr]) ** (i - 1)
            i += 1

        is_urban = model.gdf["IsUrban"] > 20
        is_rural = model.gdf["IsUrban"] < 20

        urban_denominator = model.gdf.loc[is_urban, "Calibrated_pop"].sum() * model.gdf.loc[is_urban, 'Households']
        rural_denominator = model.gdf.loc[is_rural, "Calibrated_pop"].sum() * model.gdf.loc[is_rural, 'Households']

        distributed_cost = pd.Series(index=model.gdf.index, dtype='float64')

        distributed_cost[is_urban] = model.gdf.loc[is_urban, "Calibrated_pop"] * total_mor_u / urban_denominator
        distributed_cost[is_rural] = model.gdf.loc[is_rural, "Calibrated_pop"] * total_mor_r / rural_denominator

        cases_avoided = pd.Series(index=model.gdf.index, dtype='float64')

        cases_avoided[is_urban] = sum(mor_u.values()) * model.gdf.loc[is_urban, "Calibrated_pop"] / urban_denominator
        cases_avoided[is_rural] = sum(mor_r.values()) * model.gdf.loc[is_rural, "Calibrated_pop"] / rural_denominator

        return distributed_cost, cases_avoided

    def mortality(self, model):
        """
        Calculates mortality rate per fuel

        Returns
        ----------
        Monetary mortality for each stove in urban and rural settings
        """
        distributed_mortality, deaths_avoided = self.mort_morb(model, parameter='Mort', dr='Discount_rate')
        self.distributed_mortality = distributed_mortality
        self.deaths_avoided = deaths_avoided

        if model.specs['Health_spillovers_parameter'] > 0:
            self.distributed_spillovers_mort = distributed_mortality * model.specs['Health_spillovers_parameter']
            self.deaths_avoided += deaths_avoided * model.specs['Health_spillovers_parameter']
        else:
            self.distributed_spillovers_mort = pd.Series(0, index=model.gdf.index, dtype='float64')

    def morbidity(self, model):
        """
        Calculates morbidity rate per fuel

        Returns
        ----------
        Monetary morbidity for each stove in urban and rural settings
        """
        distributed_morbidity, cases_avoided = self.mort_morb(model, parameter='Morb', dr='Discount_rate')
        self.distributed_morbidity = distributed_morbidity
        self.cases_avoided = cases_avoided

        if model.specs['Health_spillovers_parameter'] > 0:
            self.distributed_spillovers_morb = distributed_morbidity * model.specs['Health_spillovers_parameter']
            self.cases_avoided += cases_avoided * model.specs['Health_spillovers_parameter']
        else:
            self.distributed_spillovers_morb = pd.Series(0, index=model.gdf.index, dtype='float64')

    def salvage(self, model):
        """
        Calculates discounted salvage cost assuming straight-line depreciation
        Returns
        ----------
        discounted salvage cost
        """
        discount_rate, proj_life = self.discount_factor(model.specs)
        used_life = proj_life % self.tech_life
        used_life_base = proj_life % model.base_fuel.tech_life

        base_salvage = model.base_fuel.inv_cost * (1 - used_life_base / model.base_fuel.tech_life)
        salvage = self.inv_cost * (1 - used_life / self.tech_life)

        salvage = salvage - base_salvage
        # TODO: this needs to be changed to use a series for each salvage value
        discounted_salvage = salvage / discount_rate

        self.discounted_salvage_cost = discounted_salvage

    def discounted_om(self, model):
        """
        Calls discount_factor function and creates discounted OM costs.
        Returns
        ----------
        discountedOM costs for each stove during the project lifetime
        """
        discount_rate, proj_life = self.discount_factor(model.specs)
        operation_and_maintenance = self.om_cost * np.ones(proj_life)

        discounted_om = np.array([sum((operation_and_maintenance - x) / discount_rate) for
                                  x in model.base_fuel.om_cost])
        self.discounted_om_costs = pd.Series(discounted_om, index=model.gdf.index)

    def discounted_inv(self, model, relative=True):
        """
        Calls discount_factor function and creates discounted investment cost. Uses proj_life and tech_life to determine
        number of necessary re-investments

        Returns
        ----------
        discounted investment cost for each stove during the project lifetime
        """
        discount_rate, proj_life = self.discount_factor(model.specs)

        inv = self.inv_cost * np.ones(model.gdf.shape[0])
        tech_life = self.tech_life * np.ones(model.gdf.shape[0])

        proj_years = np.matmul(np.expand_dims(np.ones(model.gdf.shape[0]), axis=1),
                               np.expand_dims(np.zeros(proj_life), axis=0))

        for i in np.unique(tech_life):
            where = np.where(tech_life == i)
            for j in range(int(i) - 1, proj_life, int(i)):
                proj_years[where, j] = 1

        investments = proj_years * inv[:, None]

        if relative:
            discounted_base_investments = model.base_fuel.discounted_investments
        else:
            discounted_base_investments = 0

        investments_discounted = np.array([sum(x / discount_rate) for x in investments])
        self.discounted_investments = pd.Series(investments_discounted, index=model.gdf.index) + self.inv_cost - \
                                      discounted_base_investments

    def discount_fuel_cost(self, model, relative=True):
        self.required_energy(model)
        discount_rate, proj_life = self.discount_factor(model.specs)

        cost = (self.energy * self.fuel_cost / self.energy_content + self.transport_cost) * np.ones(model.gdf.shape[0])

        fuel_cost = [np.ones(proj_life) * x for x in cost]

        fuel_cost_discounted = np.array([sum(x / discount_rate) for x in fuel_cost])

        if relative:
            discounted_base_fuel_cost = model.base_fuel.discounted_fuel_cost
        else:
            discounted_base_fuel_cost = 0

        self.discounted_fuel_cost = pd.Series(fuel_cost_discounted, index=model.gdf.index) - discounted_base_fuel_cost

    def total_time(self, model):
        self.total_time_yr = (self.time_of_cooking + self.time_of_collection) * 365

    def time_saved(self, model):
        proj_life = model.specs['End_year'] - model.specs['Start_year']
        self.total_time(model)
        self.total_time_saved = model.base_fuel.total_time_yr - self.total_time_yr
        # time value of time saved per sq km
        self.time_value = self.total_time_saved * model.gdf["value_of_time"] / (
                1 + model.specs["Discount_rate"]) ** (proj_life)

    def total_costs(self):
        self.costs = (self.discounted_fuel_cost + self.discounted_investments +  # - self.time_value +
                      self.discounted_om_costs - self.discounted_salvage_cost)

    def net_benefit(self, model, w_health=1, w_spillovers=1, w_environment=1, w_time=1, w_costs=1):
        self.total_costs()
        self.benefits = w_health * (self.distributed_morbidity + self.distributed_mortality) + \
                        w_spillovers * (self.distributed_spillovers_morb + self.distributed_spillovers_mort) + \
                        w_environment * self.decreased_carbon_costs + w_time * self.time_value
        model.gdf["costs_{}".format(self.name)] = self.costs
        model.gdf["benefits_{}".format(self.name)] = self.benefits
        model.gdf["net_benefit_{}".format(self.name)] = self.benefits - w_costs * self.costs
        self.factor = pd.Series(np.ones(model.gdf.shape[0]), index=model.gdf.index)
        self.households = model.gdf['Households']


class LPG(Technology):
    """LPG technology class used to model LPG stoves.

    This class inherits the standard :class:`Technology` class and is used to model stoves using LPG as fuel.
    The LPG is assumed to be bought either by the closest vendor or in the closest urban settlement depedning on
    data availability. In the first case a point layer indicating vendors is assumed to be passed to the OnStove after
    which a least-cost path is determined using a friction map. In the other case it is assumed that the traveltime map
    is passed to OnStove directly.

    Parameters
    ----------
    name: str, optional.
       Name of the technology to model.
    carbon_intensity: float, optional
       The CO2 equivalent emissions in kg/GJ of burned fuel. If this attribute is used, then none of the
       gas-specific intensities will be used (e.g. ch4_intensity).
    co2_intensity: float, default 63
       The CO2 emissions in kg/GJ of burned fuel.
    ch4_intensity: float, default 0.003
       The CH4 emissions in kg/GJ of burned fuel.
    n2o_intensity: float, default 0.0001
       The N2O emissions in kg/GJ of burned fuel.
    co_intensity: float, default 0
       The CO emissions in kg/GJ of burned fuel.
    bc_intensity: float, default 0.0044
       The black carbon emissions in kg/GJ of burned fuel.
    oc_intensity: float, default 0.0091
       The organic carbon emissions in kg/GJ of burned fuel.
    energy_content: float, default 45.5
       Energy content of the fuel in MJ/kg.
    tech_life: int, default 7
       Stove life in year.
    inv_cost: float, default 44
       Investment cost of the stove in USD.
    fuel_cost: float, default 1.04
       Fuel cost in USD/kg.
    time_of_cooking: float, default 2
       Daily average time spent for cooking with this stove in hours.
    om_cost: float, default 3.7
       Operation and maintenance cost in USD/year.
    efficiency: float, default 0.5
       Efficiency of the stove.
    pm25: float, default 43
       Particulate Matter emissions (PM25) in mg/kg of fuel.
    travel_time: Pandas Series, optional
       Pandas Series describing the time needed (in hours) to reach either the closest LPG supply point or urban
       settlement  from each population point. It is either calculated using the LPG supply points, friction layer and
       population density layer or taken directly from a traveltime map.
    truck_capacity: float, default 2000
       Capacity of the truck carrying the fuel in kg.
    diesel_cost: float, 1.04
       Cost of diesel used in order to estimate the cost of transportation. Given in USD/liter
    diesel_per_hour: float, default 14
       Average diesel consumption of the truck carrying the fuel. Measured in liter/h
    lpg_path: str, optional
        Path to the lpg supply points (point vector file).
    friction_path: str, optional
       Path to the friction raster file describing the time needed (in minutes) to travel one meter within each
       cell using motorized transport.
    cylinder_cost: float, default 2.78
       Cost of LPG cylinder. This is relevant for first time buyers currenty not having access to an LPG cylinder.
       Given in USD/kg
    cylinder_life: float, 15
       Lifetime of LPG cylinder, measured in years.
    """

    def __init__(self,
                 name: Optional[str] = None,
                 carbon_intensity: Optional[float] = None ,
                 co2_intensity: float = 63,
                 ch4_intensity: float = 0.003,
                 n2o_intensity: float = 0.0001,
                 co_intensity: float = 0,
                 bc_intensity: float = 0.0044,
                 oc_intensity: float = 0.0091,
                 energy_content: float = 45.5,
                 tech_life: int = 7,  # in years
                 inv_cost: float = 44,  # in USD
                 fuel_cost: float = 0.73,
                 time_of_cooking: float = 2,
                 om_cost: float = 3.7,
                 efficiency: float = 0.5,  # ratio
                 pm25: float = 43,
                 travel_time: Optional[pd.Series] = None,
                 truck_capacity: float = 2000,
                 diesel_cost: float = 1.04,
                 diesel_per_hour: float = 14,
                 lpg_path: Optional[str] = None,
                 friction_path: Optional[str] = None,
                 cylinder_cost: float = 2.78,  # USD/kg,
                 cylinder_life: float = 15):
        super().__init__(name, carbon_intensity, co2_intensity, ch4_intensity,
                         n2o_intensity, co_intensity, bc_intensity, oc_intensity,
                         energy_content, tech_life, inv_cost, fuel_cost, time_of_cooking,
                         om_cost, efficiency, pm25, is_clean=True)
        self.travel_time = travel_time
        self.truck_capacity = truck_capacity
        self.diesel_cost = diesel_cost
        self.diesel_per_hour = diesel_per_hour
        self.transport_cost = None
        self.lpg_path = lpg_path
        self.friction_path = friction_path
        self.cylinder_cost = cylinder_cost
        self.cylinder_life = cylinder_life

    def add_travel_time(self, lpg_path: Optional[str] = None, friction_path: Optional[str] = None,
                        model: 'onstove.onstove.OnStove', align: bool = False):
        """This method calculates the travel time needed to transport LPG.

        The travel time is calculated as the time needed (in hours) to reach the closest LPG supplier from each
        population point. It uses a point layer for LPG suppliers, a friction layer and a population density layer.

        Parameters
        ----------
        lpg_path: str
            Path to the LPG supply points.
        friction_path: str
            Path to the friction raster file describing the time needed (in minutes) to travel one meter within each
            cell using motorized transport.
        model: OnStove model
            Instance of the OnStove model containing the main data of the study case. See
            :class:`onstove.onstove.OnStove`.
        align: bool, default False
            Boolean parameter to indicate if the friction layer need to be align with the population
            data in the `model`.
        """

        if lpg_path is None:
            lpg_path = self.lpg_path

        lpg = VectorLayer(self.name, 'Suppliers', path=lpg_path)

        if friction_path is None:
            friction_path = self.friction_path

        friction = RasterLayer(self.name, 'Friction', path=friction_path, resample='average')

        if align:
            os.makedirs(os.path.join(model.output_directory, self.name, 'Suppliers'), exist_ok=True)
            lpg.reproject(model.base_layer.meta['crs'], os.path.join(model.output_directory, self.name, 'Suppliers'))
            friction.align(model.base_layer.path, os.path.join(model.output_directory, self.name, 'Friction'))

        lpg.friction = friction
        lpg.travel_time(os.path.join(model.output_directory, self.name))
        self.travel_time = 2 * model.raster_to_dataframe(lpg.distance_raster.data,
                                                         nodata=lpg.distance_raster.meta['nodata'],
                                                         fill_nodata='interpolate', method='read')

    def transportation_cost(self, model: 'onstove.onstove.OnStove'):
        """The cost of transporting LPG.

        Transportation cost = (2 * diesel consumption per h * national diesel price * travel time)/transported LPG

        Total cost = (LPG cost + Transportation cost)/efficiency of LPG stoves

        For more information about cost formula see [1]_.

        The function uses the following attributes of model: ``diesel_per_hour``, ``diesel_cost``, ``travel_time``,
        ``truck_capacity``, ``efficiency`` and ``energy_content``.


        References
        ----------
        .. [1] Szabó, S., Bódis, K., Huld, T. & Moner-Girona, M. Energy solutions in rural Africa: mapping
        electrification costs of distributed solar and diesel generation versus grid extension.
        Environ. Res. Lett. 6, 034002 (2011).


        Parameters
        ----------
        model: OnStove model
            Instance of the OnStove model containing the main data of the study case. See
            :class:`onstove.onstove.OnStove`.
        """

        transport_cost = (self.diesel_per_hour * self.diesel_cost * self.travel_time) / self.truck_capacity
        kg_yr = (model.specs["Meals_per_day"] * 365 * model.energy_per_meal) / (
                self.efficiency * self.energy_content)  # energy content in MJ/kg
        transport_cost = transport_cost * kg_yr
        transport_cost[transport_cost < 0] = np.nan
        self.transport_cost = transport_cost

    def discount_fuel_cost(self, model: 'onstove.onstove.OnStove', relative: bool = True):
        """This method expands :meth:`discount_fuel_cost` when LPG is the stove assessed in order to ensure that the
         transportation costs are included

        Parameters
        ----------
        model: OnStove model
            Instance of the OnStove model containing the main data of the study case. See
            :class:`onstove.onstove.OnStove`.
        relative: bool, default True
            Boolean parameter to indicate if the discounted investments will be calculated relative to the `base_fuel`
            or not.

        See also
        --------
        discount_fuel_cost
        """

        self.transportation_cost(model)
        super().discount_fuel_cost(model, relative)

    def transport_emissions(self, model: 'onstove.onstove.OnStove'):
        """Calculates the emissions caused by the transportation of LPG. This is dependent on the diesel consumption of
         the truck. Diesel consumption is assumed to be 14 l/h (14 l/100km). Each truck is assumed to transport 2,000
         kg LPG

        Emissions intensities and diesel density are taken from [1]_.

        The function uses the following attributes of model: ``energy``, ``energy_content``, ``travel_time`` and
        ``truck_capacity``.

        .. [1]Ntziachristos, L. and Z. Samaras (2018), “1.A.3.b.i, 1.A.3.b.ii, 1.A.3.b.iii, 1.A.3.b.iv Passenger cars,
        light commercial trucks, heavy-duty vehicles including buses and motor cycles”, in EMEP/EEA air pollutant
        emission inventory guidebook 2016 – Update Jul. 2018

        Parameters
        ----------
        model: OnStove model
            Instance of the OnStove model containing the main data of the study case. See
            :class:`onstove.onstove.OnStove`.

        Returns
        -------
        The total transport emissions that can be associated with each household in kg of CO2-eq per year.
        """
        diesel_density = 840  # kg/m3
        bc_fraction = 0.55  # BC fraction of pm2.5
        oc_fraction = 0.70  # OC fraction of BC
        pm_diesel = 1.52  # g/kg_diesel
        diesel_ef = {'co2': 3.169, 'co': 7.40, 'n2o': 0.056,
                     'bc': bc_fraction * pm_diesel, 'oc': oc_fraction * bc_fraction * pm_diesel}  # g/kg_Diesel
        kg_yr = self.energy / self.energy_content  # LPG use (kg/yr). Energy required (MJ/yr)/LPG energy content (MJ/kg)
        diesel_consumption = self.travel_time * (14 / 1000) * diesel_density  # kg of diesel per trip
        hh_emissions = sum([ef * model.gwp[pollutant] * diesel_consumption / self.truck_capacity * kg_yr for
                            pollutant, ef in diesel_ef.items()])  # in gCO2eq per yr
        return hh_emissions / 1000  # in kgCO2eq per yr

    def carb(self, model: 'onstove.onstove.OnStove'):
        """This method expands :meth:`Technology.carbon` when LPG is the stove assessed in order to ensure that the
         emissions caused by the transportation is included.

        Parameters
        ----------
        model: OnStove model
            Instance of the OnStove model containing the main data of the study case. See
            :class:`onstove.onstove.OnStove`.

        See also
        --------
        transport_emissions
        """
        super().carb(model)
        self.carbon += self.transport_emissions(model)

    def infrastructure_cost(self, model: 'onstove.onstove.OnStove'):
        """Calculates cost of cylinders for first-time LPG users. It is assumed that the cylinder contains 12.5 kg of
        LPG. The function calls ``infrastructure_salvage``.

        The function uses the ``cylinder_cost`` attribute of the model.

        Parameters
        ----------
        model: OnStove model
            Instance of the OnStove model containing the main data of the study case. See
            :class:`onstove.onstove.OnStove`.

        See also
        --------
        infrastructure_salvage
        """
        cost = self.cylinder_cost * 12.5
        salvage = self.infrastructure_salvage(model, cost, self.cylinder_life)
        self.discounted_infra_cost = (cost - salvage)

    def infrastructure_salvage(self, model: 'onstove.onstove.OnStove', cost: float, life: int):
        """Calculates the salvaged cylinder cost. The function calls ``discount_factor``.

        Parameters
        ----------
        model: OnStove model
            Instance of the OnStove model containing the main data of the study case. See
            :class:`onstove.onstove.OnStove`.
        cost: float
            The cost of buying an LPG-cylinder.
        life: int
            The lifetime of a cylinder.

        Returns
        -------
        The discounted salvage cost of an LPG-cylinder.

        See also
        --------
        discount_factor
        """
        discount_rate, proj_life = self.discount_factor(model.specs)
        used_life = proj_life % life
        salvage = cost * (1 - used_life / life)
        return salvage / discount_rate[0]

    def discounted_inv(self, model: 'onstove.onstove.OnStove', relative: bool = True):
        """This method expands :meth:`Technology.discounted_inv` by adding the cylinder cost for households currently
        not using LPG.

        Parameters
        ----------
        model: OnStove model
            Instance of the OnStove model containing the main data of the study case. See
            :class:`onstove.onstove.OnStove`.
        relative: bool, default True
            Boolean parameter to indicate if the discounted investments will be calculated relative to the `base_fuel`
            or not.

        See also
        --------
        infrastructure_cost
        """

        super().discounted_inv(model, relative=relative)
        self.infrastructure_cost(model)
        if relative:
            share = (model.gdf['IsUrban'] > 20) * self.current_share_urban
            share[model.gdf['IsUrban'] < 20] *= self.current_share_rural
            self.discounted_investments += (self.discounted_infra_cost * (1 - share))


class Biomass(Technology):
    """Biomass technology class used to model traditional and improved stoves.

    This class inherits the standard :class:`Technology` class and is used to model traditional and Improved Cook
    Stoves (ICS) using biomass as fuel. The biomass can be either collected or purchased, which is indicated with the
    attribute ``collected_fuel``. Depending on the biomass type (e.g. fuelwood or pellets), the parameters passed to
    the class such as efficiency, energy content, pm25 and emissions need to be representative of the fuel-stove.
    Moreover, the ICS can be modelled as natural draft or forced draft options by specifying it with the
    ``draft_type`` attribute. If forced draft is used, then the class will consider and extra capital cost for a
    standard 6 watt solar panel in order to run the fan in unelectrified areas.

    Attributes
    ----------
    forest: object of type RasterLayer, optional
        This is the forest cover raster dataset read from the ``forest_path`` parameter. See the
        :class:`onstove.layer.RasterLayer` class for more information.
    friction: str, optional
        This is the forest cover raster dataset read from the ``friction_path``.
    trips_per_yr: float
        The trips that a person per household needs to do to the nearest forest point, in order to collect the amount
        of biomass required for cooking in one year.

    Parameters
    ----------
    name: str, optional.
        Name of the technology to model.
    carbon_intensity: float, optional
        The CO2 equivalent emissions in kg/GJ of burned fuel. If this attribute is used, then none of the
        gas-specific intensities will be used (e.g. ch4_intensity).
    co2_intensity: float, default 112
        The CO2 emissions in kg/GJ of burned fuel.
    ch4_intensity: float, default 0.864
        The CH4 emissions in kg/GJ of burned fuel.
    n2o_intensity: float, default 0.0039
        The N2O emissions in kg/GJ of burned fuel.
    co_intensity: float, default 0
        The CO emissions in kg/GJ of burned fuel.
    bc_intensity: float, default 0.1075
        The black carbon emissions in kg/GJ of burned fuel.
    oc_intensity: float, default 0.308
        The organic carbon emissions in kg/GJ of burned fuel.
    energy_content: float, default 16
        Energy content of the fuel in MJ/kg.
    tech_life: int, default 2
        Stove life in year.
    inv_cost: float, default 0
        Investment cost of the stove in USD.
    fuel_cost: float, default 0
        Fuel cost in USD/kg if any.
    time_of_cooking: float, default 2.9
        Daily average time spent for cooking with this stove in hours.
    om_cost: float, default 0
        Operation and maintenance cost in USD/year.
    efficiency: float, default 0.12
        Efficiency of the stove.
    pm25: float, default 844
        Particulate Matter emissions (PM25) in mg/kg of fuel.
    forest_path: str, optional
        Path to the forest cover raster file.
    friction_path: str, optional
        Path to the friction raster file describing the time needed (in minutes) to travel one meter within each
        cell.
    travel_time: Pandas Series, optional
        Pandas Series describing the time needed (in hours) to reach the closest forest cover point from each
        population point. It is calculated using the forest cover, friction layer and population density layer.

        .. seealso::
           :meth:`transportation_time<onstove.technology.Biomass.transportation_time>` and
           :meth:`total_time<onstove.technology.Biomass.total_time>`

    collection_capacity: float, default 25
        Average wood collection capacity per person in kg/trip.
    collected_fuel: bool, default True
        Boolean indicating if the fuel is collected or purchased. If True, then the ``travel_time`` will be
        calculated. If False, the ``fuel_cost`` will be used and a travel and collection time disregarded.
    time_of_collection: float, default 2
        Time spent collecting biomass on a single trip (excluding travel time) in hours.
    draft_type: str, default 'natural'
        Whether the ICS uses a natural draft or a forced draft.
    forest_condition: Callable object (function or lambda function) with a numpy array as input, optional
        Function or lambda function describing which forest canopy cover to consider when assessing the potential
        points for biomass collection.

        .. code-block:: python
           :caption: **Example**: lambda function for canopy cover equal or over 30%

           forest_condition = lambda  x: x >= 0.3

    Examples
    --------
    An OnStove Biomass class can be created by providing the technology input data on an `csv` file and calling the
    :meth:`read_tech_data<onstove.onstove.OnStove.read_tech_data>` method of the
    :class:`OnStove<onstove.onstove.OnStove>` class, or by passing all technology information in the script.

    Creating the technologies from a `csv` configuration file (see *link to examples or mendeley* for a example of the
    configuration file):

    >>> from onstove.onstove import OnStove
    ... model = OnStove(output_directory='output_directory')
    ... mode.read_tech_data(path_to_config='path_to_csv_file', delimiter=',')
    ... model.techs
    {'Biomass': {'Biomass': <onstove.technology.Biomass at 0x2478e85ee80>}}

    Creating a Biomass technology in the script:

    >>> from onstove.onstove import OnStove
    ... from onstove.technology import Biomass
    ... model = OnStove(output_directory='output_directory')
    ... biomass = Biomass(name='Biomass')  # we define the name and leave all other parameters with the default values
    ... model.techs['Biomass'] = biomass
    ... model.techs
    {'Biomass': {'Biomass': <onstove.technology.Biomass at 0x2478e85ee80>}}
    """

    forest: Optional[RasterLayer] = None
    friction: Optional[RasterLayer] = None
    trips_per_yr: float = 0.0

    def __init__(self,
                 name: Optional[str] = None,
                 carbon_intensity: Optional[float] = None,
                 co2_intensity: float = 112,
                 ch4_intensity: float = 0.864,
                 n2o_intensity: float = 0.0039,
                 co_intensity: float = 0,
                 bc_intensity: float = 0.1075,
                 oc_intensity: float = 0.308,
                 energy_content: float = 16,
                 tech_life: int = 2,
                 inv_cost: float = 0,
                 fuel_cost: float = 0,
                 time_of_cooking: float = 2.9,
                 om_cost: float = 0,
                 efficiency: float = 0.12,
                 pm25: float = 844,
                 forest_path: Optional[str] = None,
                 friction_path: Optional[str] = None,
                 travel_time: Optional[pd.Series] = None,
                 collection_capacity: float = 25,
                 collected_fuel: bool = True,
                 time_of_collection: float = 2,
                 draft_type: str = 'natural',
                 forest_condition: Optional[Callable[[np.ndarray], np.ndarray]] = None):
        """Instantiates the class either with default or user defined values for each class attribute.
        """
        super().__init__(name, carbon_intensity, co2_intensity, ch4_intensity,
                         n2o_intensity, co_intensity, bc_intensity, oc_intensity,
                         energy_content, tech_life,
                         inv_cost, fuel_cost, time_of_cooking,
                         om_cost, efficiency, pm25, is_clean=False)

        self.forest_condition = forest_condition
        self.travel_time = travel_time
        self.forest_path = forest_path
        self.friction_path = friction_path
        self.collection_capacity = collection_capacity
        self.draft_type = draft_type
        self.collected_fuel = collected_fuel
        self.time_of_collection = time_of_collection
        self.solar_panel_adjusted: bool = False  #: boolean check to avoid adding the solar panel cost twice

    def __setitem__(self, idx, value):
        self.__dict__[idx] = value

    def transportation_time(self, friction_path: str, forest_path: str, model: 'onstove.onstove.OnStove', align: bool = False):
        """This method calculates the travel time needed to gather biomass.

        The travel time is calculated as the time needed (in hours) to reach the closest forest cover point from each
        population point. It uses a forest cover layer, a friction layer and population density layer.

        Parameters
        ----------
        friction_path: str
            Path to the friction raster file describing the time needed (in minutes) to travel one meter within each
            cell.
        forest_path: str
            Path to the forest cover raster file.
        model: OnStove model
            Instance of the OnStove model containing the main data of the study case. See
            :class:`onstove.onstove.OnStove`.
        align: bool, default False
            Boolean parameter to indicate if the forest cover and friction layers need to be align with the population
            data in the `model`.
        """
        self.forest = RasterLayer(self.name, 'Forest', path=forest_path, resample='mode')
        self.friction = RasterLayer(self.name, 'Friction', path=friction_path, resample='average')

        if align:
            self.forest.align(model.base_layer.path, os.path.join(model.output_directory, self.name, 'Forest'))
            self.friction.align(model.base_layer.path, os.path.join(model.output_directory, self.name, 'Friction'))

        self.forest.friction = self.friction
        self.forest.travel_time(condition=self.forest_condition)

        travel_time = 2 * model.raster_to_dataframe(self.forest.distance_raster.data,
                                                    nodata=self.forest.distance_raster.meta['nodata'],
                                                    fill_nodata='interpolate', method='read')
        travel_time[travel_time > 7] = 7  # cap to max travel time based on literature
        self.travel_time = travel_time

    def total_time(self, model: 'onstove.onstove.OnStove'):
        """This method expands :meth:`Technology.total_time` when biomass is collected.

        It calculates the time needed for collecting biomass, based on the ``collection_capacity`` the
        ``energy_content`` of the fuel, the ``energy`` required for cooking a standard meal and the travel time to
        the nearest forest area.

        Parameters
        ----------
        model: OnStove model
            Instance of the OnStove model containing the main data of the study case. See
            :class:`onstove.onstove.OnStove`.
        """
        if self.collected_fuel:
            self.transportation_time(self.friction_path, self.forest_path, model)
            self.trips_per_yr = self.energy / (self.collection_capacity * self.energy_content)
            self.total_time_yr = self.time_of_cooking * 365 + \
                                 (self.travel_time + self.time_of_collection) * self.trips_per_yr
        else:
            self.time_of_collection = 0
            super().total_time(model)

    def get_carbon_intensity(self, model: 'onstove.onstove.OnStove'):
        """This method expands :meth:`Technology.get_carbon_intensity`.

        It excludes the CO2 emissions from the share of firewood that is sustainably harvested (i.e. it does not affect
        other emissions such as CH4) by using the fraction of Non-Renewable Biomass (fNRB).

        Parameters
        ----------
        model: OnStove model
            Instance of the OnStove model containing the main data of the study case. See
            :class:`onstove.onstove.OnStove`.

        Notes
        -----
        For more information about fNRB see [1]_.

        References
        ----------
        .. [1] R. Bailis, R. Drigo, A. Ghilardi, O. Masera, The carbon footprint of traditional woodfuels,
           Nature Clim Change. 5 (2015) 266–272. https://doi.org/10.1038/nclimate2491.
        """
        intensity = self['co2_intensity']
        self['co2_intensity'] *= model.specs['fnrb']
        super().get_carbon_intensity(model)
        self['co2_intensity'] = intensity

    def solar_panel_investment(self, model: 'onstove.onstove.OnStove'):
        """This method adds the cost of a solar panel to unelectrified areas.

        The stove can be modelled a ICS with natural draft or forced draft. This is achieved by specifying the
        ``draft_type`` attribute of the class. If forced draft is used, then the class will consider and extra capital
        cost for a standard 6 watt solar panel in order to run the fan in unelectrified areas. The cost used for the
        panel is 1.25 USD per watt.

        Parameters
        ----------
        model: OnStove model
            Instance of the OnStove model containing the main data of the study case. See
            :class:`onstove.onstove.OnStove`.
        """
        if not self.solar_panel_adjusted:
            solar_panel_cost = 7.5  # Based on a cost of 1.25 USD per watt
            is_electrified = model.gdf['Elec_pop_calib'] > 0
            inv_cost = pd.Series(np.ones(model.gdf.shape[0]) * self.inv_cost, index=model.gdf.index)
            inv_cost[~is_electrified] += solar_panel_cost
            self.inv_cost = inv_cost
            self.solar_panel_adjusted = True  # This is to prevent to adjust the capital cost more than once

    def discounted_inv(self, model: 'onstove.onstove.OnStove', relative: bool = True):
        """This method expands :meth:`Technology.discounted_inv` by adding the solar panel cost in unlectrified areas.

        Parameters
        ----------
        model: OnStove model
            Instance of the OnStove model containing the main data of the study case. See
            :class:`onstove.onstove.OnStove`.
        relative: bool, default True
            Boolean parameter to indicate if the discounted investments will be calculated relative to the `base_fuel`
            or not.

        See also
        --------
        solar_panel_investment
        """
        if self.draft_type.lower().replace('_', ' ') in ['forced', 'forced draft']:
            self.solar_panel_investment(model)
        super().discounted_inv(model, relative=relative)


class Charcoal(Technology):
    """Charcoal technology class used to model traditional and improved stoves.

    This class inherits the standard :class:`Technology` class and is used to model traditional and Improved Cook
    Stoves (ICS) using charcoal as fuel.

    Parameters
    ----------
    name: str, optional.
        Name of the technology to model.
    carbon_intensity: float, optional
        The CO2 equivalent emissions in kg/GJ of burned fuel. If this attribute is used, then none of the
        gas-specific intensities will be used (e.g. ch4_intensity).
    co2_intensity: float, default 121
        The CO2 emissions in kg/GJ of burned fuel.
    ch4_intensity: float, default 0.576
        The CH4 emissions in kg/GJ of burned fuel.
    n2o_intensity: float, default 0.001
        The N2O emissions in kg/GJ of burned fuel.
    co_intensity: float, default 0
        The CO emissions in kg/GJ of burned fuel.
    bc_intensity: float, default 0.1075
        The black carbon emissions in kg/GJ of burned fuel.
    oc_intensity: float, default 0.308
        The organic carbon emissions in kg/GJ of burned fuel.
    energy_content: float, default 30
        Energy content of the fuel in MJ/kg.
    tech_life: int, default 2
        Stove life in year.
    inv_cost: float, default 4
        Investment cost of the stove in USD.
    fuel_cost: float, default 0.09
        Fuel cost in USD/kg if any.
    time_of_cooking: float, default 2.6
        Daily average time spent for cooking with this stove in hours.
    om_cost: float, default 3.7
        Operation and maintenance cost in USD/year.
    efficiency: float, default 0.2
        Efficiency of the stove.
    pm25: float, default 256
        Particulate Matter emissions (PM25) in mg/kg of fuel.
    """

    def __init__(self,
                 name: Optional[str] = None,
                 carbon_intensity: Optional[float] = None,
                 co2_intensity: float = 121,
                 ch4_intensity: float = 0.576,
                 n2o_intensity: float = 0.001,
                 co_intensity: float = 0,
                 bc_intensity: float = 0.1075,
                 oc_intensity: float = 0.308,
                 energy_content: float = 30,
                 tech_life: float = 2,  # in years
                 inv_cost: int = 4,  # in USD
                 fuel_cost: float = 0.09,
                 time_of_cooking: float = 2.6,
                 om_cost: float = 3.7,
                 efficiency: float = 0.2,  # ratio
                 pm25: float = 256):
        super().__init__(name, carbon_intensity, co2_intensity, ch4_intensity,
                         n2o_intensity, co_intensity, bc_intensity, oc_intensity,
                         energy_content, tech_life,
                         inv_cost, fuel_cost, time_of_cooking,
                         om_cost, efficiency, pm25, is_clean=False)

    def get_carbon_intensity(self, model):
        """This method expands :meth:`Technology.get_carbon_intensity`.

        It excludes the CO2 emissions from the share of firewood that is sustainably harvested (i.e. it does not affect
        other emissions such as CH4) by using the fraction of Non-Renewable Biomass (fNRB).

        Parameters
        ----------
        model: OnStove model
            Instance of the OnStove model containing the main data of the study case. See
            :class:`onstove.onstove.OnStove`.

        Notes
        -----
        For more information about fNRB see [1]_.

        References
        ----------
        .. [1] R. Bailis, R. Drigo, A. Ghilardi, O. Masera, The carbon footprint of traditional woodfuels,
           Nature Clim Change. 5 (2015) 266–272. https://doi.org/10.1038/nclimate2491.
        """
        intensity = self['co2_intensity']
        self['co2_intensity'] *= model.specs['fnrb']
        super().get_carbon_intensity(model)
        self['co2_intensity'] = intensity

    def production_emissions(self, model):
        """Calculates the emissions caused by the production of Charcoal. The function uses emission factors with regards
        to CO2, CO, CH4, BC and OC as well as the ``energy`` and ``energy_content`` attributes of te model.
        Emissions factors for the production of charcoal are taken from [1]_.


        References
        ----------
        .. [1]Akagi, S. K., Yokelson, R. J., Wiedinmyer, C., Alvarado, M. J., Reid, J. S., Karl, T., Crounse, J. D.,
            & Wennberg, P. O. (2010). Emission factors for open and domestic biomass burning for use in atmospheric
            models. Atmospheric Chemistry and Physics Discussions. 10: 27523–27602., 27523–27602.
            https://www.fs.usda.gov/treesearch/pubs/39297

        Parameters
        ----------
        model: OnStove model
            Instance of the OnStove model containing the main data of the study case. See
            :class:`onstove.onstove.OnStove`.

        Returns
        -------
        The total charcoal production emissions that can be associated with each household measured in
        kg of CO2-eq per year.
        """
        emission_factors = {'co2': 1626, 'co': 255, 'ch4': 39.6, 'bc': 0.02, 'oc': 0.74}  # g/kg_Charcoal
        # Charcoal produced (kg/yr). Energy required (MJ/yr)/Charcoal energy content (MJ/kg)
        kg_yr = self.energy / self.energy_content
        hh_emissions = sum([ef * model.gwp[pollutant] * kg_yr for pollutant, ef in
                            emission_factors.items()])  # gCO2eq/yr
        return hh_emissions / 1000  # kgCO2/yr

    def carb(self, model):
        """This method expands :meth:`Technology.carbon` when Charcoal is the fuel used (both traditional stoves and ICS)
         in order to ensure that the emissions caused by the production and transportation is included in the total emissions.

        Parameters
        ----------
        model: OnStove model
            Instance of the OnStove model containing the main data of the study case. See
            :class:`onstove.onstove.OnStove`.

        See also
        --------
        carbon
        """
        super().carb(model)
        self.carbon += self.transport_emissions(model)
        super().carb(model)
        self.carbon += self.production_emissions(model)


class Electricity(Technology):
    """Electricity technology class used to model electrical stoves.

    This class inherits the standard :class:`Technology` class and is used to model electrical stoves.

    Parameters
    ----------
    name: str, optional
        Name of the technology to model.
    carbon_intensity: float, optional
        The CO2 equivalent emissions in kg/GJ of burned fuel. If this attribute is used, then none of the
        gas-specific intensities will be used (e.g. ch4_intensity).
    energy_content: float, default 3.6
        Energy content in MJ/kWh.
    tech_life: int, default 10
        Stove life in year.
    connection_cost: float, defualt 2
        Cost of strengthening a household connection to enable electrical cooking.
    grid_capacity_cost: float, optional
        Cost of added capacity in the grid (USD/kW)
    inv_cost: float, default 4
        Investment cost of the stove in USD.
    fuel_cost: float, default 0.09
        Fuel cost in USD/kg if any.
    time_of_cooking: float, default 2.6
        Daily average time spent for cooking with this stove in hours.
    om_cost: float, default 3.7
        Operation and maintenance cost in USD/year.
    efficiency: float, default 0.2
        Efficiency of the stove.
    pm25: float, default 256
        Particulate Matter emissions (PM25) in mg/kg of fuel.
    """

    def __init__(self,
                 name=None,
                 carbon_intensity=None,
                 energy_content=0,
                 tech_life=0,  # in years
                 inv_cost=0,  # in USD
                 connection_cost=0,  # cost of additional infrastructure
                 grid_capacity_cost=None,
                 fuel_cost=0,
                 time_of_cooking=0,
                 om_cost=0,  # percentage of investement cost
                 efficiency=0,  # ratio
                 pm25=41):
        super().__init__(name, carbon_intensity, None, None, None,
                         None, None, None, energy_content, tech_life,
                         inv_cost, fuel_cost, time_of_cooking,
                         om_cost, efficiency, pm25, is_clean=True)
        # Carbon intensity of fossil fuel plants in kg/GWh
        self.generation = {}
        self.capacities = {}
        self.grid_capacity_cost = grid_capacity_cost
        self.tiers_path = None
        self.connection_cost = connection_cost
        self.carbon_intensities = {'coal': 0.090374363, 'natural_gas': 0.050300655,
                                   'crude_oil': 0.070650288, 'heavy_fuel_oil': 0.074687989,
                                   'oil': 0.072669139, 'diesel': 0.069332823,
                                   'still_gas': 0.060849859, 'flared_natural_gas': 0.051855075,
                                   'waste': 0.010736111, 'biofuels_and_waste': 0.010736111,
                                   'nuclear': 0, 'hydro': 0, 'wind': 0,
                                   'solar': 0, 'other': 0, 'geothermal': 0}
        # TODO: make this general, with other fuel mix this crash
        self.grid_capacity_costs = {'oil': 1467, 'natural_gas': 550,
                                    'biofuels_and_waste': 2117,
                                    'nuclear': 4000, 'hydro': 2100, 'coal': 1600, 'wind': 1925,
                                    'solar': 1400, 'geothermal': 2917}
        self.grid_techs_life = {'oil': 40, 'natural_gas': 30,
                                'biofuels_and_waste': 25,
                                'nuclear': 50, 'hydro': 60, 'coal': 40, 'wind': 22,
                                'solar': 25, 'geothermal': 30}

    def __setitem__(self, idx, value):
        if 'generation' in idx:
            self.generation[idx.lower().replace('generation_', '')] = value
        elif 'grid_capacity_cost' in idx:
            self.grid_capacity_cost = value
        elif 'capacity' in idx:
            self.capacities[idx.lower().replace('capacity_', '')] = value
        elif 'carbon_intensity' == idx:
            self.carbon_intensity = value
        elif 'carbon_intensity' in idx:
            self.carbon_intensities[idx.lower().replace('carbon_intensity_', '')] = value
        elif 'connection_cost' in idx:
            self.connection_cost = value
        elif 'grid_cap_life' in idx:
            self.grid_cap_life = value
        else:
            super().__setitem__(idx, value)

    def get_capacity_cost(self, model):
        self.required_energy(model)
        if self.tiers_path is None:
            add_capacity = 1
        else:
            model.raster_to_dataframe(self.tiers_path, name='Electricity_tiers', method='sample')
            self.tiers = model.gdf['Electricity_tiers'].copy()
            add_capacity = (self.tiers < 3)

        if self.grid_capacity_cost is None:
            self.get_grid_capacity_cost()
            salvage = self.grid_salvage(model)
        else:
            salvage = self.grid_salvage(model, True)

        self.capacity = self.energy * add_capacity / (3.6 * self.time_of_cooking * 365)
        self.capacity_cost = self.capacity * (self.grid_capacity_cost - salvage)

    def get_carbon_intensity(self, model):
        grid_emissions = sum([gen * self.carbon_intensities[fuel] for fuel, gen in self.generation.items()])
        grid_generation = sum(self.generation.values())
        self.carbon_intensity = grid_emissions / grid_generation * 1000  # to convert from Mton/PJ to kg/GJ

    def get_grid_capacity_cost(self):
        self.grid_capacity_cost = sum(
            [self.grid_capacity_costs[fuel] * (cap / sum(self.capacities.values())) for fuel, cap in
             self.capacities.items()])

    def grid_salvage(self, model, single=False):
        discount_rate, proj_life = self.discount_factor(model.specs)
        if single:
            used_life = proj_life % self.grid_cap_life
            salvage = self.grid_capacity_cost * (1 - used_life / self.grid_cap_life)
        else:
            salvage_values = []

            for tech, cap in self.capacities.items():
                used_life = proj_life % self.grid_techs_life[tech]
                salvage = self.grid_capacity_costs[tech] * (1 - used_life / self.grid_techs_life[tech])
                salvage_values.append(salvage * cap / sum(self.capacities.values()))

            salvage = sum(salvage_values)

        return salvage / discount_rate[0]

    def carb(self, model):
        if self.carbon_intensity is None:
            self.get_carbon_intensity(model)
        super().carb(model)

    def discounted_inv(self, model, relative=True):
        super().discounted_inv(model, relative=relative)
        if relative:
            share = (model.gdf['IsUrban'] > 20) * self.current_share_urban
            share[model.gdf['IsUrban'] < 20] *= self.current_share_rural
            self.discounted_investments += (self.connection_cost + self.capacity_cost * (1 - share))

    def total_costs(self):
        super().total_costs()

    def net_benefit(self, model, w_health=1, w_spillovers=1, w_environment=1, w_time=1, w_costs=1):
        super().net_benefit(model, w_health, w_spillovers, w_environment, w_time, w_costs)
        model.gdf.loc[model.gdf['Current_elec'] == 0, "net_benefit_{}".format(self.name)] = np.nan
        factor = model.gdf['Elec_pop_calib'] / model.gdf['Calibrated_pop']
        factor[factor > 1] = 1
        self.factor = factor
        self.households = model.gdf['Households'] * factor


class Biogas(Technology):
    """Biogas technology class used to model biogas fueled stoves. This class inherits the standard
    :class:`Technology` class and is used to model stove using biogas as fuel. Biogas stoves are assumed to not
    be available in urban settlements as the collection of manure is assumed to be limited. If the fuel is assumed
    to be purchased changes can be made to the function called ``available_biogas``. Biogas is also assumed to be
    restricted based on temperature (an average yearly temperature below 10 degrees Celsius is assumed to lead to
    heavy drops of efficiency [1]_). Biogas production is also assumed to be a very water intensive process [2]_, hence
    areas under water stress are assumed restricted as well.

    References
    ----------
    .. [1]Lohani, S. P., Dhungana, B., Horn, H. & Khatiwada, D. Small-scale biogas technology and clean cooking fuel:
        Assessing the potential and links with SDGs in low-income countries – A case study of Nepal.
        Sustainable Energy Technologies and Assessments 46, 101301 (2021).
    .. [2]Bansal, V., Tumwesige, V. & Smith, J. U. Water for small-scale biogas digesters in sub-Saharan Africa.
        GCB Bioenergy 9, 339–357 (2017).

    Parameters
    ----------
    name: str, optional.
        Name of the technology to model.
    carbon_intensity: float, optional
        The CO2 equivalent emissions in kg/GJ of burned fuel. If this attribute is used, then none of the
        gas-specific intensities will be used (e.g. ch4_intensity).
    co2_intensity: float, default 0
        The CO2 emissions in kg/GJ of burned fuel.
    ch4_intensity: float, default 0.029
        The CH4 emissions in kg/GJ of burned fuel.
    n2o_intensity: float, default 0.0006
        The N2O emissions in kg/GJ of burned fuel.
    co_intensity: float, default 0
        The CO emissions in kg/GJ of burned fuel.
    bc_intensity: float, default 0.0043
        The black carbon emissions in kg/GJ of burned fuel.
    oc_intensity: float, default 0.0091
        The organic carbon emissions in kg/GJ of burned fuel.
    energy_content: float, default 22.8
        Energy content of the fuel in MJ/kg.
    tech_life: int, default 20
        Stove life in year.
    inv_cost: float, default 550
        Investment cost of the stove in USD.
    fuel_cost: float, default 0
        Fuel cost in USD/kg if any.
    time_of_cooking: float, default 2
        Daily average time spent for cooking with this stove in hours.
    time_of_collection: float, default 3
        Time spent collecting biomass on a single trip (excluding travel time) in hours.
    om_cost: float, default 3.7
        Operation and maintenance cost in USD/year.
    efficiency: float, default 0.4
        Efficiency of the stove.
    pm25: float, default 43
        Particulate Matter emissions (PM25) in mg/kg of fuel.
    digestor_eff: float, default 0.4
        Efficiency of the digestor.
    friction_path: str, optional
        Path to the friction raster file describing the time needed (in minutes) to travel one meter within each
        cell.
    """

    def __init__(self,
                 name: Optional[str] = None,
                 carbon_intensity: Optional[float] = None,
                 co2_intensity: float = 0,
                 ch4_intensity: float = 0.029,
                 n2o_intensity: float = 0.0006,
                 co_intensity: float = 0,
                 bc_intensity: float = 0.0043,
                 oc_intensity: float = 0.0091,
                 energy_content: float = 22.8,
                 tech_life: int = 20,  # in years
                 inv_cost: float = 550,  # in USD
                 fuel_cost: float = 0,
                 time_of_cooking: float = 2,
                 time_of_collection: float = 3,
                 om_cost: float = 3.7,
                 efficiency: float = 0.4,  # ratio
                 pm25: float = 43,
                 digestor_eff: float = 0.4,
                 friction_path: Optional[str] = None):
        super().__init__(name, carbon_intensity, co2_intensity, ch4_intensity,
                         n2o_intensity, co_intensity, bc_intensity, oc_intensity,
                         energy_content, tech_life,
                         inv_cost, fuel_cost, time_of_cooking,
                         om_cost, efficiency, pm25, is_clean=True)

        self.digestor_eff = digestor_eff
        self.friction_path = friction_path
        self.time_of_collection = time_of_collection
        self.water = None
        self.temperature = None

    def read_friction(self, model, friction_path):
        """Reads a friction layer in min per meter (walking time per meter) and returns a pandas series with the values
        for each populated grid cell in hours per meter

        Parameters
        ----------
        model: OnStove model
            Instance of the OnStove model containing the main data of the study case. See
            :class:`onstove.onstove.OnStove`.
        friction_path: str
            Path to where the friction layer is stored.

        Returns
        -------
        A pandas series with the values for each populated grid cell in hours per meter
        """
        friction = RasterLayer(self.name, 'Friction', path=friction_path, resample='average')
        data = model.raster_to_dataframe(friction.data, nodata=friction.meta['nodata'],
                                         fill_nodata='interpolate', method='read')
        return data / 60

    def required_energy_hh(self, model):
        """Determines the required annual energy needed for cooking taking into account the stove efficiency.

        Parameters
        ----------
        model: OnStove model
            Instance of the OnStove model containing the main data of the study case. See
            :class:`onstove.onstove.OnStove`.

        Returns
        -------
        Required annual energy needed for cooking
        """

        self.required_energy(model)
        return self.energy / self.digestor_eff

    def get_collection_time(self, model):
        """Caluclates the daily time of collection based on friction (hour/meter), the available biogas energy from
        each cell (MJ/yr/meter, 1000000 represents meters per km2) and the required energy per household (MJ/yr)

        Parameters
        ----------
        model: OnStove model
            Instance of the OnStove model containing the main data of the study case. See
            :class:`onstove.onstove.OnStove`.

        """
        self.available_biogas(model)
        required_energy_hh = self.required_energy_hh(model)

        friction = self.read_friction(model, self.friction_path)

        time_of_collection = required_energy_hh * friction / (model.gdf["biogas_energy"] / 1000000) / 365
        time_of_collection[time_of_collection == float('inf')] = np.nan
        mean_value = time_of_collection.mean()
        time_of_collection[time_of_collection.isna()] = mean_value
        self.time_of_collection = time_of_collection

    def available_biogas(self, model):
        """Caluclates the biogas production potential in liters per day. It currently takes into account 6 categories
        of livestock (cattle, buffalo, sheep, goat, pig and poultry). The biogas potential for each category is determined
        following the methodology outlined by Lohani et al.[1]_ This function also applies a restriction to biogas
        production with regards to urban areas, areas with temperature lower than 10 degrees[1]_ celsius and areas under
        water stress[2]_.

        References
        ----------
        .. [1]Lohani, S. P., Dhungana, B., Horn, H. & Khatiwada, D. Small-scale biogas technology and clean cooking
            fuel: Assessing the potential and links with SDGs in low-income countries – A case study of Nepal.
            Sustainable Energy Technologies and Assessments 46, 101301 (2021).
        .. [2]Bansal, V., Tumwesige, V. & Smith, J. U. Water for small-scale biogas digesters in sub-Saharan Africa.
            GCB Bioenergy 9, 339–357 (2017).

        Parameters
        ----------
        model: OnStove model
            Instance of the OnStove model containing the main data of the study case. See
            :class:`onstove.onstove.OnStove`.

        """

        from_cattle = model.gdf["Cattles"] * 12 * 0.15 * 0.8 * 305
        from_buffalo = model.gdf["Buffaloes"] * 14 * 0.2 * 0.75 * 305
        from_sheep = model.gdf["Sheeps"] * 0.7 * 0.25 * 0.8 * 452
        from_goat = model.gdf["Goats"] * 0.6 * 0.3 * 0.85 * 450
        from_pig = model.gdf["Pigs"] * 5 * 0.75 * 0.14 * 470
        from_poultry = model.gdf["Poultry"] * 0.12 * 0.25 * 0.75 * 450


        model.gdf["available_biogas"] = ((from_cattle + from_buffalo + from_goat + from_pig + from_poultry +
                                          from_sheep) * self.digestor_eff / 1000) * 365

        # Temperature restriction
        if self.temperature is not None:
            if isinstance(self.temperature, str):
                self.temperature = RasterLayer('Biogas', 'Temperature', self.temperature)

            model.raster_to_dataframe(self.temperature.data, name="Temperature", method='read',
                                      nodata=self.temperature.meta['nodata'], fill_nodata='interpolate')
            model.gdf.loc[model.gdf["Temperature"] < 10, "available_biogas"] = 0
            model.gdf.loc[(model.gdf["IsUrban"] > 20), "available_biogas"] = 0

        # Water availability restriction
        if self.water is not None:
            if isinstance(self.water, str):
                self.water = VectorLayer('Biogas', 'Water scarcity', self.water, bbox=model.mask_layer.data)
            model.raster_to_dataframe(self.water.data, name="Water",
                                      fill_nodata='interpolate', method='read')
            model.gdf.loc[model.gdf["Water"] == 0, "available_biogas"] = 0

        # Available biogas energy per year in MJ (energy content in MJ/m3)
        model.gdf["biogas_energy"] = model.gdf["available_biogas"] * self.energy_content

    def recalibrate_livestock(self, model, buffaloes, cattles, poultry, goats, pigs, sheeps):
        """Recalibrates the livestock maps and adds them to the main dataframe. It currently takes into account 6 categories
        of livestock (cattle, buffalo, sheep, goat, pig and poultry).

        Parameters
        ----------
        model: OnStove model
            Instance of the OnStove model containing the main data of the study case. See
            :class:`onstove.onstove.OnStove`.
        buffaloes: str
            Path to the buffalo dataset.
        cattles: str
            Path to the cattle dataset.
        poultry: str
            Path to the poultry dataset.
        goats: str
            Path to the goat dataset.
        pigs: str
            Path to the pig dataset.
        sheeps: str
            Path to the sheep dataset.
        """
        paths = {
            'Buffaloes': buffaloes,
            'Cattles': cattles,
            'Poultry': poultry,
            'Goats': goats,
            'Pigs': pigs,
            'Sheeps': sheeps}

        for name, path in paths.items():
            layer = RasterLayer('Livestock', name,
                                path=path)
            model.raster_to_dataframe(layer.data, name=name, method='read',
                                      nodata=layer.meta['nodata'], fill_nodata='interpolate')

    def total_time(self, model):
        """This method expands :meth:`Technology.total_time` by adding the biogas collection time

        Parameters
        ----------
        model: OnStove model
            Instance of the OnStove model containing the main data of the study case. See
            :class:`onstove.onstove.OnStove`.

        See also
        --------
        total_time
        """
        self.get_collection_time(model)
        super().total_time(model)

    def net_benefit(self, model, w_health=1, w_spillovers=1, w_environment=1, w_time=1, w_costs=1):
        """This method expands :meth:`Technology.net_benefit` by taking into account biogas availability
        in the calculations.

        Parameters
        ----------
        model: OnStove model
            Instance of the OnStove model containing the main data of the study case. See
            :class:`onstove.onstove.OnStove`.
        w_health: int
            Determines whether health parameters (reduced morbidity and mortality)
            should be considered in the net-benefit equation.
        w_spillovers: int
            Determines whether spillover effects from cooking with traditional fuels
            should be considered in the net-benefit equation.
        w_environment: int
            Determines whether environmental effects (reduced emissions) should be considered in the net-benefit
            equation.
        w_time: int
            Determines whether opportunity cost (reduced time spent) should be considered in the net-benefit
            equation.
        w_costs: int
            Determines whether costs should be considered in the net-benefit equation.

        See also
        --------
        net_benefit
        """
        super().net_benefit(model, w_health, w_spillovers, w_environment, w_time, w_costs)
        required_energy_hh = self.required_energy_hh(model)
        model.gdf.loc[(model.gdf['biogas_energy'] < required_energy_hh), "benefits_{}".format(self.name)] = np.nan
        model.gdf.loc[(model.gdf['biogas_energy'] < required_energy_hh), "net_benefit_{}".format(self.name)] = np.nan
        factor = model.gdf['biogas_energy'] / (required_energy_hh * model.gdf['Households'])
        factor[factor > 1] = 1
        self.factor = factor
        self.households = model.gdf['Households'] * factor

        del model.gdf["Cattles"]
        del model.gdf["Buffaloes"]
        del model.gdf["Sheeps"]
        del model.gdf["Goats"]
        del model.gdf["Pigs"]
        del model.gdf["Poultry"]
