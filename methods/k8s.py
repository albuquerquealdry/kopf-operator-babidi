import os
import yaml
import kubernetes.client
import logging



class KubernetesHandler:
    def __init__(self, logger, namespace):
        self.api = kubernetes.client.AppsV1Api()
        self.s_api = kubernetes.client.CoreV1Api()
        self.logger = logger
        self.namespace = namespace

    def manifest_operation(name, file, spec):
        path = os.path.join(os.path.dirname(__file__), f'{file}.yaml')
        tmpl = open(path, 'rt').read()
        if file == 'deployment':
            text = tmpl.format(name=name, image=spec['image'], replicas=spec['replicas'], version=spec['version'])
            data = yaml.safe_load(text)
            return data
        elif file == 'service':
            text = tmpl.format(name=name, node_port=spec['node_port'])
            data = yaml.safe_load(text)
            return data

    def create_deployment(self, spec, name):
        data = KubernetesHandler.manifest_operation(name, 'deployment', spec)
        obj = self.api.create_namespaced_deployment(namespace=self.namespace, body=data)
        self.logger.info(f"Deployment created: {obj}")
 
    def create_service(self, spec, name):
        data = KubernetesHandler.manifest_operation(name, 'service', spec)
        obj = self.s_api.create_namespaced_service(namespace=self.namespace, body=data)
        self.logger.info(f"Service created: {obj}")

    def update_deployment(self, spec, name):
        data = KubernetesHandler.manifest_operation(name, 'deployment', spec)
        obj = self.api.patch_namespaced_deployment(f"{name}-deployment", namespace=self.namespace, body=data)
        self.logger.info(f"Deployment updated: {obj}")

    def update_service(self, spec, name):
        data = KubernetesHandler.manifest_operation(name, 'service', spec)
        obj = self.s_api.patch_namespaced_service(name=f"{name}-service", namespace=self.namespace, body=data)
        self.logger.info(f"Service updated: {obj}")

    def delete_resources(self, name):
        self._delete_deployment(name)
        self._delete_service(name)

    def _delete_deployment(self, name):
        try:
            self.api.delete_namespaced_deployment(name=f"{name}-deployment", namespace=self.namespace)
            self.logger.info(f"Deployment {name}-deployment deleted successfully.")
        except kubernetes.client.exceptions.ApiException as e:
            if e.status != 404:
                self.logger.error(f"Error deleting Deployment {name}-deployment: {e}")

    def _delete_service(self, name):
        try:
            self.s_api.delete_namespaced_service(name=f"{name}-service", namespace=self.namespace)
            self.logger.info(f"Service {name}-service deleted successfully.")
        except kubernetes.client.exceptions.ApiException as e:
            if e.status != 404:
                self.logger.error(f"Error deleting Service {name}-service: {e}")