from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class Empleado(models.Model):
    _name = "empleado"
    
    name          = fields.Char(string="Nombre del Empleado", required=True)
    job_title     = fields.Char(string="Cargo")
    start_date    = fields.Date(string="Fecha de contratación", required=True)
    salary        = fields.Float(string="Salario", required=True)
    department_id = fields.Many2one(comodel_name='departamento', string="Departamento", optional={'no_create':True}, required=True, ondelete="cascade" )
    
    
    _sql_constraints = [("unique_name","unique(name)","Existe un empleado con el mismo nombre")]
    
    
    @api.constrains("start_date")
    def _check_start_date(self):
        for record in self:
            if record.start_date > date.today():
                raise ValidationError("Error en la fecha de contratación")
            
    @api.constrains("salary")
    def _check_salary(self):
        for record in self:
            if record.salary < 0:
                raise ValidationError("El salario no puede ser nagativo")
            
    @api.constrains("department_id")
    def _check_department(self):
        for record in self:
            if record.department_id.available_capacity < 0:
                raise ValidationError(f"El departamento {record.department_id.name} no tiene capacidad.")
            
    # def unlink(self):
    #     for employee in self:
    #         department = employee.department_id
        
    #     department.employee_ids
        
    #     return super().unlink()
    
    