from odoo import models,fields,api
from . import bifold_helpers
import logging
from odoo.exceptions import UserError

class CortizoEstimation(models.Model):
    _name = "cortizo.bifold.estimation"
    _description = "Cortizo Estimation"
    name = fields.Char(string="Name")
    state = fields.Selection(selection=[('draft','Draft'),('component_list','Components Listed'),('quantities_calculated','Quantities Calculated')], string="Status")
    left_shutter = fields.Integer(string="Left Shutter")
    right_shutter = fields.Integer(string="Right Shutter")
    length = fields.Float(string="Length")
    height = fields.Float(string="Height")
    opening = fields.Selection(string="Opening",selection=[('IN','IN'),('OUT','OUT')])
    sill_type = fields.Selection(string="Sill Type",selection=[('STD','STD'),('LTH-1','LTH - 1'),('LTH-2','LTH - 2')])
    slide_type = fields.Selection(string="Slide Type",selection=[('Post','Post'),('H/Roller','H/Roller')])
    jamb_type = fields.Selection(string="Jamb Type",selection=[('STD','STD'),('ADJ','ADJ')])
    point_lock = fields.Selection(string="Point Lock",selection=[('3_point','3 Point'),('4_point','4 Point')])
    lth = fields.Selection(string="LTH", selection=[('STD','STD'),('Recess','Recess')])
    component_line_ids = fields.One2many('cortizo.bifold.component.line','estimation_id',string="Components", domain=[('is_accessory','=',False)])
    accessory_line_ids = fields.One2many('cortizo.bifold.component.line','estimation_id',string="Accessories", domain=[('is_accessory','=',True)])
    cost_line_ids = fields.One2many('cortizo.bifold.cost.line','estimation_id', string="Cost Lines")

    def create_components_cutting_list(self):
        logger = logging.getLogger("Bifold loger: ")
        self.component_line_ids.unlink()
        values = [self.length,self.height,self.left_shutter,self.right_shutter,self.opening,self.sill_type,self.jamb_type,self.slide_type,self.point_lock,self.lth]
        components,accessories = bifold_helpers.create_cortizo(*values)
        # logger.error("components: "+str(components))
        # logger.error("accessories: "+str(accessories))
        for component in components:
            self.env['cortizo.bifold.component.line'].create({
                'material_name': component[0]+" "+component[1],
                'material_reference': component[0],
                'shape': component[2],
                'length': component[3],
                'units': component[4],
                'estimation_id': self.id,
                'is_accessory': False,

            })

        for accessory in accessories:
            self.env['cortizo.bifold.component.line'].create({
                'material_name': accessory[0]+" "+accessory[1],
                'material_reference': component[0],
                # 'shape': accessory[2],
                # 'length': accessory[3],
                'units': accessory[2],
                'estimation_id': self.id,
                'is_accessory': True,
            })

    def create_cost_list(self):
        self.cost_line_ids.unlink()
        results = bifold_helpers.total_cost(self.component_line_ids+self.accessory_line_ids)
        for cost_result in results:
            self.env['cortizo.bifold.cost.line'].create({
                'material_name': cost_result[0],
                'quantity': cost_result[1],
                'unit_cost': cost_result[2],
                'total_cost': cost_result[3],
                'balance_length': cost_result[4],
                'estimation_id': self.id,
            })




class CortizoBifoldComponentLine(models.Model):
    _name = "cortizo.bifold.component.line"
    estimation_id = fields.Many2one('cortizo.bifold.estimation')
    product_id = fields.Many2one('product.product',string="Product")
    is_accessory = fields.Boolean(string="Is Accessory")
    material_name = fields.Char(string="Material Name")
    material_reference = fields.Char(string="Material Reference")
    part_name = fields.Char(string="Part Name")
    shape = fields.Char(string="Shape")
    length = fields.Float(string="Length")
    units = fields.Float(string="Units")

class CortizoBifoldCostLine(models.Model):
    _name = "cortizo.bifold.cost.line"
    material_name = fields.Char(string="Material Name")
    estimation_id = fields.Many2one('cortizo.bifold.estimation')
    quantity = fields.Float(string="Quantity")
    unit_cost = fields.Float(string="Unit Cost")
    total_cost = fields.Float(string = "Total Cost")
    balance_length = fields.Float(string = "Balance Length")




