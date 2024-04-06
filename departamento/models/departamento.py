from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Departamento(models.Model):
    _name = "departamento"
    
    name = fields.Char(string="Nombre del departamento" ,required=True)
    description = fields.Text(string="Funciones del departamento")
    total_salary = fields.Float(string="Salario total del Departamento", compute='_calculate_total_salary')
    capacity = fields.Integer(string="Capacidad del departamento")
    available_capacity = fields.Integer(string="Vacantes", compute="_calculate_capacity")
    total_employee_actual = fields.Integer(string="Total de Empleados", compute="_calculate_total_employees")
    employee_ids = fields.One2many(comodel_name='empleado', inverse_name='department_id',string="Empleados", required=True, ondelete='cascade')    
        
    @api.constrains
    def _check_capacity(self):
        for record in self:
            if record.capacity < 0:
                raise ValidationError("La capacidad no puede ser negativa")
    
    @api.onchange("employee_ids")
    def _calculate_total_salary(self):
        for _ in self:
            _.total_salary = 0
            for record in _.employee_ids:
                _.total_salary += record.salary
            print(_.total_salary)
            
    @api.onchange("employee_ids")
    def _calculate_total_employees(self):
        for _ in self:
            _.total_employee_actual = 0
            for record in _.employee_ids:
                _.total_employee_actual += 1
                
    @api.onchange("total_employee_actual")
    def _calculate_capacity(self):
        for record in self:
            record.available_capacity = record.capacity - record.total_employee_actual
            
    # @api.model
    # def create(self, values):
    #     for record in self:
    #         if record.available_capacity < 1:
    #             raise ValidationError("El departamento {record.name} no tiene capacidad.")
    #     return super(Departamento, self.create(values))
    
    
        # prueba = fields.Boolean(string="required")
    
    # @api.onchange("prueba")
    # def _check_prueba(self):
    #     if self.prueba:
    #         self._context['name_required'] = True
        