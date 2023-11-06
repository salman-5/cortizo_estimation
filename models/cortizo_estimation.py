from odoo import models,fields,api

class CortizoEstimation(models.Model):
    _name = "cortizo.estimation"
    _description = "Cortizo Estimation"
    name = fields.Char(string="Name")
    left_shutter = fields.Integer(string="Left Shutter")
    right_shutter = fields.Integer(string="Right Shutter")
    length = fields.Float(string="Length")
    height = fields.Float(string="Height")
    opening = fields.Selection(string="Opening",selection=[('in','IN'),('out','OUT')])
    sill_type = fields.Selection(string="Sill Type",selection=[('std','STD'),('lth_1','LTH - 1'),('lth_2','LTH - 2')])
    slide_type = fields.Selection(string="Slide Type",selection=[('post','Post'),('h_roller','H/Roller')])
    jamb_type = fields.Selection(string="Jamb Type",selection=[('std','STD'),('adj','ADJ')])
    point_lock = fields.Selection(string="Point Lock",selection=[('3_point','3 Point'),('4_point','4 Point')])
    lth = fields.Selection(string="LTH", selection=[('std','STD'),('recess','Recess')])
    estimation_lines = fields.One2many('cortizo.estimation.line','estimation_id',string="Estimations")

class CortizoEstimationLine(models.Model):
    _name = "cortizo.estimation.line"
    estimation_id = fields.Many2one('cortizo.estimation')
    material_name = fields.Char(string="Material Name")
    part_name = fields.Char(string="Part Name")
    shape = fields.Char(string="Shape")
    length = fields.Float(string="Length")
    units = fields.Char(string="Units")
