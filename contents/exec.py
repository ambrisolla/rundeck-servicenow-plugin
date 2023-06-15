import os
import sys
import yaml
import time
import json
import requests
import datetime
from requests.auth import HTTPBasicAuth
from lib.arguments import Arguments

class RundeckServiceNowApproval:

    def __init__(self):
        self.TEMP_DIR = '/tmp'
        self.HEADERS = { 'Content-type': 'application/json' }
        self.FULL_PATH = os.path.realpath(os.path.dirname(__file__))
        self.ARGUMENTS = Arguments()
        self.SN_AUTH = HTTPBasicAuth(
            self.ARGUMENTS.SN_USERNAME,
            self.ARGUMENTS.SN_PASSWORD)
        
    def loadTemplate(self, template):        
        try:
            is_yml = os.path.exists(
                f'{self.FULL_PATH}/templates/{template}.yml')
            is_yaml = os.path.exists(
                f'{self.FULL_PATH}/templates/{template}.yaml')
            if is_yaml:
                file_ext = 'yaml'
            elif is_yml:
                file_ext = 'yml'
            else:
                raise Exception('Template file not found!')            
            with open(
                f'{self.FULL_PATH}/templates/{template}.{file_ext}') \
                    as template_file:
                template = yaml.safe_load(template_file.read())
                return template                
        except Exception as err:
            raise Exception(err)
        
    def getChangeDuration(self, duration):
        start_date = datetime.datetime.now()
        end_date = start_date + datetime.timedelta(hours=duration)
        return {
            'start_date' : str(start_date),
            'end_date' : str(end_date) }
    
    def submitNormalChange(self, template):
        endpoint = '/api/sn_chg_rest/change'
        req = requests.post(
            f'{self.ARGUMENTS.SN_SERVER}{endpoint}', 
            auth=self.SN_AUTH,
            headers=self.HEADERS,
            json=template)
        if req.status_code == 200:
            data = req.json()            
            change_number = data['result']['number']['display_value']
            change_sys_id = data['result']['sys_id']['display_value']
            change_short_description = data['result']['short_description']['display_value']            
            output = (
                 '  Change info:\n'
                f'    - number: {change_number}\n'
                f'    - sys_id: {change_sys_id}\n'
                f'    - short_description: {change_short_description}')            
            print(output)            
            self.createFileWithChangeInfo(change_number)
        else:
            print(f'  Error creating change: {req.reason}')        
        return {
            'change_number' : change_number,
            'change_sys_id' : change_sys_id }
    
    def createNormalChange(self):
        print('\n- Creating change...\n')
        template = self.loadTemplate(self.ARGUMENTS.TEMPLATE) 
        change_duration = self.getChangeDuration(template['change_duration'])
        template['start_date'] = change_duration['start_date']
        template['end_date'] = change_duration['end_date']
        template['approval'] = 'Requested'
        return self.submitNormalChange(template)
            
    def waitForChangeApproval(self, change_number):
        change = self.getChangeStatus(change_number)
        is_scheduled = change['change_state'] == 'Scheduled'
        is_approved = change['change_approval'] == 'Approved'
        self.createFileWithChangeInfo(change_number)
        log_output = (
            f'{str(datetime.datetime.now())}'
            f' change: {change_number},'
            f' state: {change["change_state"]},'
            f' approval_status: {change["change_approval"]}' )
        
        print(log_output)
        if change["change_approval"] == 'Rejected':
            rejected_output = (
                f'\nChange {change_number} was rejected.'
                 '\n\n-  Change approval history:'
                f'\n\n{change["change_approval_history"]}')
            print(rejected_output)
            sys.exit(1)

        if is_scheduled and is_approved:
            approved_output = (
                f'\nChange {change_number} was approved.'
                 '\n\n- Change approval history:\n'
                f'\n\n{change["change_approval_history"]}')
            print(approved_output)
        else:
            time.sleep(10)
            self.waitForChangeApproval(change_number)

    def setChangeState(self, **kwargs):
        print(f' - Setting change state to: {kwargs["state"]}')
        endpoint = f'/api/sn_chg_rest/change/{kwargs["change_sys_id"]}'
        if kwargs['state'] == 'Closed':
            params = { 
                'state' : 'Closed',
                'close_code' : kwargs['close_code'],
                'close_notes' : kwargs['close_notes'] }
        else:
            params = { 'state' : kwargs['state'] }
        req = requests.patch(
            f'{self.ARGUMENTS.SN_SERVER}{endpoint}', 
            auth=self.SN_AUTH,
            headers=self.HEADERS,
            params=params )
        self.createFileWithChangeInfo(kwargs['change_number'])
        if req.status_code == 200:
            return req.text
        else:
            print(req.text)
            sys.exit(1)
    
    def getChangeStatus(self, change_number):
        endpoint = '/api/sn_chg_rest/change'
        params = { 'number' : change_number }
        req = requests.get(
            f'{self.ARGUMENTS.SN_SERVER}{endpoint}', 
            auth=self.SN_AUTH,
            headers=self.HEADERS,
            params=params )
        if req.status_code == 200:
            return {
                'status' : True,
                'change_sys_id' : req.json()['result'][0]['sys_id']['display_value'], 
                'change_number' : change_number,
                'change_state' : req.json()['result'][0]['state']['display_value'],
                'change_approval' : req.json()['result'][0]['approval']['display_value'],
                'change_approval_history' : req.json()['result'][0]['approval_history']['display_value']}
    
    def createFileWithChangeInfo(self, change_number):
        change = self.getChangeStatus(change_number)
        RD_JOB_EXECID = os.getenv('RD_JOB_EXECID')
        with open(f'{self.TEMP_DIR}/RD_JOB_{RD_JOB_EXECID}.json', 'w') as job_file:
            job_file.write(json.dumps(change))
    
    def getRundeckJobInfo(self, job_id):
        endpoint = f'/api/43/execution/{job_id}'
        req = requests.get(
            f'{self.ARGUMENTS.RD_SERVER}/{endpoint}',
            headers={            
                'X-Rundeck-Auth-Token': self.ARGUMENTS.RD_TOKEN,
                'Accept': 'application/json' })
        if req.status_code == 200:
            return req.json()
        else:
            print(f'{req.text}')
            sys.exit(1)

    def getChangeInfoAssociatedWithRundeckJob(self, job_id):
        try:
            with open(f'{self.TEMP_DIR}/RD_JOB_{job_id}.json', 'r') as file:
                data = json.loads(file.read())
                return data
        except Exception as err:
            print(str(err))
            sys.exit(1)
    
    def closeNormalChange(self):
        if os.getenv('RD_OPTION_JOB_ID') == '' or os.getenv('RD_OPTION_JOB_ID') is None:
            job_id = int(os.getenv('RD_JOB_EXECID'))
            current = True
        else:
            job_id = int(os.getenv('RD_OPTION_JOB_ID'))
            current = False
        job_info = self.getRundeckJobInfo(job_id)
        change_info = self.getChangeInfoAssociatedWithRundeckJob(job_id)
        print(f'Change: {change_info["change_number"]} will be closed:')
        if current:
            change_close_code = 'Successful'
        else:
            negative_rundeck_job_status = ['failed', 'aborted']
            if job_info['status'] in negative_rundeck_job_status:
                change_close_code = 'Unsuccessful'
            elif job_info['status'] == 'succeeded':
                change_close_code = 'Successful'
        change_close_notes = (
            f'- Rundeck server: {self.ARGUMENTS.RD_SERVER} \n'
            f'- Rundeck job ID: {job_id} \n'
            f'- Rundeck project: {job_info["job"]["project"]}\n'
            f'- Rundeck job link: {job_info["permalink"]}')
        self.setChangeState(
            change_sys_id=change_info['change_sys_id'],
            change_number=change_info['change_number'],
            state='Review')    
        self.setChangeState(
            change_sys_id=change_info['change_sys_id'],
            change_number=change_info['change_number'],
            state='Closed',
            close_code=change_close_code,
            close_notes=change_close_notes)
    
if __name__ == '__main__':
    service_now = RundeckServiceNowApproval()
    if service_now.ARGUMENTS.ACTION == 'open_change':
        change = service_now.createNormalChange()            
        service_now.setChangeState(
            change_sys_id=change['change_sys_id'],
            change_number=change['change_number'],
            state='Assess')        
        print('- Waiting for change approval...\n')        
        service_now.waitForChangeApproval(change['change_number'])
        service_now.setChangeState(
            change_sys_id=change['change_sys_id'],
            change_number=change['change_number'],
            state='Implement')        
    elif service_now.ARGUMENTS.ACTION == 'close_change':
        change = service_now.closeNormalChange()