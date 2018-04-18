import subprocess
import re
from hcloud.libs.celery.celery import celery
from hcloud.models.alert_rules import AlertRulesData
from hcloud.logger import logging
from hcloud.libs.monitor import monitor
@celery.task
def push_alert(cmd, alert_rules_id):
    msg = ""
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()

    #     for x in output.replace('*', '').strip().split("\n"):
    #         p1 = re.compile(r'failed=(\d)')
    #         r1 = p1.search(x)
    #         p2 = re.compile(r'unreachable=(\d)')
    #         r2 = p2.search(x)
    #         if r1 is None or r2 is None:
    #             continue
    #         else:
    #             flag = True
    #         failed_count = int(r1.group(1))
    #         unreachable_count = int(r2.group(1))
    #         if failed_count != 0 or unreachable_count != 0:
    #             msg += "There are {0} ansible-playbook sub task run into error".format(
    #                 failed_count + unreachable_count)
    #     if flag is False:
    #         msg += "ansible-playbook command execute failed."
    #
    # except Exception as e:
    #     #return {'status': -1, 'result': str(e)}
    #     msg += str(e)
    #
    # try:
    #     if msg != "":
    #         logging.error(msg)
    #         AlertRulesData.update_status(alert_rules_id, 2)
    #     else:
    #         AlertRulesData.update_status(alert_rules_id, 1)
    #         url = 'http://localhost:9090'
    #         monitor.reload(url)
    # except Exception as e:
    #     logging.error(e)
    except Exception as e:
        return {'status': -1, 'result': str(e)}

    return {'status': p_status, 'result': output.strip()}

def _push_alert_db():
    pass


@celery.task
def async_cmd_task(cmd):
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
    except Exception as e:
        return {'status': -1, 'result': str(e)}
    return {'status': p_status, 'result': output.strip()}
