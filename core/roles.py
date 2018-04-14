from rolepermissions.roles import AbstractUserRole

class Agent(AbstractUserRole):
    available_permissions = {
        'view_call_console': True,
        'create_call_record': True,
        'edit_call_record': True,
        'login_call_console': True,
        'logout_call_console': True,
    }

class Supervisor(AbstractUserRole):
    available_permissions = {
        'view_call_console': True,
        'create_call_record': True,
        'edit_call_record': True,
        'login_call_console': True,
        'logout_call_console': True,
    }
class Admin(AbstractUserRole):
    available_permissions = {
        'create_medical_record': True,
    }

class Dispatcher(AbstractUserRole):
    available_permissions = {
        'edit_patient_file': True,
    }