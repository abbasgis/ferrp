from django.db import models

# Create your models here.


class AdpDraft201718Vw(models.Model):
    gs_no = models.TextField(primary_key=True)  # This field type is a guess.
    s_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    district = models.TextField(blank=True, null=True)  # This field type is a guess.
    tehsil = models.TextField(blank=True, null=True)  # This field type is a guess.
    s_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    sec_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    sec_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    approval_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    cost_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    foreign_aid = models.TextField(blank=True, null=True)  # This field type is a guess.
    local_capital = models.TextField(blank=True, null=True)  # This field type is a guess.
    local_revenue = models.TextField(blank=True, null=True)  # This field type is a guess.
    capital_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    revenue_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    foreign_capital = models.TextField(blank=True, null=True)  # This field type is a guess.
    foreign_revenue = models.TextField(blank=True, null=True)  # This field type is a guess.
    allocation = models.TextField(blank=True, null=True)  # This field type is a guess.
    exp_upto_june = models.TextField(blank=True, null=True)  # This field type is a guess.
    projection_2017_18 = models.TextField(db_column='projection_2017-18', blank=True,
                                          null=True)  # Field renamed to remove unsuitable characters. This field type is a guess.
    projection_2018_19 = models.TextField(db_column='projection_2018-19', blank=True,
                                          null=True)  # Field renamed to remove unsuitable characters. This field type is a guess.
    throw_forward = models.TextField(blank=True, null=True)  # This field type is a guess.
    monitoring = models.TextField(blank=True, null=True)  # This field type is a guess.
    start_date = models.TextField(blank=True, null=True)
    end_date = models.TextField(blank=True, null=True)
    cost_total_adp_origional = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'adp_draft_201718_vw'


class TblSchemesHistory(models.Model):
    id = models.AutoField(primary_key=True)
    gs_no = models.IntegerField(blank=True, null=True)
    project_location = models.TextField(blank=True, null=True)
    authorities_responsible = models.TextField(blank=True, null=True)
    plan_provision = models.TextField(blank=True, null=True)
    project_objectives = models.TextField(blank=True, null=True)
    annual_operating_cost = models.TextField(blank=True, null=True)
    capital_cost_estimates = models.TextField(blank=True, null=True)
    physical_plan = models.TextField(blank=True, null=True)
    financial_plan = models.TextField(blank=True, null=True)
    financial_plan_text = models.TextField(blank=True, null=True)
    gantt_chart = models.TextField(blank=True, null=True)
    demand_and_supply_analysis = models.TextField(blank=True, null=True)
    benefits_of_the_projects_analysis = models.TextField(blank=True, null=True)
    implementation_schedule = models.TextField(blank=True, null=True)
    ms_and_mp = models.TextField(blank=True, null=True)
    additional_projects_decisions_required = models.TextField(blank=True, null=True)
    certified = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_schemes_history'

class TblSchemesAnnexure(models.Model):
    id = models.TextField(primary_key=True)
    gs_no = models.TextField(blank=True, null=True)
    annexure_title = models.TextField(blank=True, null=True)
    annexure_data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_scheme_annexure'

class TblHelp(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    section_name = models.TextField(blank=True, null=True)
    info_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    help_image = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_help'

