import uuid
from flask_restful import Resource, marshal_with
from flask import request
from hcloud.server.api.alert.controller import AlertManager
from hcloud.server.api.alert.controller import Ansible
from hcloud.exceptions import Error
from hcloud.exceptions import ModelsDBError
from .views import AlertRulesViews

class SendToAlert(Resource):
   def post(self):
       try:
           json_data = request.get_json(force=True)
           state = json_data['alerts']['status']
           exported_instance = json_data['alerts']['labels']['exported_instance']
           alertname = json_data['alerts']['labels']['alertname']
           monitor_iterm = alertname.split['_'][1]
           service = json_data['alerts']['labels']['service']

           endsAt = json_data['alerts']['endsAt']
           startsAt = json_data['alerts']['startsAt']
           description = json_data['alerts']['annotations']['description']
           current_value = description.split('=')[1]
           summary = json_data['alerts']['annotations']['summary']
           last_time = 0
           alert_rules = AlertManager.get_alert_rules_by_name(monitor_iterm)
           contact_groups = alert_rules['contact_groups']
           alert_rules_id = alert_rules['alert_rules_id']

           status = AlertManager.send_alert(monitor_iterm, summary, description, contact_groups )

           data_res = AlertManager.create_alert(alert_rules_id, exported_instance, service, alertname,
                                                startsAt, current_value, last_time, state, contact_groups, status)
       except Exception as e:
           raise Error(e)
       return {'status': 'ok'}, 201

class CreateAlertRules(Resource):

    def post(self):
        args = AlertRules.alert_rules_parser.parse_args()
        host_id = args['host_id']
        port = args['port']
        service = args['service']
        monitor_items = args['monitor_items']
        statistical_period = args['statistical_period']
        statistical_approach = args['statistical_approach']
        compute_mode = args['compute_mode']
        threshold_value = args['threshold_value']
        silence_time = args['silence_time']
        contact_groups = args['contact_groups']
        notify_type = args['notify_type']
        try:
            # running
            alert_rules_id = str(uuid.uuid1())
            # insert mysql
            data_res = AlertManager.create_alert_rules(alert_rules_id, host_id, service, monitor_items,
                                                      statistical_period, statistical_approach, compute_mode,
                                                      threshold_value, silence_time, contact_groups, notify_type, 0)
            Ansible.check(host_id)
            inv_file = Ansible.init_target_yaml(host_id)
            instance = host_id + ":" + str(port)
            yml_file = Ansible.init_metrics_yaml(service, monitor_items, host_id, instance, threshold_value, statistical_period, compute_mode)
            Ansible.execute(yml_file, inv_file, alert_rules_id)
        except Exception as e:
            raise Error(e)
        return {'status': 'ok'}, 201

class AlertRules(Resource):

    alert_rules_data_fields = AlertRulesViews.alert_rules_data_fields


    @marshal_with(alert_rules_data_fields)
    def get(self, alert_rules_id):
        try:
            data_res = AlertManager.get_alert_rules(alert_rules_id)
        except Exception as e:
            raise ModelsDBError(str(e))
        return {'data': data_res, 'total': len(data_res)}

    def put(self, alert_rules_id):
        alert_rules_parser = AlertRulesViews.json_data
        action = alert_rules_parser['action']
        if action['method'] == 'modify':
            statistical_period = action['param']['statistical_period']
            statistical_approach = action['param']['statistical_approach']
            compute_mode = action['param']['compute_mode']
            threshold_value = action['param']['threshold_value']
            contact_groups = action['param']['contact_groups']
            notify_type = action['param']['notify_type']
            try:
                data_res = AlertManager.update_alert_rules(alert_rules_id, statistical_period, statistical_approach,
                                                           compute_mode, threshold_value, contact_groups, notify_type)
            except Exception as e:
                raise Error(str(e))
            return {'status': 'ok'}, 201
        elif action['method'] == 'disable':
            pass
        elif action['method'] == 'enable':
            pass
        return {'status': 'ok'}, 201






