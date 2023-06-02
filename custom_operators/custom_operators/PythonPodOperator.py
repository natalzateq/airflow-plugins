from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator 
from airflow.kubernetes.volume_mount import VolumeMount 
from airflow.kubernetes.volume import Volume   
import inspect
import os

class PythonPodOperator:
    def __init__(self, task_id, python_callable, op_kwargs, requirements=[], namespace="airflow"):  
        self.task_id = task_id
        self.python_callable = python_callable
        self.op_kwargs = op_kwargs
        self.requirements = requirements
        self.namespace = namespace
        self.volumes = []
        self.volume_mounts = [] 
        self.func_path = os.path.abspath(inspect.getfile(self.python_callable))
        self.dir_path = '/'.join(self.func_path.split('/')[0:-1])

    def addVolume(self, volumen):
        self.volumes.append(Volume(name=volumen["name"], configs=volumen["config"])) 

    def addVolumeMount(self, volumen):
        self.volume_mounts.append(VolumeMount(name=volumen["name"], mount_path=volumen["mount_path"], sub_path=volumen["sub_path"], read_only=volumen["read_only"])) 

    def installReqs(self):
        os.system(f"rm -rf {self.dir_path}/req.txt")
        for key in self.requirements:
            os.system(f"echo {key} >> {self.dir_path}/req.txt") 

    def buildExecutor(self):
        os.system(f"rm -rf {self.dir_path}/executor-{self.task_id}.sh")
        if len(self.requirements) > 0:
            os.system(f"echo pip install -r {self.dir_path}/req.txt >> {self.dir_path}/executor-{self.task_id}.sh")
        os.system(f"echo python {self.func_path} >> {self.dir_path}/executor-{self.task_id}.sh") 
        

    def podOperator(self): 
        
        self.addVolume({'name':'airflow-dags', 'config':{ 'persistentVolumeClaim': { 'claimName': 'airflow-dags' } }})
        self.addVolumeMount({'name':'airflow-dags', 'mount_path':'/root/airflow/dags', 'sub_path':None, 'read_only':False})
        self.addVolume({'name':'airflowcfg', 'config':{ 'configMap': { 'name': 'airflowcfg' } }})
        self.addVolumeMount({'name':'airflowcfg', 'mount_path':'/root/airflow/airflow.cfg', 'sub_path':'airflow.cfg', 'read_only':False})

        if len(self.requirements) > 0:
            self.installReqs()
 
        self.buildExecutor()

        task = KubernetesPodOperator( 
            task_id=self.task_id, 
            image='742594676421.dkr.ecr.us-west-2.amazonaws.com/airflow:8ae004e1-prod',
            in_cluster=True, 
            namespace= self.namespace, 
            name=self.task_id, 
            get_logs=True, 
            log_events_on_failure=True,  
            cmds=['sh'],
            arguments=[f"{self.dir_path}/executor-{self.task_id}.sh"],
            volumes= self.volumes,
            volume_mounts=self.volume_mounts,
        )        

        return task